from rest_framework.decorators import api_view
from api.controllers.Product.service import get_products
from .service import (
    create_or_update_schedule,
    get_schedule_by_id,
    delete_schedule,
    get_all_schedules)
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST', 'PUT', 'PATCH'])
def view_add_or_update_schedule(request):
    return create_or_update_schedule(
        request.data,
        request=request
    )
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_get_all_schedules(request):
    return get_all_schedules(request) 

@api_view(['GET'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])         
def view_get_schedule_by_id(request, schedule_id):
    return get_schedule_by_id(schedule_id)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
def view_delete_schedule(request, schedule_id):
    return delete_schedule(schedule_id)