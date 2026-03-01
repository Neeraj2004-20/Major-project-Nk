"""
LLM Demo and Usage Examples
Shows how to use the AI Market Intelligence system
"""

import json
from datetime import datetime, timedelta
import numpy as np

# Import the AI modules
try:
    from ai_llm_integration import create_ai_intelligence
    from sentiment_analyzer import SentimentAnalyzer
except ImportError as e:
    print(f"Import error - make sure all modules are installed: {e}")
    exit(1)


def demo_basic_analysis():
    """Demo: Basic stock analysis with LLM"""
    print("\n" + "="*80)
    print("DEMO 1: Basic Stock Analysis with LLM")
    print("="*80 + "\n")
    
    # Create AI system
    ai = create_ai_intelligence()
    
    # Sample stock data
    symbol = "AAPL"
    current_price = 150.75
    predicted_price = 158.50
    
    # Sample technical indicators
    technical_indicators = {
        "RSI": 65,
        "MACD": 0.45,
        "SMA_20": 148.30,
        "BB_Width": 2.50,
        "Volume_Ratio": 1.2,
        "Volatility": 0.018
    }
    
    # Sample news headlines
    news_headlines = [
        "Apple stock rises as iPhone 15 sales exceed expectations",
        "Tim Cook optimistic about 2024 growth prospects",
        "Tech sector rallies on strong earnings reports"
    ]
    
    # Run analysis
    analysis = ai.analyze_stock(
        symbol=symbol,
        current_price=current_price,
        predicted_price=predicted_price,
        technical_indicators=technical_indicators,
        news_headlines=news_headlines,
        confidence=0.82
    )
    
    # Print results
    print(f"Stock: {analysis['symbol']}")
    print(f"Signal: {analysis['signals']['signal']}")
    print(f"Confidence: {analysis['confidence']:.0%}")
    print(f"Price Target: ${analysis['signals']['price_target']:.2f}")
    print(f"\nRecommendations:")
    for rec in analysis['recommendations'][:3]:
        print(f"  • {rec}")
    
    return analysis


def demo_conversation():
    """Demo: Conversational interaction"""
    print("\n" + "="*80)
    print("DEMO 2: Conversational Analysis")
    print("="*80 + "\n")
    
    ai = create_ai_intelligence()
    
    # Pre-load some analysis
    ai.analyze_stock(
        symbol="TSLA",
        current_price=250.0,
        predicted_price=268.50,
        technical_indicators={"RSI": 72, "MACD": 1.2, "SMA_20": 245.00},
        news_headlines=["Tesla Q3 earnings beat analyst expectations",
                       "Musk announces new factory in Mexico"],
        confidence=0.79
    )
    
    ai.analyze_stock(
        symbol="MSFT",
        current_price=380.0,
        predicted_price=392.00,
        technical_indicators={"RSI": 58, "MACD": 0.65, "SMA_20": 375.00},
        news_headlines=["Microsoft Azure growth accelerates",
                       "AI integration boosts productivity features"],
        confidence=0.75
    )
    
    # Have conversation
    questions = [
        "What's the prediction for Tesla?",
        "Should I buy MSFT right now?",
        "How's the market sentiment?"
    ]
    
    for question in questions:
        print(f"User: {question}")
        response = ai.chat(question)
        print(f"Assistant: {response}\n")


def demo_market_summary():
    """Demo: Market-wide summary"""
    print("\n" + "="*80)
    print("DEMO 3: Market Summary Across Multiple Stocks")
    print("="*80 + "\n")
    
    ai = create_ai_intelligence()
    
    # Analyze multiple stocks
    stocks = [
        ("AAPL", 150.75, 158.50, 0.75),
        ("MSFT", 380.00, 392.00, 0.72),
        ("GOOGL", 140.20, 148.75, 0.68),
        ("TSLA", 250.00, 268.50, 0.79),
    ]
    
    for symbol, current, predicted, conf in stocks:
        ai.analyze_stock(
            symbol=symbol,
            current_price=current,
            predicted_price=predicted,
            confidence=conf
        )
    
    # Get market summary
    summary = ai.get_market_summary([s[0] for s in stocks])
    
    print(f"Market Summary:")
    print(f"  Total Symbols: {summary['total_symbols']}")
    print(f"  Buy Signals: {summary['buy_signals']}")
    print(f"  Sell Signals: {summary['sell_signals']}")
    print(f"  Hold Signals: {summary['hold_signals']}")
    print(f"  Market Bias: {summary['market_bias']}")
    print(f"  Average Confidence: {summary['average_confidence']:.0%}")
    
    print(f"\nMarket Insights:")
    for insight in summary.get('insights', []):
        print(f"  • {insight}")


