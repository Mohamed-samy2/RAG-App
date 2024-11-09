from fastapi import APIRouter , Depends
from fastapi.responses import JSONResponse
import os
from Helpers.configs import get_settings,Settings

base_router = APIRouter()

@base_router.get("/")
async def welcome(app_settings:Settings = Depends(get_settings)):
    app_settings = get_settings()
    
    app_name = app_settings.APP_NAME
    app_version= app_settings.APP_VERSION
    
    return JSONResponse(
        content={
            "app name": app_name,
            'app_version': app_version,
            'query':"Welcome to Document Chat How can i help you ?",
        }
    )