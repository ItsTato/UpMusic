from . import Objects

from shutil import move
from .Controller import Controller

from sys import argv
argc:int = len(argv)
from os import path

def main(argv:list[str],argc:int):
	if argc == 1:
		while True:
			exec(input("UpMusicDB % "))
	if argc > 2:
		controller:Controller = Controller("./data/UpMusic.sqlite3")
		if argv[1] == "add":
			if argv[2] == "image":
				imageFileName:str = f"./{argv[argc-1]}"
				if not path.exists(imageFileName):
					print("[!] Image not found")
					exit()
				split = imageFileName.rsplit(".",1)
				imageExtension = split[1]
				image:Objects.Image = controller.newImage(imageExtension.lower())
				move(imageFileName,f"./data/images/{image.id}.{image.file_extension}")
				exit()
			if argv[2] == "artist":
				name:str = input("Name: ")
				pfp_id:int = int(input("Pfp ID: "))
				pfp:Objects.Image|None = controller.getImage(pfp_id)
				if pfp is None:
					print("[!] Image ID is invalid")
					exit()
				controller.newArtist(name,pfp)
				exit()
			if argv[2] == "audio":
				audioFileName:str = f"./{argv[argc-1]}"
				if not path.exists(audioFileName):
					print("[!] Audio not found")
					exit()
				split = audioFileName.rsplit(".",1)
				audioExtension = split[1]
				audio:Objects.Audio = controller.newAudio(audioExtension.lower())
				move(audioFileName,f"./data/audios/{audio.id}.{audio.file_extension}")
				exit()
			if argv[2] == "song":
				name:str = input("Name: ")
				artist_id:int = int(input("Artist ID: "))
				thumbnail_id:int = int(input("Thumbnail ID: "))
				thumbnail:Objects.Image|None = controller.getImage(thumbnail_id)
				artist:Objects.Artist|None = controller.getArtist(artist_id)
				if thumbnail is None:
					print("[!] Image ID is invalid")
					exit()
				if artist is None:
					print("[!] Artist ID is invalid")
					exit()
				controller.newSong(name,artist,thumbnail)
				exit()

main(argv,argc)
