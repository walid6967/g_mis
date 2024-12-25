from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from inventory.models import Inventory
from supplier.models import Supplier
from account.models import Account

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions(request):
    try:
        name = request.query_params.get('name', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        transactions = Transaction.objects.filter(is_deleted=False)
        if name:
            transactions = transactions.filter(name__icontains=name)
        if order_by:
            transactions = transactions.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                transactions = transactions[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id,is_deleted=False)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    try:
        serializer = TransactionSerializer(data=request.data)
        
        # Access raw data from request
        inv_id = request.data.get('inventory')
        supplier_id = request.data.get('supplier')
        quantity = request.data.get('quantity')

        # Retrieve related objects
        inventory = Inventory.objects.get(id=inv_id, is_deleted=False)
        supplier = Supplier.objects.get(id=supplier_id, is_deleted=False)
        account = Account.objects.get(id=supplier.account.pk)
        
        # Calculate transaction amount
        trans_amount = int(quantity) * inventory.price
        
        # Deduct amount from user's account balance
        if account.balance < trans_amount:
            return Response(
                {"error": "Insufficient balance in account."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deduct stock and balance
        account.balance -= trans_amount
        account.save()

        # Validate and save transaction
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Inventory.DoesNotExist:
        return Response({"error": "Inventory item does not exist or is deleted."}, status=status.HTTP_404_NOT_FOUND)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier does not exist or is deleted."}, status=status.HTTP_404_NOT_FOUND)
    except Account.DoesNotExist:
        return Response({"error": "Account associated with supplier does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id, is_deleted=False)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, id):
    try:
        transaction = Transaction.objects.get(pk=id)
        transaction.is_deleted=True
        transaction.save()
        return Response({"message": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
