from .Objects import Artist, Audio, Image, Song

import sqlite3
import os

class Controller:
	def __init__(self,location:str) -> None:
		try:
			self.__connection = sqlite3.connect(location,check_same_thread=False)
		except:
			print(f"Could not connect to database at {location}")
			exit()
		cursor = self.__connection.cursor()
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS "Images" (
			"ID" INTEGER NOT NULL UNIQUE,
			"FileExtension" TEXT NOT NULL DEFAULT 'png',
			"AltText" TEXT NOT NULL DEFAULT 'This image has no set definition.',
			PRIMARY KEY("ID" AUTOINCREMENT)
		);
		""")
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS "Audios" (
			"ID" INTEGER NOT NULL UNIQUE,
			"FileExtension" TEXT NOT NULL DEFAULT 'mp3',
			PRIMARY KEY("ID" AUTOINCREMENT)
		);
		""")
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS "Artists" (
			"ID" INTEGER NOT NULL UNIQUE,
			"Name" TEXT NOT NULL,
			"Bio" TEXT NOT NUll DEFAULT 'No bio yet...',
			"PfpID" INTEGER NOT NULL,
			PRIMARY KEY("ID" AUTOINCREMENT)
		);
		""")
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS "Songs" (
			"ID" INTEGER NOT NULL UNIQUE,
			"Name" TEXT NOT NULL,
			"ArtistID" INTEGER NOT NULL,
			"ThumbnailID" INTEGER NOT NULL,
			"AudioID" INTEGER NOT NULL,
			PRIMARY KEY("ID" AUTOINCREMENT)
		);
		""")
		self.__connection.commit()
	
	def Close(self) -> None:
		self.__connection.close()
	
	def getImage(self,image_id:int) -> Image|None:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Images WHERE ID = ?",(image_id,))
		raw_image:tuple[int,str,str]|None = cursor.fetchone()
		if raw_image is None:
			return
		image:Image = Image(
			raw_image[0],
			raw_image[1],
			raw_image[2]
		)
		return image
	
	def deleteImage(self,image_id:int) -> None:
		image:Image|None = self.getImage(image_id)
		if image is None:
			return
		os.remove(f"./data/images/{image.file_name}")
		cursor = self.__connection.cursor()
		cursor.execute("DELETE FROM Images WHERE ID = ?",(image_id,))
		self.__connection.commit()
		return
	
	def newImage(self,file_extension:str) -> Image:
		cursor = self.__connection.cursor()
		cursor.execute("INSERT INTO Images (FileExtension) Values(?)",(file_extension,))
		self.__connection.commit()
		return self.getImage(cursor.lastrowid)#type:ignore
	
	def getAllImages(self) -> list[Image]:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Images")
		raw_images:list[tuple[int,str,str]] = cursor.fetchall()
		if raw_images is None:
			return []
		images:list[Image] = []
		for raw_image in raw_images:
			image:Image = Image(
				raw_image[0],
				raw_image[1],
				raw_image[2]
			)
			images.append(image)
		return images
	
	def getAudio(self,audio_id:int) -> Audio|None:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Audios WHERE ID = ?",(audio_id,))
		raw_audio:tuple[int,str]|None = cursor.fetchone()
		if raw_audio is None:
			return
		audio:Audio = Audio(
			raw_audio[0],
			raw_audio[1]
		)
		return audio
	
	def deleteAudio(self,audio_id:int) -> None:
		audio:Audio|None = self.getAudio(audio_id)
		if audio is None:
			return
		os.remove(f"./data/audios/{audio.file_name}")
		cursor = self.__connection.cursor()
		cursor.execute("DELETE FROM Audios WHERE ID = ?",(audio_id,))
		self.__connection.commit()
		return
	
	def newAudio(self,file_extension:str) -> Audio:
		cursor = self.__connection.cursor()
		cursor.execute("INSERT INTO Audios (FileExtension) Values(?)",(file_extension,))
		self.__connection.commit()
		return self.getAudio(cursor.lastrowid)#type:ignore
	
	def getAllAudios(self) -> list[Audio]:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Audios")
		raw_audios:list[tuple[int,str]] = cursor.fetchall()
		if raw_audios is None:
			return []
		audios:list[Audio] = []
		for raw_audio in raw_audios:
			audio:Audio = Audio(
				raw_audio[0],
				raw_audio[1]
			)
			audios.append(audio)
		return audios
	
	def getArtist(self,artist_id:int) -> Artist|None:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Artists WHERE ID = ?",(artist_id,))
		raw_artist:tuple[int,str,str,int]|None = cursor.fetchone()
		if raw_artist is None:
			return
		artist:Artist = Artist(
			raw_artist[0],
			raw_artist[1],
			raw_artist[2],
			self.getImage(raw_artist[3])#type:ignore
		)
		return artist
	
	def deleteArist(self,artist_id:int) -> None:
		artist:Artist|None = self.getArtist(artist_id)
		if artist is None:
			return
		cursor = self.__connection.cursor()
		cursor.execute("DELETE FROM Artists WHERE ID = ?",(artist_id,))
		self.__connection.commit()
		return
	
	def newArtist(self,name:str,pfp:Image) -> Artist:
		cursor = self.__connection.cursor()
		cursor.execute("INSERT INTO Artists (Name,PfpID) Values(?,?)",(name,pfp.id))
		self.__connection.commit()
		return self.getArtist(cursor.lastrowid)#type:ignore
	
	def getAllArtists(self) -> list[Artist]:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Artists")
		raw_artists:list[tuple[int,str,str,int]] = cursor.fetchall()
		if raw_artists is None:
			return []
		artists:list[Artist] = []
		for raw_artist in raw_artists:
			artist:Artist = Artist(
				raw_artist[0],
				raw_artist[1],
				raw_artist[2],
				self.getImage(raw_artist[3])#type:ignore
			)
			artists.append(artist)
		return artists
	
	def getSong(self,song_id:int) -> Song|None:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Songs WHERE ID = ?",(song_id,))
		raw_song:tuple[int,str,int,int,int]|None = cursor.fetchone()
		if raw_song is None:
			return
		song:Song = Song(
			raw_song[0],
			raw_song[1],
			self.getArtist(raw_song[2]),#type:ignore
			self.getImage(raw_song[3]),#type:ignore
			self.getAudio(raw_song[4])#type:ignore
		)
		return song
	
	def deleteSong(self,song_id:int) -> None:
		song:Song|None = self.getSong(song_id)
		if song is None:
			return
		cursor = self.__connection.cursor()
		cursor.execute("DELETE FROM Songs WHERE ID = ?",(song_id,))
		self.__connection.commit()
		return
	
	def newSong(self,name:str,artist:Artist,thumbnail:Image,audio:Audio) -> Song:
		cursor = self.__connection.cursor()
		cursor.execute("INSERT INTO Songs (Name,ArtistID,ThumbnailID,AudioID) Values(?,?,?,?)",(name,artist.id,thumbnail.id,audio.id))
		self.__connection.commit()
		return self.getSong(cursor.lastrowid)#type:ignore
	
	def getAllSongs(self) -> list[Song]:
		cursor = self.__connection.cursor()
		cursor.execute("SELECT * FROM Songs")
		raw_songs:list[tuple[int,str,int,int,int]] = cursor.fetchall()
		if raw_songs is None:
			return []
		songs:list[Song] = []
		for raw_song in raw_songs:
			song:Song = Song(
				raw_song[0],
				raw_song[1],
				self.getArtist(raw_song[2]),#type:ignore
				self.getImage(raw_song[3]),#type:ignore
				self.getAudio(raw_song[4])#type:ignore
			)
			songs.append(song)
		return songs
