from .BaseController import BaseController
from fastapi import UploadFile
from Helpers.Enums.ResponseEnum import Response


class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
    
    def run(self,file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False , Response.FILE_TYPE_NOT_SUPPORTED.value
        
        return True , Response.FILE_UPLOADED_SUCCESS.value