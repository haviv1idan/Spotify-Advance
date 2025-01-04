# Spotify-Advance
some cool stuffs for spotify

## prerequisites
### Spotify Client data
Before starting working we need to get our client data from Spotify to use the API
- create a new account or log in on https://developers.spotify.com/.
- Go to the dashboard, create an app and add your new ID and SECRET (ID and SECRET can be found on an app setting) to conf.yml file.

Example of conf.yml file:
```yaml
client_id: <CLIENT_ID>
client_secret: <CLIENT_SECRET>
redirect_uri: http://localhost:3000
```

### Setup venv
```bash
python -m venv venv
```

### install requirements
```bash
pip install -r requirements.txt
```

## How to use
### ipynb file
You can use the playground.ipynb file to run blocks of code and debugging

### scripts
You can use the files with *.py* to run specific api

### using flask
```bash
flask --app web run --debug
```


## In Development
Improving of the flask app

### Usage:
Build docker file
```bash
docker run -itd -p 5000:5000 spotify-advance:latest
```
