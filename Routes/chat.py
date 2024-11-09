from fastapi import APIRouter , status, Request,Query
from fastapi.responses import JSONResponse
from Controllers import LlmController
from Helpers.Enums.ResponseEnum import Response
chat_router = APIRouter()

@chat_router.post("/chat")
async def process_endpoint(request:Request,query:str):
    
    llm = await LlmController()
    
    response = await llm.run(query)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'response':Response.CHAT_SUCCESS.value,
            'query':response['documents'],
        }
    )

