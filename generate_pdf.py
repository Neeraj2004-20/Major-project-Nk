"""
AI Market Predictor - PDF Presentation Generator
Generates a professional PDF presentation from the project
"""

from fpdf import FPDF
import datetime

class PDFPresentation(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Arial', 'B', 10)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, 'AI Market Predictor - Advanced Stock Prediction System', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(102, 126, 234)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, title, 0, 1, 'L', 1)
        self.ln(4)
        
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
        
    def body_text(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(2)
        
    def bullet_point(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.cell(10, 6, '>', 0, 0)
        self.multi_cell(0, 6, text)
        
    def code_block(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 5, text, 0, 'L', 1)
        self.ln(2)

# Create PDF
pdf = PDFPresentation()
pdf.add_page()

# Title Page
pdf.set_font('Arial', 'B', 32)
pdf.set_text_color(102, 126, 234)
pdf.ln(60)
pdf.cell(0, 20, 'AI Market Predictor', 0, 1, 'C')

pdf.set_font('Arial', 'I', 18)
pdf.set_text_color(118, 75, 162)
pdf.cell(0, 10, 'Advanced Transformer-based Stock Prediction', 0, 1, 'C')

pdf.ln(20)
pdf.set_font('Arial', '', 14)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, 'Deep Learning System for Indian Stock Market', 0, 1, 'C')

pdf.ln(40)
pdf.set_font('Arial', 'I', 10)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 6, f'Generated on: {datetime.datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')

# Slide 2: Project Overview
pdf.add_page()
pdf.chapter_title('1. Project Overview')
pdf.section_title('What is it?')
pdf.bullet_point('Real-time stock price prediction system using AI')
pdf.bullet_point('Predicts future prices for 20+ Indian companies')
pdf.bullet_point('Web-based interface with live predictions')
pdf.bullet_point('Currency: Indian Rupees (INR)')
pdf.ln(5)

pdf.section_title('Key Features')
pdf.bullet_point('Advanced Transformer Neural Network')
pdf.bullet_point('26 Technical Indicators')
pdf.bullet_point('Real Company Logos')
pdf.bullet_point('Interactive Web Interface')
pdf.bullet_point('Live Prediction Mode')
pdf.bullet_point('Color-coded Trend Analysis')

# Slide 3: Technology Stack
pdf.add_page()
pdf.chapter_title('2. Technology Stack')
pdf.section_title('Backend')
pdf.bullet_point('Python 3.10 - Core language')
pdf.bullet_point('PyTorch 2.9.1 - Deep learning framework')
pdf.bullet_point('FastAPI - REST API framework')
pdf.bullet_point('yfinance - Real-time stock data')
pdf.ln(5)

pdf.section_title('Frontend')
pdf.bullet_point('HTML5/CSS3/JavaScript')
pdf.bullet_point('Chart.js - Data visualization')
pdf.bullet_point('Responsive Design - Mobile-friendly')
pdf.ln(5)

pdf.section_title('Deployment')
pdf.bullet_point('LocalTunnel - Public URL access')
pdf.bullet_point('Docker - Containerization ready')

# Slide 4: AI Model Architecture
pdf.add_page()
pdf.chapter_title('3. AI Model Architecture')
pdf.section_title('Advanced Transformer Model')
pdf.code_block('''Input Layer (26 features)
    |
Positional Encoding
    |
Multi-Head Attention (8 heads)
    |
Feed-Forward Network (3 layers)
    |
Output Layer (Price Prediction)''')

pdf.ln(5)
pdf.section_title('Model Specifications')
pdf.bullet_point('Model Dimension: 128')
pdf.bullet_point('Attention Heads: 8')
pdf.bullet_point('Transformer Layers: 3')
pdf.bullet_point('Sequence Length: 30 days')
pdf.bullet_point('Total Parameters: ~100K')

# Slide 5: Technical Indicators
pdf.add_page()
pdf.chapter_title('4. Technical Indicators (26 Features)')
pdf.section_title('Moving Averages')
pdf.bullet_point('SMA (5, 10, 20 days)')
pdf.bullet_point('EMA (12, 26 days)')
pdf.ln(3)

pdf.section_title('Momentum Indicators')
pdf.bullet_point('RSI (Relative Strength Index)')
pdf.bullet_point('MACD (Moving Average Convergence Divergence)')
pdf.bullet_point('Momentum & Rate of Change')
pdf.ln(3)

pdf.section_title('Volatility Indicators')
pdf.bullet_point('Bollinger Bands (Upper, Middle, Lower)')
pdf.bullet_point('ATR (Average True Range)')
pdf.bullet_point('Standard Deviation')
pdf.ln(3)

pdf.section_title('Volume Analysis')
pdf.bullet_point('Volume Ratio')
pdf.bullet_point('On-Balance Volume')

# Slide 6: Training Process
pdf.add_page()
pdf.chapter_title('5. Training Process')
pdf.section_title('Data Collection')
pdf.bullet_point('Historical data from Yahoo Finance')
pdf.bullet_point('1 year of daily stock prices')
pdf.bullet_point('NSE (National Stock Exchange) listed companies')
pdf.ln(5)

pdf.section_title('Training Configuration')
pdf.bullet_point('Optimizer: AdamW')
pdf.bullet_point('Learning Rate: 0.001 (adaptive)')
pdf.bullet_point('Batch Size: 32')
pdf.bullet_point('Epochs: 50 (with early stopping)')
pdf.bullet_point('Loss Function: MSE (Mean Squared Error)')
pdf.ln(5)

pdf.section_title('Advanced Techniques')
pdf.bullet_point('Early Stopping (patience: 20)')
pdf.bullet_point('Learning Rate Scheduling')
pdf.bullet_point('Gradient Clipping')
pdf.bullet_point('Dropout Regularization')

# Slide 7: Companies Covered
pdf.add_page()
pdf.chapter_title('6. Companies Covered (20 Total)')
pdf.section_title('Top Performers (Bullish)')
pdf.body_text('Reliance Industries, TCS, Infosys, HDFC Bank, L&T')
pdf.ln(3)

pdf.section_title('Declining Stocks (Bearish)')
pdf.body_text('Tata Steel, Vedanta, Zee Entertainment, Yes Bank, Adani Ports')
pdf.ln(3)

pdf.section_title('Growth Leaders (Strong Buy)')
pdf.body_text('Bajaj Finance, Asian Paints, Maruti Suzuki, HUL, Wipro')
pdf.ln(3)

pdf.section_title('Mixed Performance (Volatile)')
pdf.body_text('ICICI Bank, SBI, Bharti Airtel, ITC Limited, Tata Motors')

# Slide 8: Web Interface
pdf.add_page()
pdf.chapter_title('7. Web Interface Features')
pdf.section_title('User-Friendly Design')
pdf.bullet_point('Company Dropdown - Categorized by performance')
pdf.bullet_point('Real Logos - Professional company branding')
pdf.bullet_point('Prediction Periods - 1 to 365 days')
pdf.bullet_point('Live Mode - Auto-refresh every 30 seconds')
pdf.bullet_point('Interactive Charts - Smooth prediction curves')
pdf.ln(5)

pdf.section_title('Visual Intelligence')
pdf.bullet_point('Green Charts - Positive/Upward trends')
pdf.bullet_point('Red Charts - Negative/Downward trends')
pdf.bullet_point('Gradient Fills - Visual depth')
pdf.bullet_point('Smooth Curves - 11-point interpolation')

# Slide 9: API Architecture
pdf.add_page()
pdf.chapter_title('8. API Architecture')
pdf.section_title('REST API Endpoints (9 Total)')
pdf.bullet_point('POST /predict/live - Get stock prediction')
pdf.bullet_point('GET /health - System health check')
pdf.bullet_point('GET /model/info - Model specifications')
pdf.bullet_point('GET /experiments - Training history')
pdf.bullet_point('GET /attention - Attention visualization')
pdf.bullet_point('GET /docs - OpenAPI documentation')
pdf.ln(5)

pdf.section_title('API Features')
pdf.bullet_point('CORS enabled for cross-origin requests')
pdf.bullet_point('JSON request/response format')
pdf.bullet_point('Smart INR currency conversion')
pdf.bullet_point('Error handling & validation')

# Slide 10: Prediction Logic
pdf.add_page()
pdf.chapter_title('9. Smart Prediction Logic')
pdf.section_title('Category-Based Trends')
pdf.bullet_point('Bullish Stocks: 2-8% predicted gains')
pdf.bullet_point('Bearish Stocks: 3-7% predicted losses')
pdf.bullet_point('Mixed Stocks: Variable predictions')
pdf.ln(5)

pdf.section_title('Currency Intelligence')
pdf.code_block('''if stock.endswith('.NS') or stock.endswith('.BO'):
    # Indian stock - already in INR
    price_inr = current_price
else:
    # US stock - convert USD to INR
    price_inr = current_price * 83.0''')

# Slide 11: Deployment
pdf.add_page()
pdf.chapter_title('10. Deployment Architecture')
pdf.section_title('Local Development')
pdf.code_block('''API Server: Port 8000
Frontend: Port 3000''')
pdf.ln(5)

pdf.section_title('Public Deployment (LocalTunnel)')
pdf.code_block('''Frontend: https://pretty-mirrors-refuse.loca.lt
API: https://vast-pants-search.loca.lt''')
pdf.ln(5)

pdf.section_title('Production Ready')
pdf.bullet_point('Docker containerization')
pdf.bullet_point('Nginx reverse proxy')
pdf.bullet_point('PostgreSQL database')
pdf.bullet_point('Redis caching')

# Slide 12: Project Structure
pdf.add_page()
pdf.chapter_title('11. Project Structure')
pdf.code_block('''market-predictor-ai/
├── model.py              # Transformer architecture
├── train.py              # Training pipeline
├── serve.py              # FastAPI server
├── data_loader.py        # Data processing
├── frontend.html         # Web interface
├── serve_frontend.py     # Frontend server
├── main.py               # CLI interface
├── hyperparameter_search.py
├── requirements.txt      # Dependencies
├── Dockerfile           # Container config
├── outputs/             # Trained models
└── logs/                # Training logs''')

# Slide 13: Achievements
pdf.add_page()
pdf.chapter_title('12. Key Achievements')
pdf.section_title('Technical Accomplishments')
pdf.bullet_point('Built advanced Transformer model from scratch')
pdf.bullet_point('Implemented 26 technical indicators')
pdf.bullet_point('Created full-stack web application')
pdf.bullet_point('Deployed with public URL access')
pdf.bullet_point('Real-time data integration')
pdf.ln(5)

pdf.section_title('Features Delivered')
pdf.bullet_point('20 Indian companies coverage')
pdf.bullet_point('Real company logos integration')
pdf.bullet_point('Live auto-refresh predictions')
pdf.bullet_point('Dynamic color-coded charts')
pdf.bullet_point('Category-based organization')

# Slide 14: Future Enhancements
pdf.add_page()
pdf.chapter_title('13. Future Enhancements')
pdf.section_title('Short Term')
pdf.bullet_point('Add more Indian companies (50+)')
pdf.bullet_point('Historical comparison charts')
pdf.bullet_point('Multiple stock comparison')
pdf.bullet_point('Performance metrics dashboard')
pdf.bullet_point('User authentication')
pdf.ln(5)

pdf.section_title('Long Term')
pdf.bullet_point('Portfolio optimization')
pdf.bullet_point('Risk analysis')
pdf.bullet_point('News sentiment integration')
pdf.bullet_point('Mobile app (React Native)')
pdf.bullet_point('Real-time trading signals')

# Slide 15: Use Cases
pdf.add_page()
pdf.chapter_title('14. Use Cases')
pdf.section_title('1. Retail Investors')
pdf.body_text('Quick price predictions, trend analysis, investment decisions')
pdf.ln(3)

pdf.section_title('2. Financial Analysts')
pdf.body_text('Market research, stock screening, pattern recognition')
pdf.ln(3)

pdf.section_title('3. Students & Researchers')
pdf.body_text('AI/ML learning, financial modeling, academic projects')
pdf.ln(3)

pdf.section_title('4. Day Traders')
pdf.body_text('Short-term predictions, live monitoring, quick insights')

# Slide 16: Advantages
pdf.add_page()
pdf.chapter_title('15. Why This System?')
pdf.bullet_point('AI-Powered - Deep learning predictions')
pdf.bullet_point('Real-Time - Live market data')
pdf.bullet_point('User-Friendly - Simple interface')
pdf.bullet_point('Visual - Interactive charts')
pdf.bullet_point('Comprehensive - 26 indicators')
pdf.bullet_point('Free - No subscription needed')
pdf.bullet_point('Indian Market - NSE-focused')
pdf.ln(5)

pdf.section_title('Competitive Edge')
pdf.bullet_point('Transformer model (state-of-art)')
pdf.bullet_point('Real company logos')
pdf.bullet_point('Live prediction mode')
pdf.bullet_point('Category-based insights')

# Slide 17: Technical Highlights
pdf.add_page()
pdf.chapter_title('16. Technical Highlights')
pdf.section_title('Code Quality')
pdf.bullet_point('Modular architecture')
pdf.bullet_point('Type hints & documentation')
pdf.bullet_point('Error handling')
pdf.bullet_point('Logging system')
pdf.ln(5)

pdf.section_title('Performance')
pdf.bullet_point('Fast inference (<1 second)')
pdf.bullet_point('Efficient data loading')
pdf.bullet_point('Optimized model size')
pdf.bullet_point('Responsive UI')
pdf.ln(5)

pdf.section_title('Scalability')
pdf.bullet_point('Docker ready')
pdf.bullet_point('API-first design')
pdf.bullet_point('Horizontal scaling support')

# Conclusion
pdf.add_page()
pdf.chapter_title('17. Conclusion')
pdf.section_title('Project Summary')
pdf.body_text('Built a complete AI-powered stock market prediction system with advanced Transformer neural network, 20 Indian companies, real-time predictions, professional web interface, and public deployment.')
pdf.ln(5)

pdf.section_title('Learning Outcomes')
pdf.bullet_point('Deep Learning (PyTorch)')
pdf.bullet_point('REST API Development (FastAPI)')
pdf.bullet_point('Web Development (HTML/CSS/JS)')
pdf.bullet_point('Financial Analysis')
pdf.bullet_point('Cloud Deployment')
pdf.ln(10)

pdf.set_font('Arial', 'B', 20)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 10, 'Thank You!', 0, 1, 'C')
pdf.ln(5)
pdf.set_font('Arial', 'I', 14)
pdf.cell(0, 8, 'Questions?', 0, 1, 'C')

# Save PDF
output_file = 'AI_Market_Predictor_Presentation.pdf'
pdf.output(output_file)
print(f'✅ PDF Generated Successfully: {output_file}')
print(f'📄 Total Pages: {pdf.page_no()}')
print(f'📊 Presentation ready for viewing!')
