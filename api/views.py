from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello Market AI!"}, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get("name", "Guest")
        return Response({"message": f"Hello {name}!"}, status=status.HTTP_201_CREATED)