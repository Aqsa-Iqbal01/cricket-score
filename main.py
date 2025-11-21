
import requests
import xmltodict
from flask import Flask, render_template

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
    scores = get_live_scores()
    return render_template("index.html", scores=scores)

if __name__ == "__main__":
    app.run(debug=True)
