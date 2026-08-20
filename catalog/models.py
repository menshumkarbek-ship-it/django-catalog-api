from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("Слаг", max_length=140, unique=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField("Рейтинг", validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    def __str__(self):
        return f"{self.product} - {self.rating}/5"
