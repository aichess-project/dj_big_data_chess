import os
import re

from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import FolderConfig, LichessFile
from django.conf import settings

logger = settings.ELK_LOGGER  # Accessing the logger

# Define a regex pattern to match filenames with any year and month
FILE_PATTERN = re.compile(r"lichess_db_standard_rated_(\d{4})-(\d{2})\.pgn\.zst")

def check_new_lichess_file(request):
    fkt_name = "check_new_lichess_file"
    try:
        logger.info("Starting API call", function=fkt_name)
        # Fetch the folder configuration (assuming there's only one instance)
        config = FolderConfig.objects.first()
        if not config:
            return Response({'error': 'FolderConfig not found'}, status=404)

        # Construct the folder path
        folder_path = os.path.join(config.base_folder, config.zip_sub_folder)
        print(folder_path)
        
        # List all files in the directory
        files_in_folder = os.listdir(folder_path)
        print(files_in_folder)
        
        # Keep track of files added to the database
        added_files = []

        # Process each file in the directory
        for file_name in files_in_folder:
            print(file_name)
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

        logger.info("Ending API call", status=200, function=fkt_name)
        if added_files:
            return Response({'message': f'New files added to the database: {", ".join(added_files)}'}, status=201)
        else:
            return Response({'message': 'No new files found'}, status=200)

    except Exception as e:
        logger.info(f"error: {e}", status=500, function=fkt_name)
        return Response({'error': str(e)}, status=500)
