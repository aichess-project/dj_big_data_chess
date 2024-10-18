from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.lichess_rest_api import check_new_lichess_file, decom_new_lichess_file_api, get_next_db_api  # Import the service
import logging

logger = logging.getLogger('django')

@api_view(['GET'])
def check_new_lichess_file_view(request):
    try:
        # Call the function that checks for new Lichess files
        return check_new_lichess_file(request)
    except Exception as e:
        # Catch any exceptions and return a generic error response
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def decom_file(request):
    try:
        # Call the function that checks for new Lichess files
        return decom_new_lichess_file_api(request)
    except Exception as e:
        # Catch any exceptions and return a generic error response
        return Response({'error': str(e)}, status=500)
    
#
# New APIs
#
@api_view(['GET'])
def get_next_db_view(request):
    try:
        # Call the function that checks for new Lichess files
        return get_next_db_api(request)
    except Exception as e:
        # Catch any exceptions and return a generic error response
        return Response({'error': str(e)}, status=500)
