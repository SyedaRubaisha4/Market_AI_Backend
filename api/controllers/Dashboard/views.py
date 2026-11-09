from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication 

from .service import get_dashboard_stats

class DashboardStatsAPIView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Dashboard'],
        operation_summary="Get Dashboard Statistics",
        operation_description="Returns counts for Total Products, Generated, Published, Drafts, Pending, and Scheduled posts for the logged-in user.",
        responses={200: openapi.Response(description="Stats fetched successfully")}
    )
    def get(self, request):
        try:
            stats = get_dashboard_stats(request.user)
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)