from typing import Protocol

from ... import IGraphPostAction

class ISharepointDocumentFolder(Protocol):
    def create_folder(self, relative_folder_path:str) -> IGraphPostAction:
        """"""
    
    def file(self, relative_file_path:str):
        """"""

    def build_url(self) -> str:
        """"""