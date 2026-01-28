from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


# -------- UI TEST PAGE --------
def login_page(request):
    return render(request, "login.html")


# -------- API LOGIN --------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse(
            {"error": "Username and password required"},
            status=400
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=400
        )

    login(request, user)
    return JsonResponse({"message": "Login successful"})


# -------- API LOGOUT --------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


# -------- PROTECTED API --------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return JsonResponse({
        "message": "You are authenticated",
        "user": request.user.username
    })
