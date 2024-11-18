from .BaseController import BaseController
from Database.VectorDB import VectorDB
from asyncinit import asyncinit
from llmlingua import PromptCompressor

@asyncinit
class RetrievalContoller(BaseController):
    
    async def __init__(self):
        super().__init__()
        self.k=6
        self.collection = await VectorDB.get_collection()
        self.prompt_compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        model_config={"revision": "main"},
        use_llmlingua2=True,
        device_map="cuda",
        )
    
    def run(self,query):
        
        documents = self.get_documents(query)
        
        query_info = self.process_documents(query,documents)

        compressed_prompt = self.prompt_compressor.compress_prompt(
        query_info['demonstration_str'], 
        instruction=query_info['instruction'],
        question=query_info['question'],
        target_token=400,
        rank_method="longllmlingua", 
        context_budget="+100",
        dynamic_context_compression_ratio=0.4,
        reorder_context="sort",
        )
        
        print(compressed_prompt)       
        return compressed_prompt['compressed_prompt']
        
    
    def process_documents(self,query,documents):
        
        formatted_docs = "\n\n".join(doc for doc in documents[0])
        
        
        query_info={
            'demonstration_str': formatted_docs,
            'instruction': "Write a high-quality answer for the given question using only the provided search results.",
            'question': query 
        }
        
        return query_info
    
    def get_documents(self,query):
        
        results = self.collection.query(
            query_texts=[query],
            n_results=self.k,
        )
        
        return results['documents']