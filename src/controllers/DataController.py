from fastapi import UploadFile
from .BaseController import BaseController
from .Project_Controller import ProjectController
from models import ResponseSignal
import re
import os 


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
    def validate_uploded_file (self,file):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * 1024 * 1024:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True ,ResponseSignal.FILE_UPLODED_SUCCESS.value
    
    def generate_unique_filepath(self, original_filename: str, project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_prject_path(project_id=project_id)

        clean_file_name = self.get_clean_file_name(
        org_file_name=original_filename,
        project_id=project_id
        )

        new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

    # Loop until we get a non-existing file path
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

        return new_file_path , f"{random_key}_{clean_file_name}"


    
    def get_clean_file_name (self,org_file_name : str ,project_id:str):
        
        clean_file_name= re.sub(r'[^\w. ]', '', org_file_name.strip())
        
        clean_file_name = clean_file_name.replace(" ", "_")
        
        return clean_file_name