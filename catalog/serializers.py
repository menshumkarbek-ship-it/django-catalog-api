from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[])

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "image", "created_at"]
        read_only_fields = ["created_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Размер изображения не должен превышать 5 МБ.")
        if value.content_type not in ["image/jpeg", "image/png"]:
            raise serializers.ValidationError("Допустимы только изображения в формате JPG или PNG.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Review
        fields = ["id", "product", "author", "author_name", "text", "rating", "created_at"]
        read_only_fields = ["author", "author_name", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value
