from flask import Flask, redirect, render_template, request, url_for

from src.utils import (TermEnum, clear_func_cache, current_user_data,
                       print_func_cache, user_recommendations,
                       user_saved_tracks, user_top_artists, user_top_tracks)

app = Flask(__name__)


@app.route("/")
def profile():
    app.logger.debug('profile func called')
    user_data = current_user_data()
    return render_template('profile.html', user_data=user_data)


@app.route("/top_artists")
def top_artists():
    app.logger.debug('top_artists func called')
    top_artists_per_term: dict[str, dict] = {
        term.value: user_top_artists(term=term.value, count=5)
        for term in TermEnum
    }

    app.logger.info(f"{top_artists=}")
    return render_template("top_artists.html", top_artists=top_artists_per_term)


@app.route("/top_tracks")
def top_tracks():
    app.logger.debug('top_tracks func called')
    top_tracks_per_term: dict[str, dict] = {
        term.value: user_top_tracks(term=term.value, count=5)
        for term in TermEnum
    }

    app.logger.info(f"{top_tracks=}")
    return render_template("top_tracks.html", top_tracks=top_tracks_per_term)


@app.route("/saved_tracks")
def saved_tracks():
    app.logger.debug('saved_tracks func called')
    saved_tracks = user_saved_tracks()
    app.logger.info(f"{saved_tracks=}")
    return render_template("saved_tracks.html", saved_tracks=saved_tracks)


@app.route('/recommend_playlist', methods=['GET', 'POST'])
def recommend_playlist():
    if request.method == 'POST':

        # Get the selected artist IDs from the form
        selected_artists = request.form.getlist('artists')

        # Ensure exactly five artists are selected
        if len(selected_artists) != 5:
            return render_template(
                'recommend_playlist.html',
                top_artists=top_artists,
                error="Please select exactly 5 artists.")

        # Pass recommended tracks to the template
        recommended_tracks = user_recommendations(artists=selected_artists)
        return render_template('recommend_results.html', recommended_tracks=recommended_tracks)

    # Retrieve top artists
    return render_template('recommend_playlist.html', top_artists=user_top_artists())


@app.route("/get_cache")
def get_cache():
    app.logger.debug('get_cache func called')
    print_func_cache()
    return redirect(url_for("profile"))


@app.route("/clear_cache")
def clear_cache():
    app.logger.debug('clear_cache func called')
    clear_func_cache()
    return redirect(url_for("profile"))
