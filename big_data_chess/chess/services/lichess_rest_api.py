import os
import re
import logging

from rest_framework.response import Response
from ..models import FolderConfig, LichessFile
from libs.wrap_log import log_function_call

# Define a regex pattern to match filenames with any year and month
FILE_PATTERN = re.compile(r"lichess_db_standard_rated_(\d{4})-(\d{2})\.pgn\.zst")
logger = logging.getLogger('django')

@log_function_call
def check_new_lichess_file(request):
    try:
        logger.info("Processing request", extra={'status': 'started', 'operation': 'example_view', 'value': '1'})
        # Perform some operation
        logger.info("Request processed successfully", extra={'status': 'ok', 'operation': 'example_view', 'value': '2'})
 
        # Fetch the folder configuration (assuming there's only one instance)
        config = FolderConfig.objects.first()
        if not config:
            return Response({'error': 'FolderConfig not found'}, status=404)

        # Construct the folder path
        folder_path = os.path.join(config.base_folder, config.zip_sub_folder)

        # List all files in the directory
        files_in_folder = os.listdir(folder_path)
        
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
