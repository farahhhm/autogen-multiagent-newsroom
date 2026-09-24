# 📰 AutoGen Multi-Agent Newsroom (`autogen-multiagent-newsroom`)

A smart AI newsroom system powered by **Microsoft AutoGen** and local AI (**Ollama `llama3.1:8b`**). Instead of using just one AI, this project creates a **team of 4 specialized AI agents** that work together to research topics, write articles, and review them automatically.

---

## 📌 How the Team Works (Workflow Diagram)

```mermaid
flowchart TD
    subgraph Team1 [Step 1: Gather Facts]
        A[Reporter Agent] -->|1. Requests Facts| B[UserProxy Agent]
        B -->|2. Runs Python Tool| A
    end

    subgraph Team2 [Step 2: Write and Review]
        C[Writer Agent] -->|3. Sends Draft| D[Critic Agent]
        D -->|Revisions Needed| C
        D -->|4. Approve| E[Published Newsletter]
    end

    Team1 -->|Passes News Data| Team2


## 🤖 Meet the AI Agents

| Agent Name | Role | What It Actually Does |
|---|---|---|
| **Reporter** | Fact Finder | Asks the system to gather facts on a requested topic. |
| **UserProxy** | Helper Assistant | Runs the Python function to fetch the raw data and hands it to the Reporter. |
| **Writer** | Content Creator | Takes the raw facts and writes a short 150-word newsletter introduction. |
| **Critic** | Chief Editor | Reviews the draft. Asks for changes if needed, or says **"APPROVE"** when ready. |

---

## 📂 Repository File Breakdown
autogen-multiagent-newsroom/ ├── capstone_newsroom.py # Main program file containing all AI agents & workflow rules ├── run_log.txt # Live text record showing a real test run on the topic "rainbow" └── README.md # Project documentation


### Simple Explanation of the Files:

#### 1. `capstone_newsroom.py` (Main Code File)
* **Connects to Local AI**: Connects the agents to a free AI model (`llama3.1:8b`) running locally on your computer.
* **Gives Tools to Agents**: Gives the `Reporter` agent a custom search tool (`fetch_news_data`) to collect facts.
* **Controls Team Conversation**: Coordinates how the agents talk back and forth, and automatically stops the program once the `Critic` approves the draft.

#### 2. `run_log.txt` (Real Test Output)
* Records a full live test run on the topic **"rainbow"**.
* Shows step-by-step how the Reporter gathered facts, how the Writer wrote the story, and how the Critic reviewed and approved it.

---

## 🛠️ Simple Technology Summary

| Component | Tool Used | What It Does |
|---|---|---|
| **Agent Framework** | Microsoft AutoGen | Coordinates the 4 AI agents so they can work as a team |
| **AI Brain / Model** | Ollama (`llama3.1:8b`) | Generates answers and text locally on your computer |
| **Data Retrieval** | Python Functions | Fetches news data when requested by the Reporter agent |
