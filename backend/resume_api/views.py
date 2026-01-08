from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from predictor.ats_checks import analyze_resume


class ResumePredictView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("resume")

        if not file:
            return Response({"error": "Resume file is required"}, status=400)

        try:
            return Response(analyze_resume(file))
        except Exception as e:
            return Response({"error": str(e)}, status=500)