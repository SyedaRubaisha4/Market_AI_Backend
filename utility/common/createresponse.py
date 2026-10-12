from rest_framework import status
from rest_framework.response import Response
from .responsemodel import ResponseModel, ResponseModelSerializer
from utility.helper.constant import ErrorCodes
import math

class CreateResponse:

    @staticmethod
    def success(serialized_data, message, error_code=int(ErrorCodes.SUCCESS), token=None,
                http_status=status.HTTP_200_OK):

        response = ResponseModel(
            error_code=error_code,
            result=serialized_data,
            message=message,
            page=0,
            success=True,
            page_size=None,
            total_pages=None,
            total_records=None,
            token=token
        )

        return Response(ResponseModelSerializer(response).data, status=http_status)

    @staticmethod
    def error(message, error_code=int(ErrorCodes.EXCEPTION), token=None,
              http_status=status.HTTP_400_BAD_REQUEST):

        response = ResponseModel(
            error_code=error_code,
            result=None,
            message=message,
            page=0,
            success=False,
            page_size=None,
            total_pages=None,
            total_records=None,
            token=token
        )

        return Response(ResponseModelSerializer(response).data, status=http_status)

    @staticmethod
    def no_record_found(message, error_code=int(ErrorCodes.NOT_EXIST), token=None,
                        http_status=status.HTTP_404_NOT_FOUND):

        response = ResponseModel(
            error_code=error_code,
            result=[],
            message=message,
            page=0,
            success=False,
            page_size=None,
            total_pages=None,
            total_records=None,
            token=token
        )

        return Response(ResponseModelSerializer(response).data, status=http_status)

    @staticmethod
    def paginated(serialized_data, message, page, page_size, total_records,
                  error_code=int(ErrorCodes.SUCCESS), token=None,
                  http_status=status.HTTP_200_OK):

        total_pages = 0 if not page_size else math.ceil((total_records or 0) / page_size)

        response = ResponseModel(
            result=serialized_data,
            page=page,
            page_size=page_size,
            success=True,
            total_records=total_records,
            error_code=error_code,
            message=message,
            total_pages=total_pages,
            token=token
        )

        return Response(ResponseModelSerializer(response).data, status=http_status)
