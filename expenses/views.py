from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Expense
from .serializers import RegisterSerializer, LoginSerializer, ExpenseSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'email': user.email, 'name': user.name,'user':"user created"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"Expense '{instance.description}' has been deleted."},
            status=status.HTTP_200_OK
        )    


class MonthlySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Expense.objects.filter(user=request.user)
        aggregated = qs.annotate(month=TruncMonth('date')) \
                       .values('month', 'category') \
                       .annotate(total=Sum('amount')) \
                       .order_by('month', 'category')
        result = [
            {'month': row['month'].strftime('%Y-%m'), 'category': row['category'], 'total': float(row['total'])}
            for row in aggregated
        ]
        return Response(result)
