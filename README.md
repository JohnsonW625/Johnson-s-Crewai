# Johnson's CrewAI Twin — Homework Example 🚀

A compact example multi-agent project that demonstrates how to build two cooperating agents:
- a twin "research" agent that answers questions on behalf of Johnson using a local `information.txt` file 📄
- a writer agent that converts the twin's draft reply into a polished, formal first-person message and saves it to disk ✍️

This repository is intended as a homework/example project showing agent roles, tasks, and tool usage with `crewai` and `crewai_tools`.

---

## Contents 📁
- `main.py` — example agent definitions and a small runner
- `information.txt` — Johnson Wang's background used by the twin agent
- `requirements.txt` — Python dependencies
- `scripts/setup_env.sh` — helper script to create a virtualenv and install dependencies

## Quick overview 🔍
1. Run the program and enter a question for Johnson.
2. The twin agent reads `information.txt` and drafts a short first-person reply.
3. The writer agent formalizes the draft and saves the reply to `johnson_reply.md`.

## Requirements 📦
- Python 3.8+
- See `requirements.txt` for package versions. The project expects `crewai` and `crewai[tools]` to be available.

## Setup (recommended) 🛠️
1. Make the setup script executable and run it (zsh / macOS):

```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
source .venv/bin/activate
```

2. Set your OpenAI API key (required for real runs):

```bash
export OPENAI_API_KEY="sk-..."
```

- Optional (web search):

```bash
export SERPER_API_KEY="serper-..."
```

## Usage ▶️
Run the main script:

```bash
python main.py
```

The script will prompt for a question. If the agents successfully use the file tool, the final reply will be saved to `johnson_reply.md`.

## Agents & Tasks 🤖
- Twin agent (`create_twin_agent`):
  - Role: represent Johnson's persona and knowledge
  - Tools: `FileReadTool` pointing to `information.txt`
  - Task: read `information.txt` and draft a short first-person answer + support notes

- Writer agent (`create_writer_agent`):
  - Role: take the twin draft and produce a formal, concise first-person reply
  - Tools: `FileWriterTool` to save the final reply

Key task functions:
- `create_johnson_response_task(agent, question)` — instructs the twin to answer the question using local info
- `create_writing_task(agent, draft_output)` — instructs the writer to formalize and save the reply

## Development notes 🧭
- The current code uses a placeholder draft when wiring the tasks together for demonstration. For a full pipeline you can:
  1. Run the twin agent task and capture its output.
  2. Provide that output to `create_writing_task` and run the writer agent.

- Avoid hard-coding API keys in the source. Use environment variables as implemented.

