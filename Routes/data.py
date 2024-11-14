from fastapi import APIRouter , Depends,UploadFile , status, Request
from fastapi.responses import JSONResponse
from Controllers import ProcessController,DataController,FileController
from Helpers.Enums.ResponseEnum import Response

data_router = APIRouter()

@data_router.post("/upload")
async def process_endpoint(request:Request,file:UploadFile):
    data_controller = DataController()
    is_valid,response = data_controller.run(file=file)
    
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "query": response
            }
        )
    
    
    file_controller = FileController()
    
    file_path = await file_controller.run(file)
    
    process_controller = await ProcessController()
    no_records = await  process_controller.run(file_path=file_path)
    
    
    if no_records == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "query": Response.FILE_UPLOADED_FAILED.value,   
            }
        )
    
    file_controller.remove_file()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "query":Response.FILE_UPLOADED_SUCCESS.value,
            "Inserted Chunks": no_records,
            'File name':file.filename,
        }
    )
    
