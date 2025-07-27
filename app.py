from flask import Flask, render_template, request, redirect, url_for, make_response
import json

app = Flask(__name__)
@app.template_filter('thousands')
def thousands_filter(value):
    return f"{value:,}".replace(",", ".")

VOTE_FILE = "votes.json"

def load_votes():
    with open(VOTE_FILE, "r") as f:
        return json.load(f)

def save_votes(votes):
    with open(VOTE_FILE, "w") as f:
        json.dump(votes, f)

@app.route("/")
def index():
    votes = load_votes()
    voted = request.cookies.get("voted")
    return render_template("index.html", votes=votes, voted=voted)

@app.route("/vote/<player>", methods=["POST"])
def vote(player):
    voted = request.cookies.get("voted")

    if voted:  # se ha già votato, lo rimandiamo indietro
        return redirect(url_for("index"))

    votes = load_votes()
    if player in votes:
        votes[player] += 1
        save_votes(votes)

    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("voted", player, max_age=60*60*24*365)  # 1 anno

    return resp

if __name__ == "__main__":
    app.run(debug=True)
