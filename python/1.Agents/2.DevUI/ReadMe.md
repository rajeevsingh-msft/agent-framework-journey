## DevUI Weather Agent Demo

This directory contains a simple DevUI demo (`agents.py`) that creates a single weather assistant agent using the Agent Framework. It selects an Azure OpenAI chat model if all required Azure environment variables are present, otherwise it falls back to an OpenAI model.

### How It Works
1. Loads environment variables via `python-dotenv` (optional `.env`).
2. Chooses a chat client:
	- Azure path when `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` are set.
	- OpenAI path when `OPENAI_API_KEY` is set.
3. Instantiates a `ChatAgent` with name, description, instructions, and two tool functions.
4. Serves the agent locally through DevUI on `http://localhost:8090` using `serve()`.

### Agent Creation Location
The agent object is created in `agents.py` where `agent = ChatAgent(...)` appears. This binds the chosen `chat_client` and the list of tool functions to the agent instance before launching the DevUI server.

### Tool Functions
`get_weather(city)` and `get_forecast()` currently return static placeholder strings. They illustrate how the framework can call Python functions. Replace these with real API calls (e.g. Open-Meteo, WeatherAPI) for dynamic data.

### Required Environment Variables (Azure Option)
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT` (e.g. `https://<resource>.openai.azure.com/`)
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` (deployment name of your chat model)
- Optional: `AZURE_OPENAI_API_VERSION`

### Required Environment Variables (OpenAI Fallback)
- `OPENAI_API_KEY`
- Optional: `OPENAI_CHAT_MODEL_ID` (defaults to `gpt-4o-mini` if unset)

### Running the Demo
From the repo root:
```powershell
python .\python\2.DevUI\agents.py
```
The DevUI will open automatically (controlled by `auto_open=True`). If it does not, manually visit `http://localhost:8090`.

### Extending
- Replace placeholder tool logic with real API requests.
- Add more tools (e.g. unit conversion, severe weather alerts).
- Introduce memory or stateful components via framework capabilities.
- Wrap external calls with error handling and caching.

### Troubleshooting
- If you get "No chat client configured" ensure you have either the full Azure trio of vars or at least `OPENAI_API_KEY` set.
- Use PowerShell to inspect env vars:
```powershell
Get-ChildItem Env:AZURE_OPENAI* ; Get-ChildItem Env:OPENAI*
```

### License
See repository `LICENSE` for terms.

