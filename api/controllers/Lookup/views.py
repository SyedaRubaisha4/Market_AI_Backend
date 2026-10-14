from rest_framework.decorators import api_view
from .service import (
    create_lookup,
    get_all_lookups,
    get_lookup_by_id,
    update_lookup,
    delete_lookup,
)


@api_view(['POST'])
def view_add_lookup(request):
    return create_lookup(request.data)


@api_view(['GET'])
def view_get_lookups(request):
    return get_all_lookups()


@api_view(['GET'])
def view_get_lookup_by_id(request, lookup_id):
    return get_lookup_by_id(lookup_id)


@api_view(['PUT', 'PATCH'])
def view_update_lookup(request, lookup_id):
    return update_lookup(lookup_id, request.data)


@api_view(['DELETE'])
def view_delete_lookup(request, lookup_id):
    return delete_lookup(lookup_id)