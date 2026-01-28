

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.http import HttpResponse



from .models import Dataset
from .utils import analyze_csv
from .serializers import CSVUploadSerializer


class UploadCSVView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CSVUploadSerializer

    def get(self, request):
        return Response({
            "message": "Upload a CSV file using POST (form-data, key = file)"
        })

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        summary, data = analyze_csv(file)

        Dataset.objects.create(
            file=file,
            summary=summary,
            columns=list(data[0].keys()) if data else []
        )

        return Response(
            {
                "summary": summary,
                "data": data
            },
            status=status.HTTP_201_CREATED
        )


class HistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        datasets = Dataset.objects.all().order_by("-created_at")
        return Response([d.summary for d in datasets])


def home(request):
    return HttpResponse("Chemical Equipment Visualizer is running 🚀")