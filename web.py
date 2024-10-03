from typing import Final
from flask import Flask
from src.utils import read_client_data, user

app = Flask(__name__)

@app.route('/')
def hello_world():
    user_data: dict = user().me()
    profile_data = \
    f"""
    <h1>Display your Spotify profile data</h1>

    <section id="profile">
    <h2>Logged in as <span id="displayName">{user_data['display_name']}</span></h2>
    <ul>
        <li>User ID: <span id="id">{user_data['id']}</span></li>
        <li>Spotify URI: <a id="uri" href="#">{user_data['uri']}</a></li>
    </ul>
    </section>    
    """
    return profile_data

