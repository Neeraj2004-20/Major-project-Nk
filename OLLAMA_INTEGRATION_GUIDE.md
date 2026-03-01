# How Ollama Works in Your Market Prediction System

## Quick Start Summary

```
1. Download & Install Ollama
   → ollama.ai/download ← Downloads and installs locally

2. Download Mistral Model
   → ollama pull mistral ← ~4GB, fast inference

3. Start Ollama Server
   → ollama serve ← Listens on http://localhost:11434

4. Your Backend Auto-Detects
   → Connects to Ollama
   → Sends market analysis prompts
   → Receives LLM-powered insights

5. Dashboard Consumes Results
   → Displays market analysis
   → Shows trading signals (BUY/SELL/HOLD)
   → Provides risk assessment
```

---

## Technical Implementation

### **1. Ollama Dual-Mode Support**

Your system tries to connect to Ollama in TWO ways:

#### **Method A: Python SDK (Preferred)**
```python
# If `ollama` Python package is installed
import ollama

response = ollama.generate(
    model="mistral",
    prompt="Analyze AAPL stock...",
    stream=False  # Waits for complete response
)
analysis = response.get("response", "")
```

**Pros:** Native Python, automatic model loading  
**Cons:** Requires `ollama` package (already installed)

#### **Method B: HTTP API (Fallback)**
```python
# If ollama package not available, use HTTP
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Analyze AAPL stock...",
        "stream": False
    },
    timeout=60
)
analysis = response.json().get("response", "")
```

**Pros:** Works even without Python package, language-agnostic  
**Cons:** HTTP overhead, must wait for response

---

## System Architecture

### **Initialization Chain**

```python
# In serve.py when app starts:
from ai_llm_integration import AIMarketIntelligence

ai = AIMarketIntelligence()
# → Creates LLMMarketAnalyst
# → Checks LLM_BACKEND environment variable
# → Auto-detects Ollama availability
# → Initializes gracefully (no blocking)
```

### **Market Analysis Pipeline**

```
User Request (login.html → index.html)
    ↓
GET /dashboard or POST /llm-analyze
    ↓
serve.py receives request
    ↓
ai_llm_integration.analyze_stock(symbol, prices, sentiment)
    ↓
AIMarketIntelligence.analyze_stock()
    ↓
Creates MarketAnalysisInput:
  - symbol: "AAPL"
  - current_price: 150.00
  - predicted_price: 152.50
  - sentiment_score: 0.65 (positive)
  - technical_indicators: {RSI, MACD, BB, SMA, EMA}
  - news_headlines: ["Apple earnings beat...", ...]
  - historical_data: {prices, volumes}
    ↓
llm_market_analyst.analyze(input)
    ↓
Generates Analysis Prompt
    ↓
┌──────────────────────────────────┐
│   Check Model Availability       │
├──────────────────────────────────┤
│ IF Ollama available:             │
│   → ollama.generate(prompt)      │
│                                  │
│ ELSE IF Ollama HTTP running:     │
│   → requests.post("/api/generate")
│                                  │
│ ELSE:                            │
│   → Use template-based response  │
└──────────────────────────────────┘
    ↓
Parse LLM Response
    ↓
Extract Trading Signals:
  - Direction: UP/DOWN
  - Signal: BUY/SELL/HOLD
  - Price Target
  - Stop Loss
  - Risk Level
    ↓
Return JSON Response to Frontend
    ↓
Dashboard displays:
  • Market Analysis Text
  • Trading Signal with confidence
  • Risk Assessment
  • Entry/Exit Points
```

---

## Environment Variables

Your system reads these for Ollama configuration:

```env
# In .env file or environment
LLM_BACKEND=ollama          # Which backend to use
OLLAMA_BASE_URL=http://localhost:11434  # Where Ollama runs
OLLAMA_MODEL=mistral        # Which model to download/use
```

### **Autodetection Priority**

If `LLM_BACKEND=auto`, system tries in order:

1. ✅ **Anthropic Claude** (if API key set)
2. ✅ **Ollama** (if running locally)
3. ✅ **HuggingFace** (if transformers lib available)
4. ✅ **Template** (fallback - always works)

---

## Real Example: Stock Analysis

### **Input to Ollama:**

```
STOCK ANALYSIS REQUEST:

Symbol: AAPL
Current Price: $150.50
Predicted Price: $155.00
Confidence: 87%

SENTIMENT ANALYSIS:
Positive Sentiment: 65%
Neutral: 25%
Negative: 10%

TECHNICAL INDICATORS:
RSI: 65 (Moderate Buy)
MACD: Positive (Bullish)
Bollinger Bands: Price near upper band
SMA 20: $149.00
EMA 12: $150.20
Volume Ratio: 1.2x (Above average)

RECENT NEWS HEADLINES:
- Apple Q1 earnings beat expectations
- New iPhone 16 pre-orders exceed projections
- Analyst upgrades Apple to "Outperform"

Please provide:
1. Market Analysis
2. Sentiment Impact
3. Trading Signal
4. Risk Assessment
5. Entry/Exit Points
```

