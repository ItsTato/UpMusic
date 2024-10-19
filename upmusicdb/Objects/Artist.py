from .Image import Image

class Artist:
	def __init__(self,artist_id:int,name:str,bio:str,pfp:Image) -> None:
		self.__id:int = artist_id
		self.__name:str = name
		self.__bio:str = bio
		self.__pfp:Image = pfp
	
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
	def bio(self) -> str:
		return self.__bio
	@bio.setter
	def bio(self,new_bio:str) -> None:
		self.__bio = new_bio
	
	@property
	def pfp(self) -> Image:
		return self.__pfp
	@pfp.setter
	def pfp(self,new_pfp:Image) -> None:
		self.__pfp = new_pfp
