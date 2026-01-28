from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from equipment.views import UploadCSVView, HistoryView, home
def home(request):
    return JsonResponse({"message": "Backend running"})

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path('accounts/', include('accounts.urls')),
   

    # API routes ✅
    path("api/upload/", UploadCSVView.as_view(), name="upload-csv"),
    path("api/history/", HistoryView.as_view(), name="history"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
