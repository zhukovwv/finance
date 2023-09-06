from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer, BalanceSerializer


from ..authentication.models import UserProfile


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            balance = user_profile.balance
            serializer = BalanceSerializer(balance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found for the user.'}, status=status.HTTP_404_NOT_FOUND)


class TransactionList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        user_profile = UserProfile.objects.get(user=request.user)
        balance = user_profile.balance
        return Response({'transactions': serializer.data, 'balance': balance.amount}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListByCategory(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        transactions = Transaction.objects.filter(user=request.user, category_id=category_id)
        serializer = TransactionSerializer(transactions, many=True)
        user_profile = UserProfile.objects.get(user=request.user)
        balance = user_profile.balance
        return Response({'transactions': serializer.data, 'balance': balance.amount}, status=status.HTTP_200_OK)


class TransactionDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id, user=request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id, user=request.user)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, transaction_id):
        transaction = Transaction.objects.get(pk=transaction_id, user=request.user)
        transaction.delete()
        return Response({'message': 'Transaction deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
