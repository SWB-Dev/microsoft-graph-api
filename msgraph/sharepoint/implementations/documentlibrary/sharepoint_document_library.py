from __future__ import annotations

import io
import requests

from .... import IGraphPutAction, IGraphPostAction
from ...abstractions.ISharepointDocumentFolder import ISharepointDocumentFolder
from ...abstractions.ISharepointSite import ISharepointSite
from .... import GraphResponseBase
from ...utilities.sharepoint_graph_client_base import SharepointGraphClientBase
from .actions.sharepoint_document_library_file_put import SharepointDocumentLibraryFilePUT

class SharepointDocumentLibrary:
    
    def __init__(self, library_name:str, parent:ISharepointSite, client:SharepointGraphClientBase):
        self.library_name = library_name
        self.parent = parent
        self.client = client
        self.graph_request = GraphResponseBase()
        self.client.add_request(self.graph_request)


    def folder(self, folder_name:str) -> ISharepointDocumentFolder:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()
    
    def file(self, relative_file_path:str):
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()
    
    def create_folder(self, relative_folder_path:str) -> IGraphPostAction:
        """TODO: NEEDS IMPLEMENTED"""
        raise NotImplementedError()

    
    def create_file(self, relative_file_path:str, stream:io.BufferedIOBase) -> IGraphPutAction:
        #Credit Hold/10192021.zip
        drive_uri = self.build_url()
        file_uri = f"{drive_uri}root:/{relative_file_path}:/content"
        return SharepointDocumentLibraryFilePUT(file_uri, self, stream, self.client)
    
    def build_url(self) -> str:
        library_id = self._get_library_id()
        library_uri = f"drives/{library_id}/"
        return library_uri
    
    def _get_library_id(self) -> str:
        site_uri = self.parent.build_url()
        libraries_url = f"{self.client.GRAPH_BASE_URI}{site_uri}drives?$select=id,name"
        library_resp = requests.get(libraries_url, headers=self.client.conn.headers)
        self.graph_request.add_response(library_resp)
        library_json = library_resp.json()

        if "value" in library_json.keys():
            for lib in library_json['value']:
                if lib['name'] == self.library_name:
                    return lib['id']
        
        if "error" in library_json.keys():
            print("Error in retreiving Document Library id.")
            print(library_json['error'])
            raise Exception("Error in retreiving Document Library id.")