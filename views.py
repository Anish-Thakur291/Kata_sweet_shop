from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from decimal import Decimal

from .models import Sweet
from .serializers import (
    UserRegistrationSerializer, UserSerializer, SweetSerializer,
    PurchaseSerializer, RestockSerializer
)
from .permissions import IsAdminUser, IsAdminOrReadOnly


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class SweetListCreateView(generics.ListCreateAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class SweetSearchView(generics.ListAPIView):
    serializer_class = SweetSerializer
    # Allow unauthenticated users to search the catalog
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Sweet.objects.all()
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category=category)
        if min_price:
            queryset = queryset.filter(price__gte=Decimal(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=Decimal(max_price))

        return queryset


class SweetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_sweet(request, pk):
    try:
        sweet = Sweet.objects.get(pk=pk)
    except Sweet.DoesNotExist:
        return Response(
            {'error': 'Sweet not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PurchaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    quantity = serializer.validated_data.get('quantity', 1)

    if sweet.quantity < quantity:
        return Response(
            {'error': f'Not enough stock. Available: {sweet.quantity}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    sweet.quantity -= quantity
    sweet.save()
    return Response({
        'message': f'Successfully purchased {quantity} {sweet.name}(s)',
        'sweet': SweetSerializer(sweet).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def restock_sweet(request, pk):
    try:
        sweet = Sweet.objects.get(pk=pk)
    except Sweet.DoesNotExist:
        return Response(
            {'error': 'Sweet not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = RestockSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    quantity = serializer.validated_data['quantity']
    sweet.quantity += quantity
    sweet.save()
    return Response({
        'message': f'Successfully restocked {quantity} {sweet.name}(s)',
        'sweet': SweetSerializer(sweet).data
    })
