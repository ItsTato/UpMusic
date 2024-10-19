class Audio:
	def __init__(self,audio_id:int,file_extension:str):
		self.__id:int = audio_id
		self.__file_extension:str = file_extension
		self.__file_name:str = f"{audio_id}.{self.__file_extension.lower()}"

	@property
	def id(self) -> int:
		return self.__id
	@id.setter
	def id(self,new_id:int) -> None:
		self.__id = new_id
	
	@property
	def file_extension(self) -> str:
		return self.__file_extension
	@file_extension.setter
	def file_extension(self,new_extension:str) -> None:
		self.__file_extension = new_extension

	@property
	def file_name(self) -> str:
		return self.__file_name
