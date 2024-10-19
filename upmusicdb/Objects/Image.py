class Image:
	def __init__(self,image_id:int,file_extension:str,alt_text:str) -> None:
		self.__id:int = image_id
		self.__file_extension:str = file_extension
		self.__file_name:str = f"{self.__id}.{self.__file_extension}"
		self.__alt_text:str = alt_text
	
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
	
	@property
	def alt_text(self) -> str:
		return self.__alt_text
	@alt_text.setter
	def alt_text(self,new_alt_text) -> None:
		self.__alt_text = new_alt_text
