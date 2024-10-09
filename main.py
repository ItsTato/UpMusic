import flask
from flask import Flask

site:Flask = Flask(__name__)

@site.route("/",methods=["GET"])
def index():
	return flask.redirect("/app")

@site.route("/images/<image_id>")
def images_id(image_id:int):
	return flask.send_from_directory("./data/images",f"{image_id}.png")

@site.route("/music/<music_id>")
def music_id(music_id:int):
	return flask.send_from_directory("./data/music",f"{music_id}.mp3")

@site.route("/app",methods=["GET"])
def app():
	return flask.render_template("app.html")

site.run("localhost",4646)