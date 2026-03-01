"""
Web API Client - Interactive API Testing UI
Serves a web-based interface for testing all API endpoints
"""

from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

# Create router for web client
web_router = APIRouter(prefix="/web", tags=["Web Interface"])


@web_router.get("/client", response_class=HTMLResponse)
async def api_client():
    """Serve interactive API client"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>AI Market Predictor - API Client</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { opacity: 0.9; font-size: 1.1em; }
            .content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0;
            }
            .panel {
                padding: 30px;
                border-right: 1px solid #eee;
            }
            .panel:last-child { border-right: none; }
            .section {
                margin-bottom: 30px;
            }
            .section h3 {
                color: #333;
                margin-bottom: 15px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-weight: 500;
            }
            input, textarea, select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-family: inherit;
                font-size: 1em;
            }
            input:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 1em;
                font-weight: 600;
                transition: all 0.3s;
                width: 100%;
            }
            button:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .response {
                background: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 15px;
                margin-top: 15px;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-family: 'Courier New', monospace;
                max-height: 500px;
                overflow-y: auto;
                font-size: 0.9em;
            }
            .response.success {
                color: #27ae60;
                border-color: #27ae60;
                background: #d5f4e6;
            }
            .response.error {
                color: #e74c3c;
                border-color: #e74c3c;
                background: #fadbd8;
            }
            .tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                border-bottom: 2px solid #eee;
            }
            .tab-btn {
                padding: 10px 20px;
                background: none;
                border: none;
                cursor: pointer;
                color: #666;
                font-weight: 600;
                border-bottom: 3px solid transparent;
                transition: all 0.3s;
                width: auto;
            }
            .tab-btn.active {
                color: #667eea;
                border-bottom-color: #667eea;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
            .status {
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 15px;
                text-align: center;
                color: white;
            }
            .status.healthy {
                background: #27ae60;
            }
            .status.unhealthy {
                background: #e74c3c;
            }
            .status.checking {
                background: #f39c12;
            }
            .separator { border-top: 1px solid #eee; margin: 20px 0; }
            @media (max-width: 1024px) {
                .content { grid-template-columns: 1fr; }
                .panel { border-right: none; border-bottom: 1px solid #eee; }
                .panel:last-child { border-bottom: none; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>API Market Predictor</h1>
                <p>Interactive REST API Client</p>
            </div>
            
            <div class="content">
                <!-- Left Panel -->
                <div class="panel">
                    <div id="status" class="status checking">Checking server...</div>
                    
                    <div class="tabs">
                        <button class="tab-btn active" onclick="switchTab('analyze')">Analyze</button>
                        <button class="tab-btn" onclick="switchTab('chat')">Chat</button>
                        <button class="tab-btn" onclick="switchTab('alerts')">Alerts</button>
                        <button class="tab-btn" onclick="switchTab('summary')">Summary</button>
                    </div>
                    
                    <!-- Analyze Tab -->
                    <div id="analyze" class="tab-content active">
                        <div class="section">
                            <h3>Stock Analysis</h3>
                            <div class="form-group">
                                <label>Stock Symbol:</label>
                                <input type="text" id="symbol" placeholder="e.g., AAPL" value="AAPL">
                            </div>
                            <div class="form-group">
                                <label>Current Price:</label>
                                <input type="number" id="current_price" placeholder="e.g., 150.75" value="150.75" step="0.01">
                            </div>
                            <div class="form-group">
                                <label>Predicted Price:</label>
                                <input type="number" id="predicted_price" placeholder="e.g., 158.50" value="158.50" step="0.01">
                            </div>
                            <div class="form-group">
                                <label>Confidence (0-1):</label>
                                <input type="number" id="confidence" placeholder="e.g., 0.82" value="0.82" min="0" max="1" step="0.01">
                            </div>
                            <button onclick="analyzeStock()">Analyze Stock</button>
                        </div>
                    </div>
                    
                    <!-- Chat Tab -->
                    <div id="chat" class="tab-content">
                        <div class="section">
                            <h3>Chat with AI</h3>
                            <div class="form-group">
                                <label>Message:</label>
                                <textarea id="message" placeholder="Ask anything about the market..." rows="4">What's the market outlook?</textarea>
                            </div>
                            <button onclick="chatWithAI()">Send Message</button>
                        </div>
                    </div>
                    
                    <!-- Alerts Tab -->
                    <div id="alerts" class="tab-content">
                        <div class="section">
                            <h3>Trading Alerts</h3>
                            <div class="form-group">
                                <label>Symbols (comma-separated):</label>
                                <textarea id="symbols" placeholder="e.g., AAPL, MSFT, GOOGL" rows="3">AAPL,MSFT,GOOGL</textarea>
                            </div>
                            <button onclick="getAlerts()">Get Alerts</button>
                        </div>
                    </div>
                    
                    <!-- Summary Tab -->
                    <div id="summary" class="tab-content">
                        <div class="section">
                            <h3>Market Summary</h3>
                            <div class="form-group">
                                <label>Symbols (comma-separated):</label>
                                <textarea id="summary_symbols" placeholder="e.g., AAPL, MSFT, GOOGL" rows="3">AAPL,MSFT,GOOGL</textarea>
                            </div>
                            <button onclick="getMarketSummary()">Get Summary</button>
                        </div>
                    </div>
                </div>
                
                <!-- Right Panel -->
                <div class="panel">
                    <div class="section">
                        <h3>Response</h3>
                        <div id="response" class="response">Ready to send requests...</div>
                    </div>
                    
                    <div class="separator"></div>
                    
                    <div class="section">
                        <h3>System Info</h3>
                        <button onclick="getSystemInfo()">Get System Info</button>
                        <div id="info" style="margin-top: 15px; font-size: 0.9em;"></div>
                    </div>
                    
                    <div class="separator"></div>
                    
                    <div class="section">
                        <h3>Quick Commands</h3>
                        <button onclick="healthCheck()">Health Check</button>
                        <button onclick="getPerformance()" style="margin-top: 10px;">Performance Metrics</button>
                        <button onclick="getHistory()" style="margin-top: 10px;">Chat History</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Auto-detect API server (same host and port)
            const API_BASE = window.location.origin;
            
            // Tab switching
            function switchTab(tabName) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }
            
            // API calls
            async function makeRequest(endpoint, method = 'GET', data = null) {
                try {
                    const options = {
                        method: method,
                        headers: {'Content-Type': 'application/json'}
                    };
                    if (data) options.body = JSON.stringify(data);
                    
                    const response = await fetch(`${API_BASE}${endpoint}`, options);
                    const result = await response.json();
                    
                    showResponse(result, response.ok);
                    return result;
                } catch (error) {
                    showResponse({error: error.message}, false);
                }
            }
            
            async function analyzeStock() {
                const data = {
                    symbol: document.getElementById('symbol').value,
                    current_price: parseFloat(document.getElementById('current_price').value),
                    predicted_price: parseFloat(document.getElementById('predicted_price').value),
                    confidence: parseFloat(document.getElementById('confidence').value)
                };
                await makeRequest('/api/ai/analyze', 'POST', data);
            }
            
            async function chatWithAI() {
                const data = {message: document.getElementById('message').value};
                await makeRequest('/api/ai/chat', 'POST', data);
            }
            
            async function getAlerts() {
                const symbols = document.getElementById('symbols').value
                    .split(',').map(s => s.trim());
                const params = new URLSearchParams();
                symbols.forEach(s => params.append('symbols', s));
                await makeRequest(`/api/ai/alerts?${params}`);
            }
            
            async function getMarketSummary() {
                const symbols = document.getElementById('summary_symbols').value
                    .split(',').map(s => s.trim());
                const data = {symbols: symbols};
                await makeRequest('/api/ai/market-summary', 'POST', data);
            }
            
            async function getSystemInfo() {
                const result = await makeRequest('/api/ai/info');
                if (result) {
                    document.getElementById('info').textContent = 
                        'Version: ' + result.version + '\\n' +
                        'Components: ' + Object.keys(result.components).length;
                }
            }
            
            async function healthCheck() {
                await makeRequest('/api/ai/health');
            }
            
            async function getPerformance() {
                await makeRequest('/api/ai/performance');
            }
            
            async function getHistory() {
                await makeRequest('/api/ai/conversation-history?limit=10');
            }
            
            function showResponse(data, success) {
                const elem = document.getElementById('response');
                elem.textContent = JSON.stringify(data, null, 2);
                elem.className = 'response ' + (success ? 'success' : 'error');
            }
            
            // Check health on load
            window.onload = async () => {
                const statusElem = document.getElementById('status');
                try {
                    const response = await fetch(`${API_BASE}/api/ai/health`);
                    if (response.ok) {
                        statusElem.textContent = '✓ Server Healthy';
                        statusElem.className = 'status healthy';
                    } else {
                        statusElem.textContent = '✗ Server Error';
                        statusElem.className = 'status unhealthy';
                    }
                } catch (e) {
                    statusElem.textContent = '✗ Cannot connect to server';
                    statusElem.className = 'status unhealthy';
                }
            };
        </script>
    </body>
    </html>
    """


