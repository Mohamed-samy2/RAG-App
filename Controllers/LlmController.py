from .BaseController import BaseController
from langchain_google_genai import ChatGoogleGenerativeAI
from Database.VectorDB import VectorDB
from asyncinit import asyncinit

@asyncinit
class LlmController(BaseController):
    
    async def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI(
             model="gemini-1.5-flash",
            temperature=0,
            # max_tokens=None,
            # timeout=None,
            api_key=self.app_settings.GOOGLE_API_KEY,
            # max_retries=2,
            )
        self.k=3
        self.collection = await VectorDB.get_collection()
        
    async def run(self,query):
        return self.get_documents(query)
    
    
    def get_documents(self,query):
        
        results = self.collection.query(
            query_texts=[query],
            n_results=self.k,
        )
        
        return results
        