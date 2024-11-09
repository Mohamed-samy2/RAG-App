import os
import asyncio
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from Helpers.configs import get_settings
# from dotenv import load_dotenv
# load_dotenv()

class VectorDB:
    __instance = None
    
    @classmethod    
    async def get_collection(cls): 
        if cls.__instance is None:
            cls.__instance = super(VectorDB, cls).__new__(cls)
            cls.__instance.__client = None
            cls.__instance.__collection_name = None
            cls.__instance.__collection = None
            cls.__instance.__embedding_model = None  
            
            await cls.__instance.__connect__()
        return cls.__instance.__collection

    async def __connect__(self):
        self.app_settings = get_settings()
        self.__collection_name = self.app_settings.COLLECTION_NAME
        try: 
            self.__client = chromadb.PersistentClient(path='Database/')
            print("Connected to Chroma Vector Database Client")
        except Exception as error:
            print("Failed to connect to ChromaDB client:", error)
        
        try:
            self.__embedding_model = embedding_functions.GoogleGenerativeAiEmbeddingFunction(self.app_settings.GOOGLE_API_KEY)
            print("Initialized Google Embedding Model")
        except Exception as error:
            print("Failed to load the Google Embedding model:", error)
        
        try:
            self.__collection = self.__client.get_or_create_collection(
                name=self.__collection_name,
                embedding_function=self.__embedding_model,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Collection '{self.__collection_name}' created with the embedding model.")
        except Exception as e:
            print(f"Failed to create {self.__collection_name}: {e}")


async def main():
    db = await VectorDB.get_collection()
    print(db)
if __name__ == "__main__":
    asyncio.run(main())