@web_router.get("/swagger", response_class=HTMLResponse)
async def swagger_ui():
    """Serve Swagger UI documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #333; }
            .endpoint { 
                background: #f9f9f9; 
                padding: 15px; 
                margin: 15px 0; 
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                margin-right: 10px;
            }
            .post { background: #f39c12; }
            .get { background: #3498db; }
            code { background: #eee; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>API Documentation</h1>
            
            <h2>Analysis Endpoints</h2>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/ai/analyze</code>
                <p>Analyze a stock and get trading signals</p>
                <p><strong>Body:</strong> {symbol, current_price, predicted_price, confidence}</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/analyze/{symbol}</code>
                <p>Get cached analysis for a symbol</p>
            </div>
            
            <h2>Chat Endpoints</h2>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/ai/chat</code>
                <p>Chat with AI analyst</p>
                <p><strong>Body:</strong> {message}</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/conversation-history</code>
                <p>Get conversation history</p>
            </div>
            
            <h2>Market Endpoints</h2>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/ai/market-summary</code>
                <p>Get market summary</p>
                <p><strong>Body:</strong> {symbols: []}</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/alerts</code>
                <p>Get trading alerts</p>
                <p><strong>Query:</strong> ?symbols=AAPL&symbols=MSFT</p>
            </div>
            
            <h2>System Endpoints</h2>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/health</code>
                <p>System health check</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/info</code>
                <p>System information</p>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span> <code>/api/ai/performance</code>
                <p>Performance metrics</p>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span> <code>/api/ai/export</code>
                <p>Export analysis data</p>
            </div>
        </div>
    </body>
    </html>
    """


__all__ = ["web_router"]
