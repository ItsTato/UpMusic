import flask
from flask import Flask
from upmusicdb import Controller, Objects
from json import load, dump
from os import listdir, path

with open("./secret.key","r") as file:
	secretKey = file.read()

site:Flask = Flask(__name__)
updb:Controller = Controller("./data/UpMusic.sqlite3")

site.config["SECRET_KEY"] = secretKey

@site.route("/",methods=["GET"])
def index():
	if not flask.session.get("user"):
		return flask.redirect("/login")
	return flask.redirect("/app")

@site.route("/files/audios/<audio_id>")
def files_audio_id(audio_id:int):
	if not flask.session.get("user"):
		return flask.redirect("/login")
	audio_id = int(audio_id)
	audio:Objects.Audio|None = updb.getAudio(audio_id)
	if audio is not None:
		return flask.send_from_directory("./data/audios",audio.file_name)
	return "Audio not found", 404

@site.route("/files/images/<image_id>")
def files_images_id(image_id:int):
	if not flask.session.get("user"):
		return flask.redirect("/login")
	image_id = int(image_id)
	image:Objects.Image|None = updb.getImage(image_id)
	if image is not None:
		return flask.send_from_directory("./data/images",image.file_name)
	return "Image not found", 404

@site.route("/files/pfps/<user_id>",methods=["GET"])
def files_pfps_id(user_id:int):
	if not flask.session.get("user"):
		return flask.redirect("/login")
	return flask.send_from_directory(f"./data/users/{user_id}","pfp.png")

@site.route("/api/songs/<song_id>")
def api_songs_id(song_id:int):
	if not flask.session.get("user"):
		return flask.redirect("/login")
	song_id = int(song_id)
	song:Objects.Song|None = updb.getSong(song_id)
	if song is not None:
		return {
			"title": song.name,
			"artist": song.artist.name,
			"thumbnail_id": song.thumbnail.id,
			"audio_id": song.audio.id
		}
	return {}

@site.route("/api/songs/<song_id>/like",methods=["GET","POST","DELETE"])
def api_songs_id_like(song_id:int):
	if not flask.session.get("user"):
		return flask.redirect("/login")
	song_id = int(song_id)
	with open(f"./data/users/{flask.session['user']['ID']}/playlists.json","r") as file:
		data:dict[str,list] = load(file)
	if flask.request.method.upper() == "GET":
		return {"Liked": song_id in data["Likes"]}
	if flask.request.method.upper() == "POST":
		data["Likes"].append(song_id)
		with open(f"./data/users/{flask.session['user']['ID']}/playlists.json","w") as file:
			dump(data,file)
		return {"Liked": True}, 200
	if flask.request.method.upper() == "DELETE":
		data["Likes"].remove(song_id)
		with open(f"./data/users/{flask.session['user']['ID']}/playlists.json","w") as file:
			dump(data,file)
		return {"Liked": False}, 200
	return "Uhm... What?", 404

@site.route("/app",methods=["GET"])
def app():
	if not flask.session.get("user"):
		return flask.redirect("/login")
	return flask.render_template("app.html",user_name=flask.session["user"]["Name"],user_id=flask.session["user"]["ID"])

@site.route("/login",methods=["GET","POST"])
def login():
	if flask.request.method.upper() == "GET":
		return flask.render_template("login.html")
	if flask.request.method.upper() == "POST":
		if not flask.request.form.get("username"):
			return "Invalid response?", 500
		if not flask.request.form.get("password"):
			return "Invalid response?", 500
		for _user_folder in listdir("./data/users"):
			user_folder:str = path.join("./data/users",_user_folder)
			with open(path.join(user_folder,"meta.json"),"r") as file:
				data:dict = load(file)
			if data["Name"] == flask.request.form.get("username"):
				with open(path.join(user_folder,"password.key"),"r") as file:
					password:str = file.read()
				if password == flask.request.form.get("password"):
					flask.session["user"] = data
					return flask.redirect("/app")
				else:
					return "Something was incorrect, idiot!"
		return "Something was incorrect, idiot!"
	return "The request was not understood", 500

site.run("localhost",4646)