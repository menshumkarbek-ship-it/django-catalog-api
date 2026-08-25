from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Product, Review
from .permissions import IsOwnerOrAdmin, IsOwnerOrAdminForAll
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["name"]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"category": ["exact"], "price": ["exact", "gte", "lte"]}
    search_fields = ["name", "description"]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("author", "product").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminForAll, IsOwnerOrAdmin]
    filterset_fields = ["product", "rating"]
    search_fields = ["text"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
