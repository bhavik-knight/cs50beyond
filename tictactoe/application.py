#!/usr/bin/env python3

#####################################
# Bhavik Knight
#
# day1, morning session
# problem - tictactoe
#
# 2019, CS50beyond
#####################################


from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index(n=3):
    if "board" not in session:
        session["board"] = [[None for _ in range(n)] for _ in range(n)]
        session["turn"] = "X"
    return render_template("game.html", game=session["board"], turn=session["turn"], n=n)


@app.route("/reset")
def reset():
    # remove existing board from session
    del(session["board"])
    return redirect(url_for("index"))


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]

    # play turn, check game state, update table
    is_game_over, winner = game_state(row, col)
    if is_game_over:
        result = f"Winner: {'-XO'[winner]}" if winner else "Game Draw"
        return render_template("final.html", game=session["board"], result=result)

    # other player's turn
    session["turn"] = "O" if session["turn"] == "X" else "X"
    return redirect(url_for("index"))


def game_state(i, j):
    """
    (int, int) -> tuple

    :param i: an int, grid's x coordinate
    :param j: an int, grid's y coordinate

    :returns: a tuple, (False, None) if game is not finished yet
    or draw if finished already, (True, int) where int helps to identify the winner
    """
    grid = session["board"]
    n = len(grid)

    # from top-left to bottom-right diagonal, aka major diagonal (\)
    if i == j:
        check = [grid[d][d] for d in range(n)]
        major = is_won(check)
        if major[0]: return major

    # from top-right, bottom-left diagonal, aka minor diagonal (/)
    if (i + j) == (n - 1):
        check = [grid[d][(n - 1) - d] for d in range(n)]
        minor = is_won(check)
        if minor[0]: return minor

    # row, column
    check = [grid[i][col] for col in range(n)]
    row = is_won(check)
    if row[0]: return row

    check = [grid[row][j] for row in range(n)]
    col = is_won(check)
    if col[0]: return col

    # check for game state whether completed or not
    counter = sum(1 for row in grid for e in row if e == None)
    if counter:
        return False, None
    return True, None


def is_won(check):
    """
    (list) -> tuple

    :param check: a list, having data to check whether game is won or not

    :returns: a tuple, (True, int) if game is won (False, None) o.w.
    """
    tot, n = -1, len(check)
    try:
        tot = sum("-XO".index(e) for e in check)
    except TypeError:
        pass

    return (False, None) if (tot % n) else (True, tot // n)


if __name__ == "__main__":
    app.run(debug=True)
