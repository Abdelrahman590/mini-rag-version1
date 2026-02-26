from fastapi import APIRouter,FastAPI ,Depends,UploadFile,status 
from fastapi.responses import JSONResponse
import os
from helpers.config  import get_settings, Settings
from controllers import DataController
from controllers import  ProjectController,ProcessController
import aiofiles 
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest

logger  = logging.getLogger("uvicorn.error")
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")

async def upload_data(project_id: str , file : UploadFile,app_sttings: Settings = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid ,result_signal = data_controller.validate_uploded_file(file=file)
    
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal" : result_signal})
  

    project_dir_path =  ProjectController().get_prject_path(project_id=project_id)
    file_path ,file_id  = data_controller.generate_unique_filepath (original_filename=file.filename,project_id=project_id)
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_sttings.FILE_DEFULT_CHUNK_SIZE):
            # Read the file in chunks
                await f.write(chunk)
    except Exception as  e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal" : ResponseSignal.FILE_UPLOADING_FAILED.value,"error":str(e)})
       
    return JSONResponse(
        content={
            "signal" : ResponseSignal.FILE_UPLODED_SUCCESS.value,
            "file_id":file_id
            }
        )
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest, app_sttings: Settings = Depends(get_settings)):
   file_id = process_request.file_id
   chunk_size = process_request.chunk_size
   overlap_size = process_request.overlap_size
   
   process_controller = ProcessController(project_id=project_id)
   file_content = process_controller.get_file_content(file_id=file_id)
   
   file_chunks = process_controller.process_file_content(file_content=file_content,file_id=file_id,chunk_size=chunk_size,chunk_overlap=overlap_size)
   
   if file_chunks is None or len(file_chunks) == 0:
       return JSONResponse(
           status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.PROCESSING_FAILED.value})
       
   return file_chunks 