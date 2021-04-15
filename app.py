from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

game = Boggle()

@app.route("/")
def start():
    board = game.make_board()
    session['board'] = board
    highscore = session.get("score", 0)
    plays = session.get("plays", 0)

    return render_template("index.html", board=board, highscore=highscore, nplays=plays)

@app.route("/check")
def check():
    word = request.args["word"]
    board = session['board']
    res = game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route("/post-score", methods=['POST'])
def score():
    score = request.json["score"]
    highscore = session.get("score", 0)
    plays = session.get("plays", 0)

    session["score"] = max(highscore, score)
    session["plays"] = plays + 1

    return jsonify(highscore=max(highscore, score))
