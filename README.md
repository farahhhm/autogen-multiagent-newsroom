


#### 1. `capstone_newsroom.py`
The main application entry point:
- **LLM Configuration**: Connects AutoGen agents to a local Ollama server running `llama3.1:8b` via OpenAI-compatible REST API (`http://localhost:11434/v1`).
- **Tool Registration**: Registers `fetch_news_data()` tool with `register_function()`, binding caller rights to `Reporter` and execution rights to `UserProxy`.
- **GroupChat Management**: Manages sequential conversations between agents, implementing custom termination checks (`TERMINATE` and `APPROVE`).

#### 2. `run_log.txt`
Live execution trace logging a full run on the topic *"rainbow"*:
- Logs tool invocation and execution by `UserProxy`.
- Records draft iteration between `Writer` and `Critic` up to final approval.

---

## 🛠️ Technical Specifications & Stack

| Component | Technology | Version / Setting | Role |
|---|---|---|---|
| **Multi-Agent Framework** | Microsoft AutoGen | `autogen-agentchat` | Agent orchestration & conversation management |
| **LLM Engine** | Ollama | Local Daemon | Serves LLM endpoints locally at `http://localhost:11434/v1` |
| **Target Model** | Meta Llama 3.1 | `llama3.1:8b` | Open-weights 8B parameter model |
| **Tool Execution** | Python Native | Functions | Local function execution for data retrieval |
