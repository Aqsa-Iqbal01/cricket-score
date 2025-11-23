
import requests
import xmltodict
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def get_live_scores():
    """
    Fetches live cricket scores from the RSS feed.
    """
    try:
        response = requests.get("https://static.cricinfo.com/rss/livescores.xml")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = xmltodict.parse(response.content)
        return data["rss"]["channel"]["item"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

@app.route("/")
def index():
    """
    Renders the index page with live scores.
    """
    return render_template("index.html")

@app.route("/api/scores")
def api_scores():
    """
    Returns live cricket scores as JSON, with optional search.
    """
    search_term = request.args.get("search", "").lower()
    scores = get_live_scores()

    if search_term:
        filtered_scores = [
            score for score in scores
            if search_term in score.get("title", "").lower()
        ]
        return jsonify(filtered_scores)
    else:
        return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True)
