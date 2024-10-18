import os
import re
import logging

from rest_framework.response import Response
from ..models import FolderConfig, LichessFile, get_next_db_url, LichessFile
from libs.wrap_log import log_function_call
from libs.zstd import decompress_zst_file
from ..config import ChessConfigManager
import requests

# Define a regex pattern to match filenames with any year and month
FILE_PATTERN = re.compile(r"lichess_db_standard_rated_(\d{4})-(\d{2})\.pgn\.zst")
logger = logging.getLogger('django')

def get_folder():
    # Fetch the folder configuration (assuming there's only one instance)
        config = FolderConfig.objects.first()
        if not config:
            return Response({'error': 'FolderConfig not found'}, status=404)

        # Construct the folder path
        zip_path = os.path.join(config.base_folder, config.zip_sub_folder)
        unzip_path = os.path.join(config.base_folder, config.unzip_sub_folder)
        return zip_path, unzip_path



@log_function_call
def check_new_lichess_file(request):
    try:
        zip_path, _ = get_folder()

        # List all files in the directory
        files_in_folder = os.listdir(zip_path)
        
        # Keep track of files added to the database
        added_files = []

        # Process each file in the directory
        for file_name in files_in_folder:
            match = FILE_PATTERN.match(file_name)
            if match:
                year, month = int(match.group(1)), int(match.group(2))
                # Check if the file is already in the database
                if not LichessFile.objects.filter(name=file_name).exists():
                    # Create a new LichessFiles entry
                    LichessFile.objects.create(
                        name=file_name,
                        year=year,
                        month=month,
                        status=LichessFile.DOWNLOAD  # Assuming DOWNLOAD = 0
                    )
                    added_files.append(file_name)

        if added_files:
            return Response({'message': f'New files added to the database: {", ".join(added_files)}'}, status=201)
        else:
            return Response({'message': 'No new files found'}, status=200)

    except Exception as e:
        print("Error")
        return Response({'error': str(e)}, status=500)
    
#
# New APIs
#

@log_function_call
def get_next_db_api(request):
    logger.info(f"Start API")
    try:
        url, filename, year, month = get_next_db_url()
        save_path = os.path.join(ChessConfigManager.get("download_folder"), filename)
        try:
            file_path = download_and_save_file(url, save_path)
            LichessFile.objects.create(
                name=filename,
                year=year,
                month=month,
                status=LichessFile.DOWNLOAD  # or any other status
            )
            return Response({"message": f"File saved to: {file_path}"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    except Exception as e:
        print("Error")
        return Response({'error': str(e)}, status=500)
    
def download_and_save_file(url: str, save_path: str):
    logger.info(f"Start Download")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as out_file:
            out_file.write(response.content)
        return save_path
    else:
        raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")

@log_function_call
def decom_new_lichess_file_api(request):
    try:
        zip_path = ChessConfigManager.get("download_folder")
        unzip_path = ChessConfigManager.get("unzip_folder")
        # List all files in the directory
        files_in_folder = os.listdir(zip_path)
        # Process each file in the directory
        for file_name in files_in_folder:
            match = FILE_PATTERN.match(file_name)
            if match:
                if LichessFile.objects.filter(name=file_name).filter(status=LichessFile.DOWNLOAD).exists():
                    decompress_zst_file(zip_path, unzip_path, file_name)
                    LichessFile.objects.filter(name=file_name).update(status=LichessFile.UNZIPPED)
                    os.remove(os.path.join(zip_path, file_name))
        return Response({"message": f"All files unzipped"}, status=200)
    except Exception as e:
        print("Error")
        return Response({'error': str(e)}, status=500)  