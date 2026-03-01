"""
Advanced Sentiment Analysis Engine for Stock Market Predictions

This module provides comprehensive sentiment analysis combining:
- News sentiment analysis using NewsAPI
- Multi-source sentiment scoring (VADER + TextBlob)
- Sentiment trend tracking (7-day history)
- Technical vs Sentiment conflict detection
- Topic extraction and keyword analysis

Author: AI Market Predictor Team
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from collections import defaultdict

# Sentiment Analysis Libraries
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Advanced sentiment analysis engine that combines multiple sources
    to provide comprehensive market sentiment insights.
    """
    
    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize the sentiment analyzer with NewsAPI integration.
        
        Args:
            newsapi_key: NewsAPI key for fetching news articles
        """
        self.newsapi_key = newsapi_key or os.getenv('NEWSAPI_KEY')
        
        # Initialize sentiment analyzers
        self.vader = SentimentIntensityAnalyzer() if VADER_AVAILABLE else None
        
        # Initialize NewsAPI client
        self.newsapi = None
        if NEWSAPI_AVAILABLE and self.newsapi_key:
            try:
                self.newsapi = NewsApiClient(api_key=self.newsapi_key)
                logger.info("✓ NewsAPI initialized successfully")
            except Exception as e:
                logger.warning(f"NewsAPI initialization failed: {e}")
        
        # Sentiment history storage
        self.sentiment_history_file = "sentiment_history.json"
        self.sentiment_history = self._load_sentiment_history()
        
        # Indian stock market keywords
        self.market_keywords = {
            'positive': ['bullish', 'surge', 'rally', 'gain', 'profit', 'growth', 'upgrade', 
                        'expansion', 'revenue', 'earnings beat', 'breakthrough', 'innovation'],
            'negative': ['bearish', 'crash', 'decline', 'loss', 'risk', 'warning', 'downgrade',
                        'recession', 'layoff', 'scandal', 'investigation', 'penalty', 'debt']
        }
    
    def _load_sentiment_history(self) -> Dict:
        """Load sentiment history from JSON file."""
        try:
            if os.path.exists(self.sentiment_history_file):
                with open(self.sentiment_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading sentiment history: {e}")
        return {}
    
    def _save_sentiment_history(self):
        """Save sentiment history to JSON file."""
        try:
            with open(self.sentiment_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.sentiment_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving sentiment history: {e}")
    
    def fetch_news(self, symbol: str, company_name: str, days_back: int = 7) -> List[Dict]:
        """
        Fetch news articles for a given stock symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            company_name: Company name for search
            days_back: Number of days to look back
            
        Returns:
            List of news articles with metadata
        """
        if not self.newsapi:
            logger.warning("NewsAPI not available - using mock data")
            return self._get_mock_news(symbol, company_name)
        
        try:
            # Clean symbol (remove .NS for search)
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            # Search for news
            search_query = f"{company_name} OR {clean_symbol} stock India"
            
            response = self.newsapi.get_everything(
                q=search_query,
                language='en',
                sort_by='publishedAt',
                from_param=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d'),
                page_size=20
            )
            
            articles = []
            if response and response.get('articles'):
                for article in response['articles']:
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'content': article.get('content', '')
                    })
            
            logger.info(f"✓ Fetched {len(articles)} news articles for {symbol}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return self._get_mock_news(symbol, company_name)
    
    def _get_mock_news(self, symbol: str, company_name: str) -> List[Dict]:
        """Generate mock news for testing when NewsAPI is unavailable."""
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        mock_articles = [
            {
                'title': f'{company_name} reports strong quarterly earnings, stock surges',
                'description': f'{company_name} exceeded analyst expectations with robust revenue growth.',
                'source': 'Economic Times',
                'url': 'https://economictimes.com',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'content': f'{company_name} stock gained momentum after earnings beat.'
            },
            {
                'title': f'Market analysts upgrade {clean_symbol} to buy rating',
                'description': 'Leading analysts see strong growth potential in the sector.',
                'source': 'Moneycontrol',
                'url': 'https://moneycontrol.com',
                'published_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'content': 'Positive outlook for the company based on fundamentals.'
            },
            {
                'title': f'{company_name} faces headwinds amid market volatility',
                'description': 'Concerns about global economic slowdown impact investor sentiment.',
                'source': 'Business Standard',
                'url': 'https://business-standard.com',
                'published_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'content': 'Market uncertainty creates challenges for the stock.'
            }
        ]
        
        return mock_articles
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text using multiple methods.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores from multiple sources
        """
        if not text:
            return {'score': 0.0, 'label': 'neutral', 'confidence': 0.0}
        
        scores = []
        
        # VADER sentiment (specialized for social media and news)
        if self.vader and VADER_AVAILABLE:
            vader_scores = self.vader.polarity_scores(text)
            vader_compound = vader_scores['compound']
            scores.append(vader_compound)
        
        # TextBlob sentiment (general-purpose NLP)
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                textblob_score = blob.sentiment.polarity
                scores.append(textblob_score)
            except Exception as e:
                logger.warning(f"TextBlob analysis failed: {e}")
        
        # Keyword-based sentiment (domain-specific for stocks)
        keyword_score = self._keyword_sentiment(text)
        scores.append(keyword_score)
        
        # Average all scores
        if scores:
            avg_score = np.mean(scores)
            confidence = 1.0 - np.std(scores)  # Lower std = higher confidence
        else:
            avg_score = 0.0
            confidence = 0.0
        
        # Determine sentiment label
        if avg_score > 0.05:
            label = 'positive'
        elif avg_score < -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'score': float(avg_score),
            'label': label,
            'confidence': float(max(0.0, min(1.0, confidence)))
        }
    
    def _keyword_sentiment(self, text: str) -> float:
        """Calculate sentiment based on financial keywords."""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.market_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.market_keywords['negative'] if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        return (positive_count - negative_count) / total
    
    def analyze_news_sentiment(self, symbol: str, company_name: str) -> Dict:
        """
        Analyze overall sentiment from news articles.
        
        Args:
            symbol: Stock symbol
            company_name: Company name
            
        Returns:
            Comprehensive sentiment analysis results
        """
        # Fetch news articles
        articles = self.fetch_news(symbol, company_name)
        
        if not articles:
            return {
                'overall_score': 0.0,
                'overall_label': 'neutral',
                'confidence': 0.0,
                'article_count': 0,
                'articles': [],
                'trend': 'insufficient_data'
            }
        
        # Analyze each article
        analyzed_articles = []
        scores = []
        
        for article in articles:
            # Combine title and description for analysis
            text = f"{article['title']} {article['description']}"
            sentiment = self.analyze_text_sentiment(text)
            
            analyzed_articles.append({
                'title': article['title'],
                'source': article['source'],
                'url': article['url'],
                'published_at': article['published_at'],
                'sentiment': sentiment
            })
            
            scores.append(sentiment['score'])
        
        # Calculate overall sentiment
        overall_score = np.mean(scores) if scores else 0.0
        overall_std = np.std(scores) if len(scores) > 1 else 0.0
        confidence = 1.0 - min(overall_std, 1.0)
        
        # Determine overall label
        if overall_score > 0.1:
            overall_label = 'positive'
        elif overall_score < -0.1:
            overall_label = 'negative'
        else:
            overall_label = 'neutral'
        
        # Determine trend
        if len(scores) >= 3:
            recent_avg = np.mean(scores[:3])
            older_avg = np.mean(scores[3:]) if len(scores) > 3 else overall_score
            
            if recent_avg > older_avg + 0.1:
                trend = 'improving'
            elif recent_avg < older_avg - 0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        # Save to history
        self._update_sentiment_history(symbol, overall_score, overall_label)
        
        result = {
            'overall_score': float(overall_score),
            'overall_label': overall_label,
            'confidence': float(confidence),
            'article_count': len(analyzed_articles),
            'articles': analyzed_articles[:10],  # Top 10 most recent
            'trend': trend,
            'positive_count': sum(1 for a in analyzed_articles if a['sentiment']['label'] == 'positive'),
            'negative_count': sum(1 for a in analyzed_articles if a['sentiment']['label'] == 'negative'),
            'neutral_count': sum(1 for a in analyzed_articles if a['sentiment']['label'] == 'neutral')
        }
        
        logger.info(f"✓ Sentiment analysis complete for {symbol}: {overall_label} ({overall_score:.3f})")
        return result
    
    def _update_sentiment_history(self, symbol: str, score: float, label: str):
        """Update sentiment history for a symbol."""
        if symbol not in self.sentiment_history:
            self.sentiment_history[symbol] = []
        
        self.sentiment_history[symbol].append({
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'label': label
        })
        
        # Keep only last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        self.sentiment_history[symbol] = [
            entry for entry in self.sentiment_history[symbol]
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        self._save_sentiment_history()
    
    def get_sentiment_trend(self, symbol: str, days: int = 7) -> List[Dict]:
        """
        Get sentiment trend for the past N days.
        
        Args:
            symbol: Stock symbol
            days: Number of days to retrieve
            
        Returns:
            List of sentiment data points
        """
        if symbol not in self.sentiment_history:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        trend_data = [
            entry for entry in self.sentiment_history[symbol]
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        return sorted(trend_data, key=lambda x: x['timestamp'])
    
    def detect_sentiment_conflicts(self, symbol: str, technical_signal: str, 
                                   technical_confidence: float) -> Optional[Dict]:
        """
        Detect conflicts between technical indicators and sentiment.
        
        Args:
            symbol: Stock symbol
            technical_signal: 'bullish', 'bearish', or 'neutral'
            technical_confidence: Confidence in technical signal (0-1)
            
        Returns:
            Conflict information if detected, None otherwise
        """
        # Get recent sentiment
        recent_sentiment = self.sentiment_history.get(symbol, [])
        if not recent_sentiment:
            return None
        
        # Get most recent sentiment
        latest = recent_sentiment[-1]
        sentiment_label = latest['label']
        sentiment_score = latest['score']
        
        # Map technical signal to sentiment
        technical_sentiment_map = {
            'bullish': 'positive',
            'bearish': 'negative',
            'neutral': 'neutral'
        }
        
        expected_sentiment = technical_sentiment_map.get(technical_signal, 'neutral')
        
        # Check for strong conflict
        conflict_detected = False
        conflict_severity = 'low'
        
        if expected_sentiment == 'positive' and sentiment_label == 'negative':
            conflict_detected = True
            conflict_severity = 'high' if abs(sentiment_score) > 0.3 else 'medium'
        elif expected_sentiment == 'negative' and sentiment_label == 'positive':
            conflict_detected = True
            conflict_severity = 'high' if sentiment_score > 0.3 else 'medium'
        elif expected_sentiment != 'neutral' and sentiment_label != expected_sentiment:
            conflict_detected = True
            conflict_severity = 'low'
        
        if not conflict_detected:
            return None
        
        return {
            'symbol': symbol,
            'technical_signal': technical_signal,
            'technical_confidence': technical_confidence,
            'sentiment_label': sentiment_label,
            'sentiment_score': sentiment_score,
            'conflict_severity': conflict_severity,
            'message': f"⚠️ Conflict detected: Technical indicators suggest {technical_signal}, "
                      f"but market sentiment is {sentiment_label}",
            'recommendation': self._generate_conflict_recommendation(
                technical_signal, sentiment_label, conflict_severity
            )
        }
    
    def _generate_conflict_recommendation(self, technical: str, sentiment: str, 
                                         severity: str) -> str:
        """Generate recommendation based on conflict analysis."""
        if severity == 'high':
            return ("Strong divergence between technical and sentiment signals. "
                   "Exercise caution and consider waiting for signal alignment. "
                   "News-driven sentiment may override technical patterns in the short term.")
        elif severity == 'medium':
            return ("Moderate divergence detected. Technical analysis may be more reliable "
                   "for timing, but monitor news developments closely.")
        else:
            return ("Minor divergence - both signals can be considered. "
                   "Overall market conditions appear mixed.")


# Utility function for easy integration
def create_sentiment_analyzer(newsapi_key: Optional[str] = None) -> SentimentAnalyzer:
    """
    Factory function to create a SentimentAnalyzer instance.
    
    Args:
        newsapi_key: Optional NewsAPI key
        
    Returns:
        Initialized SentimentAnalyzer instance
    """
    return SentimentAnalyzer(newsapi_key=newsapi_key)


if __name__ == "__main__":
    # Demo usage
    analyzer = create_sentiment_analyzer()
    
    # Test sentiment analysis
    test_symbol = "RELIANCE.NS"
    test_company = "Reliance Industries"
    
    print(f"\n{'='*60}")
    print(f"Sentiment Analysis Demo for {test_company}")
    print(f"{'='*60}\n")
    
    # Analyze news sentiment
    result = analyzer.analyze_news_sentiment(test_symbol, test_company)
    
    print(f"Overall Sentiment: {result['overall_label'].upper()} "
          f"(Score: {result['overall_score']:.3f})")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Articles Analyzed: {result['article_count']}")
    print(f"Trend: {result['trend']}")
    print(f"\nBreakdown:")
    print(f"  Positive: {result['positive_count']}")
    print(f"  Negative: {result['negative_count']}")
    print(f"  Neutral: {result['neutral_count']}")
    
    if result['articles']:
        print(f"\nTop Headlines:")
        for i, article in enumerate(result['articles'][:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Sentiment: {article['sentiment']['label']} "
                  f"({article['sentiment']['score']:.3f})")
    
    # Test conflict detection
    print(f"\n{'='*60}")
    print("Conflict Detection Demo")
    print(f"{'='*60}\n")
    
    conflict = analyzer.detect_sentiment_conflicts(
        test_symbol, 
        technical_signal='bullish',
        technical_confidence=0.8
    )
    
    if conflict:
        print(f"⚠️  {conflict['message']}")
        print(f"Severity: {conflict['conflict_severity'].upper()}")
        print(f"Recommendation: {conflict['recommendation']}")
    else:
        print("✓ No conflicts detected - technical and sentiment signals aligned")
