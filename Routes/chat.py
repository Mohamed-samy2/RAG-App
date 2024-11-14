from fastapi import APIRouter , status, Request,Depends
from fastapi.responses import JSONResponse
from Controllers import LlmController
from Helpers.Enums.ResponseEnum import Response
chat_router = APIRouter()

llm = None

async def get_llm_controller():
    return llm

@chat_router.on_event('startup')
async def startup_event():
    global llm
    if llm is None:
        llm = await LlmController() 
    

@chat_router.post("/chat")
async def process_endpoint(request:Request,query:str,llm: LlmController = Depends(get_llm_controller)):
    
    response = await llm.run(query)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'response':Response.CHAT_SUCCESS.value,
            'query':response,
        }
    )

