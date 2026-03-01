# Ollama Local LLM Setup Guide

This guide walks you through setting up **Ollama** for offline LLM support in **Transformer-Based Market Movement Prediction**.

---

## What is Ollama?

Ollama is a fast and lightweight CLI to run Large Language Models (LLMs) locally on your machine. It requires no API keys and works completely offline.

**Benefits:**
- ✅ Free and open-source
- ✅ No API calls or internet required
- ✅ Private (data never leaves your machine)
- ✅ Works with NVIDIA/AMD GPUs and CPUs
- ✅ Fast inference (~5-30 tokens/sec depending on hardware)

---

## Step 1: Download & Install Ollama

### For Windows:

1. Go to https://ollama.ai/download/windows
2. Download the **Ollama Windows installer**
3. Run the installer and follow on-screen prompts
4. Ollama will auto-start and run in the background

### Verify Installation:

Open PowerShell and run:
```powershell
ollama --version
```

You should see a version number like `0.1.X` or higher.

---

## Step 2: Pull a Model

Ollama runs models locally. You need to download one first.

### Recommended Models:

| Model | Size | Speed | Quality | Hardware |
|-------|------|-------|---------|----------|
| **mistral** | 4.1GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 8GB+ RAM |
| **neural-chat** | 4.1GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 8GB+ RAM |
| **llama2** | 3.8GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 8GB+ RAM |
| **llama2-uncensored** | 3.8GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 8GB+ RAM |
| **quantized-llama2** | 1.3GB | ⚡⚡⚡⚡ Very Fast | ⭐⭐ Fair | 4GB+ RAM |

### Pull the Model:

Open PowerShell and run:
```powershell
ollama pull mistral
```

This downloads the Mistral model (~4GB). First time takes 5-15 minutes depending on internet speed.

To pull a different model:
```powershell
ollama pull neural-chat
```

### List Downloaded Models:

```powershell
ollama list
```

---

## Step 3: Start Ollama Server

Ollama runs as a background service. It should auto-start, but you can manually start it:

```powershell
ollama serve
```

This starts the Ollama HTTP server on `http://localhost:11434`

**Keep this terminal open while using the application.**

---

## Step 4: Configure Your Application

### Option A: Auto-Detection (Recommended)

The project auto-detects Ollama. Just ensure it's running (Step 3).

### Option B: Manual Configuration

Create or edit `.env` file in the project root:

```env
# Use Ollama for LLM
LLM_BACKEND=ollama
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Step 5: Test the Connection

### Method 1: Test from Python

```powershell
cd "c:\Users\palam\OneDrive\Desktop\empty folder"
.\.venv\Scripts\python.exe
```

Then run:
```python
from llm_market_analyst import create_analyst

analyst = create_analyst("ollama")
print(analyst.model_type)  # Should print: ollama
```

### Method 2: Test Ollama Directly

Open a new PowerShell and run:
```powershell
ollama run mistral "What is the stock market?"
```

You should get an answer within 30 seconds (first response is slower).

---

## Step 6: Start Your Application

In your activated virtual environment:

```powershell
cd "c:\Users\palam\OneDrive\Desktop\empty folder"
.\.venv\Scripts\python.exe -m uvicorn serve:app --host 0.0.0.0 --port 8000 --reload
```

Visit: http://localhost:8000

The dashboard will use Ollama for market analysis automatically!

---

## Troubleshooting

### "Ollama not available locally"

**Solution:**
1. Ensure Ollama is running: Open new PowerShell and run `ollama serve`
2. Check if server is accessible: Open browser to `http://localhost:11434/api/tags`
3. You should see JSON with available models

### "Model not found"

**Solution:**
```powershell
ollama pull mistral
```

Then restart the application.

### "Connection refused on port 11434"

**Cause:** Ollama server not running

**Solution:**
```powershell
ollama serve
```

Keep this terminal open.

### Slow Response Times

**Cause:** Running on CPU (not GPU)

**Solutions:**
1. **Use a smaller model:**
   ```powershell
   ollama pull neural-chat:7b-quantized
   ```
   Then update `.env`:
   ```env
   OLLAMA_MODEL=neural-chat:7b-quantized
   ```

2. **Enable GPU support:**
   - NVIDIA: Requires CUDA toolkit (auto-enabled)
   - AMD: Requires ROCm (manual setup)
   - Intel: Requires Intel GPU drivers

---

## Available Models for Download

Check https://ollama.ai/library for the full list.

Popular choices:
```powershell
ollama pull llama2          # Meta's Llama (7B, good balance)
ollama pull neural-chat     # Intel's model (very good quality)
ollama pull mistral         # Mistral's model (fast, quality)
ollama pull orca-mini       # Lightweight (1.3GB)
ollama pull phi             # Tiny but capable (1.6GB)
```

---

## Using Ollama with Your Dashboard

Once set up, the market predictor will:

1. **Pull market data** from your ML model
2. **Generate insights** using Ollama
3. **Provide market analysis** in natural language
4. **Give trading recommendations** powered by local LLM

All processing happens on your machine - zero cloud calls!

---

## Next Steps

1. ✅ Install Ollama
2. ✅ Pull a model (`ollama pull mistral`)
3. ✅ Start Ollama server (`ollama serve`)
4. ✅ Start the dashboard
5. ✅ Login and use LLM features!

---

## Performance Tips

- **GPU users:** Models run 5-10x faster
- **CPU users:** Use quantized models (4-bit, 8-bit)
- **Low RAM (<8GB):** Use smaller models or quantized versions
- **First run:** Takes longer as model loads into memory

---

## More Info

- **Ollama Docs:** https://github.com/ollama/ollama
- **Model Library:** https://ollama.ai/library
- **Troubleshooting:** https://github.com/ollama/ollama/issues

---

**Happy offline LLM-ing! 🚀**
