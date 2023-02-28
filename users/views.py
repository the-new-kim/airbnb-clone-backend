import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status


from . import serializers
from .models import User

# Create your views here.


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    # def get(self, request):
    #     return Response({"ok": True})

    def post(self, request):
        print("DATA::::", request.data)
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            print("IS VALID!!!!")
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)

        else:
            print("NOT VALID!!!!")

            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print("USERNAME & PASSWORD:::", username, password)
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"ok": True})
        else:
            return Response({"error": "Wrong password"})


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye"})


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "Wrong password"})


class GithubLogin(APIView):
    def post(self, request):

        try:
            code = request.data.get("code")

            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=6a36b939bc38d508b1d9&client_secret={settings.GITHUB_SECRET}",
                headers={
                    "Accept": "application/json",
                },
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            try:
                user = User.objects.get(email=user_data.get("email"))
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_data.get("email"),
                    avatar=user_data.get("avatar_url"),
                    name=user_data.get("name"),
                )
                user.set_unusable_password()  # Only for OAuth login. loginig with using username & password will not allowed.
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#   try:
#             username = request.data.get("username")
#             name = request.data.get("name")
#             email = request.data.get("email")
#             password = request.data.get("password")

#             # try:
#             email_taken = User.objects.filter(email=email).exists()
#             username_taken = User.objects.filter(username=username).exists()
#             print("EMAIL TAKEN::::")

#             if email_taken or username_taken:
#                 if email_taken:
#                     print("EMAIL!")
#                     return Response(
#                         {"error": "This email has already been taken"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#                 else:
#                     print("USERNAME!")
#                     return Response(
#                         {"error": "This username has already been taken"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )

#             # except User.DoesNotExist:
#             print("USER DOES NOT EXIT")
#             user = User.objects.create(
#                 username=username,
#                 email=email,
#                 name=name,
#             )
#             print("USER::::", user)
#             user.set_password(password)
#             print("PASWORD SETTED")

#             user.save()
#             print("USER SAVED!")

#             login(request, user)
#             return Response(status=status.HTTP_200_OK)
#         except Exception:
#             print("SOMETHING WRONG")

#             return Response(status=status.HTTP_400_BAD_REQUEST)
