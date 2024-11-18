from .BaseController import BaseController
from langchain_google_genai import ChatGoogleGenerativeAI
from Database.VectorDB import VectorDB
from langchain_core.messages import     HumanMessage,SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from .RetrievalController import RetrievalContoller
from asyncinit import asyncinit

@asyncinit
class LlmController(BaseController):
    
    async def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            # max_tokens=500,
            # timeout=None,
            api_key=self.app_settings.GOOGLE_API_KEY,
            max_retries=2,
            )
        
        self.prompt_compressor = await RetrievalContoller()
        self.memory = ConversationBufferWindowMemory(k=4)
                
    async def run(self,query):
        documents = self.prompt_compressor.run(query)
        
        
        memory_summary = self.memory.load_memory_variables({}).get("history", "")
        
        template = (
        "Use This Memory that can might help you answer the question"
        f"{memory_summary}\n\n"
        f"and Use These documents that might help answer the question:"
        f"{query}\n\n"
        "\n\n Relevant Documents:\n"
        f"{documents}\n\n"
        "\n\n Please provide answer based only on provided documents and the memory"
        "if you don't know the answer , just say that you don't know."
        )
        
        messages = [
        SystemMessage(content="you are a helpful assistant that answer questions"),
        HumanMessage(content= template)
        ]
        
        prompt_template = ChatPromptTemplate.from_messages(messages)
        
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke({"query":query,"documents":documents,'memory_summary':memory_summary})    
        
        self.memory.save_context(
            {"query": query},
            {"response": result}
        )
            
        return result
    
        