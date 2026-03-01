"""
AI Market Predictor - Simple PDF Generator
Creates a professional PDF presentation
"""

from fpdf import FPDF
import datetime

class Presentation(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(102, 126, 234)
            self.cell(0, 10, 'AI Market Predictor', align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(2)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# Create PDF
pdf = Presentation()
pdf.set_auto_page_break(auto=True, margin=15)

# Title Page
pdf.add_page()
pdf.set_font('Helvetica', 'B', 32)
pdf.set_text_color(102, 126, 234)
pdf.ln(80)
pdf.cell(0, 15, 'AI Market Predictor', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.set_font('Helvetica', 'I', 16)
pdf.set_text_color(118, 75, 162)
pdf.cell(0, 10, 'Advanced Transformer-based Stock Prediction System', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)

pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, 'Deep Learning for Indian Stock Market', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)

pdf.set_font('Helvetica', 'I', 9)
pdf.set_text_color(128, 128, 128)
pdf.cell(0, 6, f'Generated: {datetime.datetime.now().strftime("%B %d, %Y")}', align='C', new_x="LMARGIN", new_y="NEXT")

# Project Overview
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '1. Project Overview', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'What is it?', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, '- Real-time stock price prediction using AI\n- Predicts prices for 20+ Indian companies\n- Web-based interface with live predictions\n- Currency: Indian Rupees (INR)')
pdf.ln(3)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Key Features', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, '- Advanced Transformer Neural Network\n- 26 Technical Indicators\n- Real Company Logos\n- Interactive Web Interface\n- Live Prediction Mode\n- Color-coded Trend Analysis')

# Technology Stack
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '2. Technology Stack', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Backend', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, 'Python 3.10, PyTorch 2.9.1, FastAPI, yfinance')
pdf.ln(3)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Frontend', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, 'HTML5, CSS3, JavaScript, Chart.js')
pdf.ln(3)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Deployment', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, 'LocalTunnel (Public URLs), Docker Ready')

# AI Model
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '3. AI Model Architecture', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Transformer Model', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Courier', '', 9)
pdf.set_fill_color(245, 245, 245)
pdf.multi_cell(0, 5, 'Input (26 features) -> Positional Encoding ->\nMulti-Head Attention (8 heads) ->\nFeed-Forward (3 layers) -> Output', fill=True)
pdf.ln(5)

pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, 'Model Dim: 128 | Heads: 8 | Layers: 3 | Params: ~100K')

# Companies
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '4. Companies Covered (20)', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

companies = [
    ('Top Performers', 'Reliance, TCS, Infosys, HDFC, L&T'),
    ('Declining Stocks', 'Tata Steel, Vedanta, Zee, Yes Bank, Adani Ports'),
    ('Growth Leaders', 'Bajaj Finance, Asian Paints, Maruti, HUL, Wipro'),
    ('Mixed Performance', 'ICICI, SBI, Airtel, ITC, Tata Motors')
]

for title, comps in companies:
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, comps)
    pdf.ln(2)

# Features
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '5. Key Features', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

features = [
    ('26 Technical Indicators', 'SMA, EMA, RSI, MACD, Bollinger Bands, ATR'),
    ('Smart Predictions', 'Bullish: +2-8% | Bearish: -3-7% | Mixed: Variable'),
    ('Web Interface', 'Real logos, Live mode, Interactive charts'),
    ('API Endpoints', '9 REST endpoints with OpenAPI docs'),
    ('Currency', 'Smart INR conversion for Indian stocks')
]

for title, desc in features:
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 5, desc)
    pdf.ln(2)

# Deployment
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '6. Deployment', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 7, 'Local Development', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Courier', '', 9)
pdf.multi_cell(0, 5, 'API: localhost:8000\nFrontend: localhost:3000')
pdf.ln(3)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 7, 'Public URLs', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Courier', '', 8)
pdf.multi_cell(0, 5, 'Frontend: https://pretty-mirrors-refuse.loca.lt\nAPI: https://vast-pants-search.loca.lt')

# Use Cases
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '7. Use Cases', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

use_cases = [
    'Retail Investors: Quick predictions, trend analysis',
    'Financial Analysts: Market research, stock screening',
    'Students & Researchers: AI/ML learning, projects',
    'Day Traders: Short-term predictions, live monitoring'
]

pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
for uc in use_cases:
    pdf.multi_cell(0, 6, f'- {uc}')
    pdf.ln(1)

# Achievements
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '8. Key Achievements', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

achievements = [
    'Built advanced Transformer model from scratch',
    'Implemented 26 technical indicators',
    'Created full-stack web application',
    'Deployed with public URL access',
    'Real company logos integration',
    'Live auto-refresh predictions',
    'Dynamic color-coded charts'
]

pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
for ach in achievements:
    pdf.cell(0, 6, f'- {ach}', new_x="LMARGIN", new_y="NEXT")

# Future Enhancements
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '9. Future Enhancements', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 7, 'Short Term', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 5, 'Add 50+ companies, Historical charts, Multiple stock comparison,\nPerformance metrics, User authentication')
pdf.ln(3)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 7, 'Long Term', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 5, 'Portfolio optimization, Risk analysis, News sentiment,\nMobile app, Real-time trading signals')

# Conclusion
pdf.add_page()
pdf.set_font('Helvetica', 'B', 18)
pdf.set_fill_color(102, 126, 234)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 12, '10. Conclusion', fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 7, 'Successfully built a complete AI-powered stock market prediction system featuring advanced Transformer architecture, 20 Indian companies, real-time predictions, professional web interface, and public deployment.')
pdf.ln(10)

pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, 'Learning Outcomes', new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font('Helvetica', '', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, '- Deep Learning (PyTorch)\n- REST API Development (FastAPI)\n- Web Development\n- Financial Analysis\n- Cloud Deployment')
pdf.ln(20)

pdf.set_font('Helvetica', 'B', 24)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 12, 'Thank You!', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Helvetica', 'I', 14)
pdf.cell(0, 8, 'Questions?', align='C', new_x="LMARGIN", new_y="NEXT")

# Save
pdf.output('AI_Market_Predictor_Presentation.pdf')
print('✅ PDF Generated: AI_Market_Predictor_Presentation.pdf')
print(f'📄 Total Pages: {pdf.page_no()}')
print('📊 Ready to present!')
