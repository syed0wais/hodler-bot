import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch news articles using NewsAPI
def get_news_articles(stock_symbol, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_symbol}&apiKey={api_key}&language=en'
    response = requests.get(url)
    data = response.json()

    # If API returns an error or no articles, return an empty list
    if data.get('status') != 'ok' or 'articles' not in data:
        return []

    articles = data['articles']
    return articles

# Function to analyze sentiment of a list of articles
def analyze_sentiment_of_articles(articles):
    sentiment_scores = []
    for article in articles:
        # Get the title and description of the article
        text = article['title'] + " " + article['description'] if article['description'] else article['title']
        sentiment = analyzer.polarity_scores(text)
        sentiment_scores.append(sentiment['compound'])  # Compound score is the overall sentiment

    return sentiment_scores

# Define function to determine overall sentiment (buy/sell/hold)
def generate_signal(sentiment_scores):
    if len(sentiment_scores) == 0:
        return "No data available", 0.0  # In case no articles are fetched

    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

    if avg_sentiment > 0.1:
        return "BUY", avg_sentiment
    elif avg_sentiment < -0.1:
        return "SELL", avg_sentiment
    else:
        return "HOLD", avg_sentiment

# Example usage
def main(stock_symbol, api_key):
    # Fetch the latest news articles related to the stock
    articles = get_news_articles(stock_symbol, api_key)

    if not articles:
        print(f"No news articles found for {stock_symbol}. Please check the stock symbol or try again later.")
        return

    # Analyze sentiment for each article
    sentiment_scores = analyze_sentiment_of_articles(articles)

    # Generate Buy/Sell/Hold signal based on sentiment
    signal, avg_sentiment = generate_signal(sentiment_scores)

    # Output the result with sentiment score
    print(f"Sentiment Analysis for {stock_symbol}: {signal}")
    print(f"Average Sentiment Score: {avg_sentiment:.2f}")


# Main code
if __name__ == "__main__":

    api_key = '84304d30650d4d959fee116667241dda'  # API key
    stock_symbol = 'AAPL'  # stock symbol

    # main function
    main(stock_symbol, api_key)
