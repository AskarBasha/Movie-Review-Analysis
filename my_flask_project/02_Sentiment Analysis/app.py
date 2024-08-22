from flask import Flask, render_template, request
import pickle
import random
from textblob import TextBlob

app = Flask(__name__)

# Load the stored movie reviews data
def load_data():
    with open('stored_data.pkl', 'rb') as file:
        return pickle.load(file)

# Perform sentiment analysis on the selected number of reviews
def analyze_sentiment(reviews, num_reviews):
    random.seed(10)
    selected_reviews = [random.choice(reviews) for _ in range(num_reviews)]
    pos = neg = neu = 0
    for review in selected_reviews:
        sentiment = TextBlob(review[0]).polarity
        if sentiment > 0:
            pos += 1
        elif sentiment < 0:
            neg += 1
        else:
            neu += 1
    total = len(selected_reviews)
    return {
        "positive": round((pos / total) * 100, 2),
        "negative": round((neg / total) * 100, 2),
        "neutral": round((neu / total) * 100, 2)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    pre = load_data()
    movies = list(pre.keys())
    max_reviews = max([len(pre[movie]) for movie in movies])

    if request.method == 'POST':
        selected_movie = request.form['movie']
        num_reviews = int(request.form['num_reviews'])
        reviews = pre[selected_movie]
        results = analyze_sentiment(reviews, num_reviews)
        return render_template('index.html', movies=movies, max_reviews=max_reviews, results=results, selected_movie=selected_movie)
    
    return render_template('index.html', movies=movies, max_reviews=max_reviews, results=None)

if __name__ == '__main__':
    app.run(debug=True)
