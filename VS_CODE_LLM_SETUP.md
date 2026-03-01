# VS Code LLM Setup Guide

## 1. Open Your Project in VS Code
- Launch VS Code and open your project folder.

## 2. Install Recommended Extensions
- Python (ms-python.python)
- Jupyter (ms-toolsai.jupyter) [optional]
- REST Client (humao.rest-client) [optional]

## 3. Set Up Python Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Start Your LLM Server
- **Ollama:**
  ```powershell
  ollama serve
  ```
- **LM Studio:**
  - Open LM Studio app
  - Load your model and start the server (default: http://localhost:1234)

## 5. Run Integration Scripts
- For Ollama:
  ```powershell
  python query_ollama.py
  ```
- For LM Studio:
  ```powershell
  python query_lmstudio.py
  ```

## 6. (Optional) Test with REST Client
- Create a `.http` file and write API requests to test endpoints directly from VS Code.

---

You are now ready to use local LLMs in VS Code for development and testing!
