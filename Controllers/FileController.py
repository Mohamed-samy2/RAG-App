from .BaseController import BaseController
import os
from Helpers.Enums.ProcessingEnum import ProcessingEnum
from fastapi import UploadFile
import shutil
from chromadb.utils.batch_utils import create_batches
import aiofiles


class FileController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temporary files")
    
    def generate_filepath(self,upload_file:UploadFile):
        os.makedirs(self.temp_dir, exist_ok=True)
        file_path = os.path.join(self.temp_dir, upload_file.filename)
        
        return file_path
    
    async def run(self,upload_file:UploadFile):
        
        file_path = self.generate_filepath(upload_file=upload_file)
        async with aiofiles.open(file_path,'wb') as f :
            while chunk:= await upload_file.read(512000):
                await f.write(chunk)
        
        return file_path
    
    def remove_file(self):
        shutil.rmtree(self.temp_dir)
        