from rest_framework.response import Response
from rest_framework import status

from domain.models.Lookup import Lookup


def create_lookup(data):
    try:
        lookup = Lookup.objects.create(
            parent_id=data.get('parent_id'),
            name=data.get('name', ''),
            value=data.get('value', ''),
        )

        return Response({
            'message': 'Lookup created successfully',
            'id': str(lookup.id),
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)


def get_all_lookups():
    lookups = Lookup.objects.select_related('parent').values(
        'id',
        'parent_id',
        'name',
        'value',
        'created_on',
        'updated_on',
        'action_type',
    )

    return Response(list(lookups), status=status.HTTP_200_OK)


def get_lookup_by_id(lookup_id):
    lookup = Lookup.objects.filter(id=lookup_id).values(
        'id',
        'parent_id',
        'name',
        'value',
        'created_on',
        'updated_on',
        'action_type',
    ).first()

    if not lookup:
        return Response(
            {'message': 'Lookup not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(lookup, status=status.HTTP_200_OK)


def update_lookup(lookup_id, data):
    lookup = Lookup.objects.filter(id=lookup_id).first()

    if not lookup:
        return Response(
            {'message': 'Lookup not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if 'parent_id' in data:
        lookup.parent_id = data['parent_id']

    if 'name' in data:
        lookup.name = data['name']

    if 'value' in data:
        lookup.value = data['value']

    try:
        lookup.save()
        return Response(
            {'message': 'Lookup updated successfully'},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


def delete_lookup(lookup_id):
    lookup = Lookup.objects.filter(id=lookup_id).first()

    if not lookup:
        return Response(
            {'message': 'Lookup not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    lookup.delete()

    return Response(
        {'message': 'Lookup deleted successfully'},
        status=status.HTTP_200_OK,
    )