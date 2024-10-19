from .Artist import Artist
from .Image import Image
from .Audio import Audio

class Song:
	def __init__(self,song_id:int,name:str,artist:Artist,thumbnail:Image,audio:Audio):
		self.__id:int = song_id
		self.__name:str = name
		self.__artist:Artist = artist
		self.__thumbnail:Image = thumbnail
		self.__audio:Audio = audio
	
	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id
	
	@property
	def name(self) -> str:
		return self.__name
	@name.setter
	def name(self,new_name:str) -> None:
		self.__name = new_name
	
	@property
	def artist(self) -> Artist:
		return self.__artist
	@artist.setter
	def artist(self,new_artist:Artist) -> None:
		self.__artist = new_artist
	
	@property
	def thumbnail(self) -> Image:
		return self.__thumbnail
	@thumbnail.setter
	def thumbnail(self,new_thumbnail:Image) -> None:
		self.__thumbnail = new_thumbnail

	@property
	def audio(self) -> Audio:
		return self.__audio
	@audio.setter
	def audio(self,new_audio:Audio) -> None:
		self.__audio = new_audio
