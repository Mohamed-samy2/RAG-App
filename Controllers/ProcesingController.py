from .BaseController import BaseController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Helpers.Enums.ProcessingEnum import ProcessingEnum
from Database.VectorDB import VectorDB
from asyncinit import asyncinit
import time


@asyncinit
class ProcessController(BaseController):
    async def __init__(self):
        super().__init__()
        self.__collection = await VectorDB.get_collection()
        
    def get_file_extension(self, file_path: str) -> str:
        return os.path.splitext(file_path)[-1]
    
    def get_file_loader(self,file_path:str):
        
        file_ext = self.get_file_extension(file_path=file_path)
                
        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path=file_path,encoding='utf-8')
        
        elif file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path= file_path)
        
        else:
            return None
        
    
    def get_file_content(self,file_path:str):
        loader = self.get_file_loader(file_path=file_path)
        return loader.load()
        
        
    async def process_file_content(self,file_content:list, chunk_size :int = 1100 , overlap_size :int=200):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = overlap_size,
            length_function = len,
            # separators=[r"\n\n", r"\n", r"\s+",r" {2,}"],
            # is_separator_regex=True,
        )
        
        chunks = await text_splitter.atransform_documents(
            documents=file_content,
        )

        return chunks

    async def insert_chunks(self,chunks:list,batch_size:int = 100):
        
        start = time.time()
        for i in range(0,len(chunks),batch_size):
            
            # Get the current batch
            batch = chunks[i:i + batch_size]
            # Extract documents, metadata, and IDs for the batch
            documents = [chunk.page_content for chunk in batch]
            metadatas = [chunk.metadata for chunk in batch]
            ids = [f'{os.path.basename(metadatas[0]['source'])}_chunk_{i + j}' for j in range(len(batch))]
            
            self.__collection.add(documents=documents,
                                 metadatas=metadatas,
                                 ids=ids
                                 )
        
        elapsed_time = time.time() - start
        print(f"Elapsed Time {elapsed_time}")
            
        return len(chunks)
    
    async def run(self,file_path:str):
        
        loader = self.get_file_content(file_path=file_path)
        chunks = await self.process_file_content(loader)
        num_chunks = await self.insert_chunks(chunks=chunks)
        
        return num_chunks
        
