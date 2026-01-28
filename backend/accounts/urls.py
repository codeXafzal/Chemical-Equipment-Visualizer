from django.urls import path
from .views import login_view, logout_view, protected_view, login_page

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('protected/', protected_view),
    path('test-login/', login_page),
]
