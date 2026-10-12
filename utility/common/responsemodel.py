from rest_framework import serializers
from typing import Generic, TypeVar, Union, Optional

T = TypeVar("T")


class ResponseModel():
    error_code: int
    success: bool
    result: Optional[T] = None
    message: str
    page: int
    total_records: int
    page_size: int
    total_pages: int
    token: str = None

    def __init__(self, error_code: int, result, message: str, page: int, page_size: int, success: bool,
                 total_records: int, total_pages: int, token: str = None):
        self.error_code = error_code
        self.success = success
        self.result = result
        self.message = message
        self.page = page
        self.total_records = total_records
        self.page_size = page_size
        self.total_pages = total_pages
        self.token = token


class ResponseModelSerializer(serializers.Serializer):
    error_code = serializers.IntegerField()
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=500)
    result = serializers.JSONField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total_records = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    token = serializers.CharField(max_length=1000, required=False)

    class Meta:
        model = ResponseModel