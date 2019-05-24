from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Rest imports
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

       
class Login(APIView):
	def post(self, request, format="json"):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request,user)
			return Response({
                        "user_status":user.is_authenticated, 
						"is_superuser": user.is_superuser
                        },
						status=status.HTTP_200_OK)
		else:
			return Response({"user_status":False}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    
    def get(self,request,format="json"):
        """
            Destroys user's logged in session
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def user_authentication_status(request):
    """
        User frontend authentication verifier
        unauthenticated function - returns dict with rest status
    """
    authentication_dict = {
            'user_status': request.user.is_authenticated
        }
    if(request.user.is_authenticated):
        authentication_dict['is_superuser'] = request.user.is_superuser

    return Response(authentication_dict, status.HTTP_200_OK)
