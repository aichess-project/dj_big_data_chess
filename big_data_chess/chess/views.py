from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.lichess_rest_api import check_new_lichess_file  # Import the service

@api_view(['GET'])
def check_new_lichess_file_view(request):
    try:
        # Call the function that checks for new Lichess files
        return check_new_lichess_file(request)
    except Exception as e:
        # Catch any exceptions and return a generic error response
        return Response({'error': str(e)}, status=500)