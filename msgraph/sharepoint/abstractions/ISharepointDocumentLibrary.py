import io
from typing import Protocol

from ... import IGraphAction
from .ISharepointDocumentFolder import ISharepointDocumentFolder

class ISharepointDocumentLibrary(Protocol):
    def folder(self, folder_name:str) -> ISharepointDocumentFolder:
        """"""
    
    def file(self, relative_file_path:str):
        """"""
    
    def create_folder(self, relative_folder_path:str) -> IGraphAction:
        """"""
    
    def create_file(self, relative_file_path:str, stream:io.BufferedIOBase) -> IGraphAction:
        """"""
    
    def build_url(self) -> str:
        """"""