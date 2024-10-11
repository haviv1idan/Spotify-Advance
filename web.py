from flask import Flask, redirect, render_template, url_for

from src.utils import (TermEnum, clear_func_cache, current_user_data,
                       print_func_cache, user_top_artists, user_top_tracks)

app = Flask(__name__)


@app.route("/")
def profile():
    user_data = current_user_data()
    return render_template('profile.html', user_data=user_data)


@app.route("/top_artists")
def top_artists():
    top_artists_per_term: dict[str, dict] = {
        term.value: user_top_artists(term=term.value, count=5)
        for term in TermEnum
    }

    app.logger.info(f"{top_artists=}")
    return render_template("top_artists.html", top_artists=top_artists_per_term)


@app.route("/top_tracks")
def top_tracks():
    top_tracks_per_term: dict[str, dict] = {
        term.value: user_top_tracks(term=term.value, count=5)
        for term in TermEnum
    }

    app.logger.info(f"{top_tracks=}")
    return render_template("top_tracks.html", top_tracks=top_tracks_per_term)


@app.route("/get_cache")
def get_cache():
    print_func_cache()
    return redirect(url_for("profile"))


@app.route("/clear_cache")
def clear_cache():
    clear_func_cache()
    return redirect(url_for("profile"))
