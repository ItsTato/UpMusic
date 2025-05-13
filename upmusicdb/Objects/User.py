import bcrypt

from .Image import Image
from .Playlist import Playlist

class User:
	def __init__(self,_id:int,username:str,password_hash:str,liked_songs:Playlist,playlists:list[Playlist],pfp:Image,admin:int|bool) -> None:
		self.id:int = _id
		self.username:str = username
		self.passwordHash:bytes = password_hash.encode("UTF-8")
		self.liked_songs:Playlist = liked_songs
		self.playlists:list[Playlist] = playlists
		self.pfp:Image = pfp
		self.admin:bool = admin if isinstance(admin,bool) else (True if admin == 1 else False)

	def verifyPassword(self,password:str) -> bool:
		return bcrypt.checkpw(password.encode("UTF-8"),self.passwordHash)
