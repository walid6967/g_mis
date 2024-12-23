from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Supplier
from .serializers import SupplierSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_list(request):
    try:
        name = request.query_params.get('name', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        suppliers = Supplier.objects.filter(is_deleted=False)
        if name:
            suppliers = suppliers.filter(name__icontains=name)
        if order_by:
            suppliers = suppliers.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                suppliers = suppliers[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_detail(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk,is_deleted=False)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def supplier_create(request):
    try:
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def supplier_update(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk, is_deleted=False)
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supplier_delete(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk, is_deleted=False)
        supplier.is_deleted=True
        supplier.save()
        return Response({"message": "Supplier deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
