import json
import time
from datetime import datetime
from pathlib import Path
 
import requests
import streamlit as st
 
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODELS = ["qwen2.5:1.5b", "llama3.2:1b"]
PROMPT_TEMPLATES = {
    "Normal": "",
    "Explain simply": "Explain the answer in simple language that a beginner can understand.",
    "Summarize": "Give a short and clear summary of the topic.",
    "Define a term": "Give a clear definition and one simple example.",
    "Step-by-step": "Explain the answer in clear, numbered steps."
}
LOG_FILE = Path("logs/conversations.jsonl")
LOG_FILE.parent.mkdir(exist_ok=True)
 
st.set_page_config(page_title="z", page_icon="🧠", layout="wide")
 
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_metrics" not in st.session_state:
    st.session_state.last_metrics = None
 
 
def save_log(record):
    """Append one prompt response pair to a local JSONL file."""
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
 
 
def read_recent_logs(limit=10):
    """Return the most recent saved prompt response pairs."""
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    records = []
    for line in lines[-limit:]:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return records
 
 
def ask_model(model, messages):
    """Send the chat to local Ollama and return answer plus timing data."""
    start = time.perf_counter()
    response = requests.post(
        OLLAMA_CHAT_URL,
        json={"model": model, "messages": messages, "stream": False},
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()
    wall_seconds = time.perf_counter() - start
    eval_count = data.get("eval_count", 0)
    eval_seconds = data.get("eval_duration", 0) / 1_000_000_000

    tokens_per_second = eval_count / eval_seconds if eval_seconds > 0 else None
    return data["message"]["content"], {
        "wall_seconds": round(wall_seconds, 2),
        "load_seconds": round(data.get("load_duration", 0) / 1_000_000_000, 2),
        "output_tokens": eval_count,
        "tokens_per_second": round(tokens_per_second, 2) if tokens_per_second else None,
    }
 
 
st.title("Local AI Lab")
st.caption("Two local text models, one interface, no cloud AI API")
 
with st.sidebar:
    st.header("Controls")
    selected_model = st.selectbox("Choose a model", MODELS)

    selected_template = st.selectbox(
        "Choose a prompt template",
        list(PROMPT_TEMPLATES.keys())
    )
    st.success(f"Active model: {selected_model}")
    if st.button("Clear current conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_metrics = None
        st.rerun()
    st.divider()
    st.subheader("Last response")
    if st.session_state.last_metrics:
        metric = st.session_state.last_metrics
        st.metric("Response time", f"{metric['wall_seconds']} s")
        st.write(f"Model load time: {metric['load_seconds']} s")
        st.write(f"Output tokens: {metric['output_tokens']}")
        st.write(f"Tokens per second: {metric['tokens_per_second'] or 'Unavailable'}")
    else:
        st.write("Send a prompt to see timing.")
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
prompt = st.chat_input("Type a question for the selected local model")
 
if prompt is not None:
    if not prompt.strip():
        st.warning("Please enter a prompt before sending.")
    else:
        user_message = {"role": "user", "content": prompt.strip()}
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.markdown(user_message["content"])
        try:
            request_messages = st.session_state.messages.copy()

            template_instruction = PROMPT_TEMPLATES[selected_template]

            if template_instruction:
                request_messages.insert(0, {
                    "role": "system",
                    "content": template_instruction
                })

            with st.chat_message("assistant"):
                with st.spinner(f"{selected_model} is generating locally..."):
                    answer, metrics = ask_model(selected_model, request_messages)

                st.markdown(answer)
                st.caption(f"Model: {selected_model} | Response time: {metrics['wall_seconds']} seconds")

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.last_metrics = metrics

            save_log({
                "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
                "model": selected_model,
                "prompt": user_message["content"],
                "response": answer,
                **metrics,
            })
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach Ollama. Start Ollama from the Windows Start menu, then try again.")
        except requests.exceptions.Timeout:
            st.error("The model took too long. Wait a moment, try a shorter prompt, or restart Ollama.")
        except requests.exceptions.HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                st.error(f"Model not found. Run: ollama pull {selected_model}")
            else:
                st.error(f"Ollama returned an error: {error}")
        except Exception as error:
            st.error(f"Unexpected error: {error}")
 
with st.expander("Recent saved conversation log"):
    recent = read_recent_logs(10)
    if recent:
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("No saved prompt response pairs yet.")