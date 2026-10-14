from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, UserSerializer
class RegisterView(generics.CreateAPIView):
 serializer_class=RegisterSerializer
 permission_classes=[permissions.AllowAny]
class MeView(generics.RetrieveAPIView):
 serializer_class=UserSerializer
 def get_object(self): return self.request.user
class LogoutView(APIView):
 def post(self,request):
  token=request.data.get("refresh")
  if not token: return Response({"detail":"refresh token is required"},status=400)
  try: RefreshToken(token).blacklist()
  except TokenError: return Response({"detail":"Invalid or expired refresh token"},status=400)
  return Response(status=status.HTTP_205_RESET_CONTENT)
