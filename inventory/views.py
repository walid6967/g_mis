from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Inventory
from .serializers import InventorySerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def inventories(request):
    try:
        name = request.query_params.get('name', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        inventories = Inventory.objects.filter(is_deleted=False)
        if name:
            inventories = inventories.filter(name__icontains=name)
        if order_by:
            inventories = inventories.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                inventories = inventories[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_inventory(request, id):
    try:
        inventory = Inventory.objects.get(pk=id,is_deleted=False)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_inventory(request):
    try:
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_inventory(request, id):
    try:
        inventory = Inventory.objects.get(pk=id, is_deleted=False)
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_inventory(request, id):
    try:
        inventory = Inventory.objects.get(pk=id)
        inventory.is_deleted=True
        inventory.save()
        return Response({"message": "Inventory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
