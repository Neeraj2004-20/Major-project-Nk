"""
AI Market Prediction Report Generator
Creates professional PDF reports with all AI insights
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import Dict, List, Optional
import io
import os

class PDFReportGenerator:
    """
    Generates professional PDF reports for market predictions
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Alert box
        self.styles.add(ParagraphStyle(
            name='AlertBox',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#dc3545'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12
        ))
    
    def generate_prediction_report(
        self,
        symbol: str,
        company_name: str,
        current_price: float,
        predicted_price: float,
        prediction_data: Dict,
        output_path: str = "reports/prediction_report.pdf"
    ) -> str:
        """
        Generate a comprehensive prediction report
        
        Args:
            symbol: Stock symbol
            company_name: Company name
            current_price: Current price
            predicted_price: Predicted price
            prediction_data: All prediction data including explanations, scenarios, etc.
            output_path: Where to save the PDF
            
        Returns:
            Path to generated PDF
        """
        
        # Create reports directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else 'reports', exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        story = []
        
        # Add title
        title = Paragraph(
            f"AI Market Prediction Report<br/>{company_name} ({symbol})",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Add report metadata
        meta_data = [
            ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Report Type:', 'AI-Powered Market Analysis'],
            ['Prediction Engine:', 'Advanced Transformer Neural Network']
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add prediction summary
        story.append(Paragraph("📊 Prediction Summary", self.styles['CustomHeading']))
        
        change_pct = ((predicted_price - current_price) / current_price) * 100
        direction = "BULLISH 📈" if change_pct > 0 else "BEARISH 📉"
        
        summary_data = [
            ['Current Price:', f'₹{current_price:,.2f}'],
            ['Predicted Price:', f'₹{predicted_price:,.2f}'],
            ['Expected Change:', f'{change_pct:+.2f}%'],
            ['Direction:', direction],
            ['Confidence:', f"{prediction_data.get('confidence', 0.75)*100:.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('FONT', (1, 2), (1, 2), 'Helvetica-Bold', 12),
            ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#28a745' if change_pct > 0 else '#dc3545')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Add AI explanation if available
        if 'explanation' in prediction_data:
            story.append(Paragraph("🧠 AI Explanation", self.styles['CustomHeading']))
            
            exp = prediction_data['explanation']
            explanation_text = exp.get('summary', 'No explanation available.')
            
            story.append(Paragraph(explanation_text.replace('\n', '<br/>'), self.styles['CustomBody']))
            story.append(Spacer(1, 0.2*inch))
            
            # Key factors
            if 'key_factors' in exp and exp['key_factors']:
                story.append(Paragraph("🔑 Key Driving Factors", self.styles['CustomSubHeading']))
                for factor in exp['key_factors']:
                    story.append(Paragraph(f"• {factor}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.2*inch))
            
            # Risk assessment
            risk_color = '#dc3545' if 'HIGH' in exp.get('risk_level', '') else '#ffc107' if 'MODERATE' in exp.get('risk_level', '') else '#28a745'
            risk_text = f"<font color='{risk_color}'><b>Risk Level: {exp.get('risk_level', 'N/A')}</b></font>"
            story.append(Paragraph(risk_text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.3*inch))
        
        # Add market health if available
        if 'market_health' in prediction_data:
            story.append(Paragraph("🚨 Market Health Analysis", self.styles['CustomHeading']))
            
            health = prediction_data['market_health']
            health_score = health.get('health_score', 0)
            condition = health.get('condition', 'UNKNOWN')
            
            health_data = [
                ['Health Score:', f"{health_score}/100"],
                ['Market Condition:', condition],
                ['Status:', health.get('description', 'N/A')]
            ]
            
            health_table = Table(health_data, colWidths=[2*inch, 4*inch])
            health_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107')),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(health_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Anomalies
            anomalies = health.get('anomaly_analysis', {}).get('anomalies', [])
            if anomalies:
                story.append(Paragraph("⚠️ Detected Anomalies:", self.styles['CustomSubHeading']))
                for anomaly in anomalies[:5]:  # Top 5
                    story.append(Paragraph(
                        f"<b>{anomaly.get('description', 'Unknown anomaly')}</b><br/>"
                        f"<i>{anomaly.get('impact', '')}</i>",
                        self.styles['CustomBody']
                    ))
            story.append(Spacer(1, 0.3*inch))
        
        # Add risk scenarios
        if 'risk_scenarios' in prediction_data:
            story.append(PageBreak())
            story.append(Paragraph("📊 Risk Scenarios Analysis", self.styles['CustomHeading']))
            story.append(Paragraph(
                "The AI has generated multiple potential outcomes based on different market conditions:",
                self.styles['CustomBody']
            ))
            story.append(Spacer(1, 0.2*inch))
            
            scenarios = prediction_data['risk_scenarios']
            for scenario in scenarios:
                # Scenario name
                story.append(Paragraph(scenario['name'], self.styles['CustomSubHeading']))
                
                # Scenario details
                scenario_data = [
                    ['Probability:', scenario['probability']],
                    ['Target Price:', f"₹{scenario['target_price']:,.2f}"],
                    ['Expected Change:', f"{scenario['change_pct']:+.2f}%"],
                    ['Timeframe:', scenario['timeframe']]
                ]
                
                scenario_table = Table(scenario_data, colWidths=[1.5*inch, 4.5*inch])
                scenario_table.setStyle(TableStyle([
                    ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                story.append(scenario_table)
                story.append(Spacer(1, 0.1*inch))
                
                # Conditions
                story.append(Paragraph("<b>Conditions:</b>", self.styles['CustomBody']))
                for condition in scenario.get('conditions', [])[:3]:
                    story.append(Paragraph(f"• {condition}", self.styles['CustomBody']))
                
                # Actions
                story.append(Paragraph("<b>Recommended Actions:</b>", self.styles['CustomBody']))
                for action in scenario.get('actions', [])[:2]:
                    story.append(Paragraph(f"✓ {action}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 0.2*inch))
        
        # Add disclaimer
        story.append(PageBreak())
        story.append(Paragraph("⚠️ Important Disclaimer", self.styles['CustomHeading']))
        disclaimer = """
        This report is generated by an AI-powered market prediction system for educational and informational 
        purposes only. It should NOT be considered as financial advice or a recommendation to buy or sell 
        any securities. Stock markets are inherently volatile and unpredictable. Past performance does not 
        guarantee future results.
        <br/><br/>
        The predictions, explanations, and scenarios provided in this report are based on historical data 
        and mathematical models, which may not account for all market factors, unexpected events, or changes 
        in market conditions. Always consult with a qualified financial advisor before making investment decisions.
        <br/><br/>
        By using this report, you acknowledge that all investment decisions are made at your own risk, and 
        you are solely responsible for any gains or losses that may result.
        """
        story.append(Paragraph(disclaimer, self.styles['CustomBody']))
        
        # Add footer
        story.append(Spacer(1, 0.3*inch))
        footer = f"<i>Report generated by AI Market Predictor | Advanced Transformer Neural Network | {datetime.now().strftime('%Y')}</i>"
        story.append(Paragraph(footer, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def generate_accuracy_report(
        self,
        accuracy_stats: Dict,
        symbol: Optional[str] = None,
        output_path: str = "reports/accuracy_report.pdf"
    ) -> str:
        """
        Generate prediction accuracy report
        
        Args:
            accuracy_stats: Accuracy statistics from tracker
            symbol: Stock symbol (optional)
            output_path: Where to save PDF
            
        Returns:
            Path to generated PDF
        """
        
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else 'reports', exist_ok=True)
        
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title_text = f"Prediction Accuracy Report"
        if symbol:
            title_text += f" - {symbol}"
        
        story.append(Paragraph(title_text, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Overall stats
        story.append(Paragraph("📈 Performance Summary", self.styles['CustomHeading']))
        
        stats_data = [
            ['Total Predictions:', str(accuracy_stats.get('total_predictions', 0))],
            ['Verified Predictions:', str(accuracy_stats.get('verified_predictions', 0))],
            ['Accuracy Rate:', f"{accuracy_stats.get('accuracy_rate', 0):.2f}%"],
            ['Direction Accuracy:', f"{accuracy_stats.get('direction_accuracy', 0):.2f}%"],
            ['Average Error:', f"{accuracy_stats.get('avg_error', 0):.2f}%"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 3.5*inch])
        stats_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
            ('FONT', (1, 2), (1, 3), 'Helvetica-Bold', 12),
            ('TEXTCOLOR', (1, 2), (1, 3), colors.HexColor('#28a745')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Status breakdown
        story.append(Paragraph("📊 Prediction Quality Breakdown", self.styles['CustomHeading']))
        
        breakdown = accuracy_stats.get('status_breakdown', {})
        breakdown_data = [
            ['Excellent (<2% error):', str(breakdown.get('excellent', 0))],
            ['Good (2-5% error):', str(breakdown.get('good', 0))],
            ['Direction Correct:', str(breakdown.get('direction_correct', 0))],
            ['Incorrect:', str(breakdown.get('incorrect', 0))]
        ]
        
        breakdown_table = Table(breakdown_data, colWidths=[3*inch, 3*inch])
        breakdown_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(breakdown_table)
        
        # Build PDF
        doc.build(story)
        
        return output_path
