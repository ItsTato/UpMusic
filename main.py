import flask
from flask import Flask

site:Flask = Flask(__name__)

@site.route("/",methods=["GET"])
def index():
	return flask.redirect("/app")

@site.route("/songs/<song_id>")
def songs_id(song_id:int):
	song_id = int(song_id)
	if song_id == 1:
		return {
			"title": "Mr. Blue Sky",
			"artist": "Electric Light Orchestra",
			"audio_id": 1,
			"thumbnail_id": 1
		}

@site.route("/files/audio/<audio_id>")
def files_audio_id(audio_id:int):
	return flask.send_from_directory("./data/audio",f"{audio_id}.mp3")

@site.route("/files/images/<image_id>")
def files_images_id(image_id:int):
	return flask.send_from_directory("./data/images",f"{image_id}.png")

@site.route("/app",methods=["GET"])
def app():
	return flask.render_template("app.html")

site.run("localhost",4646)