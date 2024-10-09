from flask import Flask, redirect, url_for

from src.utils import clear_func_cache, current_user_data

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_data = current_user_data()
    profile_data = f"""
    <h1>Display your Spotify profile data</h1>

    <section id="profile">
    <h2>Logged in as <span id="displayName">{user_data['display_name']}</span></h2>
    <ul>
        <li>User ID: <span id="id">{user_data['id']}</span></li>
        <li>Spotify URI: <a id="uri" href="#">{user_data['uri']}</a></li>
        <li>Spotify URI: <a id="email" href="#">{user_data['email']}</a></li>
    </ul>
    </section>
    """
    return profile_data


@app.route("/clear_cache")
def clear_cache():
    clear_func_cache()
    return redirect(url_for("hello_world"))
