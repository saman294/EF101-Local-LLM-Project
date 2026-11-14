# EF-101 Local Large Language Model Hosting and Evaluation System

**Project Name:** Local AI Lab  
**Project ID:** EF101-P16  
**Course:** ITFA (EF-101), Fall 2026  
**Section:** B  
**Group Number:** 16  
**Instructor:** Dr. Fezan Rafiq  

## Group Members

| Name | Student ID |
|---|---|
| Saman | EE-52 |
| Dua Toseef | EE-53 |
| Shafia Eeman | EE-59 |

## 1. Project Overview

Local AI Lab is a locally hosted Large Language Model (LLM) application developed using Python, Streamlit, and Ollama.

The application allows users to interact with two locally installed AI models through a single web interface. It does not use cloud-based AI APIs. Prompts and responses are processed locally on the computer.

## 2. Technologies Used

- Python 3.12
- Streamlit
- Ollama
- Requests
- JSONL for conversation logging
- Llama 3.2 (1B)
- Qwen 2.5 (1.5B)

## 3. Main Features

- Local AI chatbot interface
- Selection between two local language models
- Five predefined prompt templates
- Conversation history during the active session
- Option to clear the current conversation
- Automatic local conversation logging in JSONL format
- Response time and model load time measurements
- Output token and tokens-per-second information
- Error handling for Ollama connection problems, timeouts, and missing models
- Recent saved conversation log viewer

## 4. Project Structure

```text
EF101-Local-LLM-Project/
│
├── app.py
├── requirements.txt
├── README.md
└── logs/
    └── conversations.jsonl   (created automatically when conversations are saved)
```

## 5. Installation Requirements

Install the following software before running the application:

1. Python 3.12 (64-bit)
2. Ollama for Windows
3. Git (if cloning the repository)

The two required models are:

- `llama3.2:1b`
- `qwen2.5:1.5b`

## 6. Installation and Setup

### Step 1: Download the Project

Clone the repository:

```bash
git clone https://github.com/saman294/EF101-Local-LLM-Project.git
```

Open the project folder:

```bash
cd EF101-Local-LLM-Project
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 2: Install Python Dependencies

Open Command Prompt or PowerShell inside the project folder and run:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Download the AI Models

Make sure Ollama is installed and running. Open Command Prompt and run:

```bash
ollama pull llama3.2:1b
ollama pull qwen2.5:1.5b
```

To check the installed models:

```bash
ollama list
```

### Step 4: Run the Application

Inside the project folder, run:

```bash
streamlit run app.py
```

If the command is not recognized, use:

```bash
python -m streamlit run app.py
```

### Step 5: Open the Application

Open a web browser and visit:

```text
http://localhost:8501
```

Select a model, choose a prompt template, and enter a question.

## 7. Data Storage

The application does not use an online database. Conversation records are stored locally in:

```text
logs/conversations.jsonl
```

The application creates the `logs` folder automatically when it starts. Each saved conversation exchange is stored as a JSON object on a separate line.

The AI models are stored locally by Ollama. No cloud AI API or online database is used.

## 8. Offline Operation

An internet connection is required initially to download the software, Python packages, and AI models.

After installation and model downloads, the application can generate responses locally without an internet connection, provided Ollama and the downloaded models are available on the computer.

## 9. Login Information

The application does not include a login system. No username, password, or API key is required.

## 10. Project Report

The project report contains the objective, system specifications, software tools, model details, architecture, implementation, testing results, offline demonstration, group contributions, and source code appendix.

## 11. GitHub Repository

Repository link:

https://github.com/saman294/EF101-Local-LLM-Project

## 12. Project Type

EF-101 Fall 2026 System Understanding Project.