def demo_trading_alerts():
    """Demo: Trading alerts"""
    print("\n" + "="*80)
    print("DEMO 4: Trading Alerts")
    print("="*80 + "\n")
    
    ai = create_ai_intelligence()
    
    # Analyze some stocks
    stocks = [
        ("NVDA", 875.00, 920.00, 0.85),
        ("AMD", 165.40, 172.30, 0.72),
        ("INTC", 42.50, 41.80, 0.65),
    ]
    
    for symbol, current, predicted, conf in stocks:
        ai.analyze_stock(
            symbol=symbol,
            current_price=current,
            predicted_price=predicted,
            confidence=conf
        )
    
    # Get alerts
    alerts = ai.get_trading_alerts([s[0] for s in stocks])
    
    print("Trading Alerts (sorted by strength):\n")
    for alert in alerts:
        print(f"🔔 {alert['symbol']}")
        print(f"   Signal: {alert['signal']} (Strength: {alert['strength']:.0%})")
        print(f"   Action: {alert['action']}")
        print(f"   Target: ${alert['take_profit']:.2f}")
        print(f"   Stop: ${alert['stop_loss']:.2f}")
        print()


def demo_sentiment_integration():
    """Demo: Using sentiment analyzer with LLM"""
    print("\n" + "="*80)
    print("DEMO 5: Sentiment Analyzer Integration")
    print("="*80 + "\n")
    
    # Initialize sentiment analyzer
    try:
        sentiment = SentimentAnalyzer()
    except Exception as e:
        print(f"Note: Sentiment analyzer not fully available: {e}")
        print("Using mock sentiment data instead\n")
        sentiment = None
    
    # Create AI system
    ai = create_ai_intelligence()
    
    # Analyze with sentiment
    symbol = "NVDA"
    current_price = 875.00
    predicted_price = 920.00
    
    news = [
        "NVDA beats earnings expectations with strong data center demand",
        "AI boom drives semiconductor stock prices higher",
        "Nvidia announces record quarterly revenue"
    ]
    
    # Calculate sentiment
    if sentiment:
        try:
            sentiments = sentiment.analyze_multiple(news)
            sentiment_score = np.mean([s['score'] for s in sentiments])
        except:
            sentiment_score = 0.65
    else:
        sentiment_score = 0.65
    
    print(f"Analyzing {symbol}")
    print(f"Sentiment Score: {sentiment_score:.2f}")
    print(f"News Headlines: {len(news)}")
    
    # Run analysis
    analysis = ai.analyze_stock(
        symbol=symbol,
        current_price=current_price,
        predicted_price=predicted_price,
        sentiment_analyzer=sentiment if sentiment else None,
        news_headlines=news,
        confidence=0.82
    )
    
    print(f"\nAnalysis Signal: {analysis['signals']['signal']}")
    print(f"Recommendation: {analysis['recommendations'][0]}")


def demo_performance_metrics():
    """Demo: System performance metrics"""
    print("\n" + "="*80)
    print("DEMO 6: Performance Metrics")
    print("="*80 + "\n")
    
    ai = create_ai_intelligence()
    
    # Run several analyses
    test_stocks = [
        ("AAPL", 150, 155, 0.75),
        ("MSFT", 380, 395, 0.72),
        ("GOOGL", 140, 145, 0.68),
        ("AMZN", 170, 180, 0.80),
        ("NVDA", 875, 920, 0.85),
    ]
    
    for symbol, current, predicted, conf in test_stocks:
        ai.analyze_stock(
            symbol=symbol,
            current_price=current,
            predicted_price=predicted,
            confidence=conf
        )
    
    # Get metrics
    metrics = ai.get_performance_metrics()
    
    print("System Performance Metrics:")
    print(f"  Total Analyses: {metrics['total_analyses']}")
    print(f"  Buy Signals: {metrics['buy_signals']}")
    print(f"  Sell Signals: {metrics['sell_signals']}")
    print(f"  Hold Signals: {metrics['hold_signals']}")
    print(f"  Buy Ratio: {metrics['buy_ratio']:.0%}")
    print(f"  Average Confidence: {metrics['average_confidence']:.0%}")
    print(f"  Unique Symbols: {metrics['unique_symbols']}")


def demo_export_import():
    """Demo: Export and import analysis"""
    print("\n" + "="*80)
    print("DEMO 7: Export Analysis Data")
    print("="*80 + "\n")
    
    ai = create_ai_intelligence()
    
    # Run an analysis
    ai.analyze_stock(
        symbol="AAPL",
        current_price=150.75,
        predicted_price=158.50,
        news_headlines=["Apple stock rises", "iPhone sales strong"],
        confidence=0.82
    )
    
    # Export
    export_path = "analysis_export_demo.json"
    ai.export_analysis(export_path, format="json")
    
    print(f"✓ Analysis exported to: {export_path}")
    
    # Show sample of exported data
    with open(export_path, 'r') as f:
        data = json.load(f)
    
    print(f"✓ Exported {len(data['analyses'])} analyses")
    print(f"✓ Conversation turns: {len(data['conversation_history'])}")
    print(f"✓ Timestamp: {data['exported_at']}")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("= AI Market Predictor - LLM Integration Demos")
    print("="*80)
    
    demos = [
        ("Basic Analysis", demo_basic_analysis),
        ("Conversational", demo_conversation),
        ("Market Summary", demo_market_summary),
        ("Trading Alerts", demo_trading_alerts),
        ("Sentiment Integration", demo_sentiment_integration),
        ("Performance Metrics", demo_performance_metrics),
        ("Export/Import", demo_export_import),
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all demos...\n")
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n⚠️  Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("= All demos completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