### **Output from Ollama (mistral):**

```
Market Analysis:
Apple demonstrates strong technical strength with price near 20-day highs. 
The positive MACD crossover suggests continued upward momentum. Volume 
above average supports the bullish structure.

Sentiment Impact:
Overwhelmingly positive sentiment (65% positive, 10% negative) from recent 
earnings beat and iPhone pre-order strength. This supports higher valuations.

Trading Signal: BUY
- Entry Point: $150.50-$151.50
- Price Target: $155.00-$157.50
- Stop Loss: $147.50 (2% below entry)

Risk Assessment: MODERATE
- Key Risk: Tech sector rotation or broader market pullback
- Catalyst Risk: Mixed data on economic conditions
- Timeframe: 2-4 weeks

Recommendations:
1. Buy on any pullback to $149-$150
2. Target first resistance at $155
3. Use trailing stop at $149
4. Size position appropriately given market volatility
```

---

## Performance Characteristics

### **Ollama vs Alternatives**

| Feature | Ollama | HuggingFace | Anthropic |
|---------|--------|-------------|-----------|
| Speed | ⚡⚡⚡ (2-30s) | ⚡⚡ (10-60s) | ⚡ (API latency) |
| Cost | FREE | FREE | $$ |
| Privacy | ✅ Local | ✅ Local | ❌ Cloud |
| Quality | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Requires Internet | ❌ | ❌ | ✅ |
| Hardware | 8GB RAM | 16GB RAM | Any |
| Setup | Simple | Medium | API Key |

---

## What Happens When...

### **Ollama is NOT Running**

```
User requests market analysis
    ↓
System tries: ollama.generate() 
    ↗ FAILS (Connection refused)
    ↓
System tries: requests.post("http://localhost:11434/api/generate")
    ↗ FAILS (Connection timeout)
    ↓
System falls back: Template-based analysis
    ↓
Returns generic (but valid) trading signal
    └─ Based on technical indicators + sentiment only
    └─ No LLM-powered natural language insights
```

**User sees:** Standard analysis without LLM text

### **Ollama IS Running**

```
User requests market analysis
    ↓
System calls: ollama.generate(model="mistral", prompt=analysis_prompt)
    ↓
Ollama processes on local GPU/CPU
    ↓
Returns detailed market insights within 2-30 seconds
    ↓
System parses response
    ↓
User sees: Rich, AI-generated market analysis
```

**User sees:** Intelligent natural-language analysis

---

## Enabling Ollama in Your Project

### **Step 1: Download Ollama**
```
Visit: https://ollama.ai/download/windows
Run the installer
```

### **Step 2: Pull a Model**
```powershell
ollama pull mistral
```
Options:
- `ollama pull mistral` - Best balance (4.1GB, fast)
- `ollama pull neural-chat` - Conversation optimized
- `ollama pull llama2` - Meta's model
- `ollama pull orca-mini` - Lightweight (1.3GB)

### **Step 3: Start Ollama Server**
```powershell
ollama serve
```
Keep this terminal open while using the dashboard.

### **Step 4: Verify Installation**
```powershell
# In new PowerShell window:
ollama list
ollama run mistral "What is the stock market?"
```

### **Step 5: Your Dashboard Auto-Detects**
No configuration needed! Your system will:
- Detect Ollama running on localhost:11434
- Use mistral model by default
- Generate insights automatically

---

## Troubleshooting

### **"Model not found" Error in Logs**

**Cause:** Ollama model not downloaded  
**Solution:**
```powershell
ollama pull mistral
ollama list  # Verify it's there
ollama serve  # Restart Ollama
```

### **"Connection refused" (Port 11434)**

**Cause:** Ollama server not running  
**Solution:**
```powershell
# New PowerShell window:
ollama serve
```

### **Slow Responses (>30 seconds)**

**Cause:** Running on CPU only  
**Solution:**
1. Use smaller model: `ollama pull neural-chat:7b-quantized`
2. Enable GPU (NVIDIA/AMD setup)
3. Close other applications

### **High Memory Usage**

**Cause:** Model loading into RAM  
**Solution:** Use smaller model or quantized versions

---

## Summary

**Ollama is an intelligent LLM that runs locally on your machine and powers your market analysis with natural-language insights. It's completely optional - if not running, the system still works with template-based analysis.**

```
Ollama = Your personal AI analyst running locally for $0
```
