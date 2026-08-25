import pytest
from catalog.models import Category, Product, Review

@pytest.mark.django_db
def test_product_read_is_public(api_client):
    category = Category.objects.create(name="Books", slug="books")
    Product.objects.create(name="Django", description="Guide", price=10, category=category)
    response = api_client.get("/api/products/")
    assert response.status_code == 200
    assert response.data["count"] == 1

@pytest.mark.django_db
def test_product_create_requires_authentication(api_client):
    response = api_client.post("/api/products/", {"name": "Django", "description": "Guide", "price": 10, "category": 1})
    assert response.status_code == 401

@pytest.mark.django_db
def test_negative_price_has_clear_error(api_client, user):
    api_client.force_authenticate(user=user)
    category = Category.objects.create(name="Books", slug="books")
    response = api_client.post("/api/products/", {"name": "Django", "description": "Guide", "price": -1, "category": category.pk})
    assert response.status_code == 400
    assert "Цена не может быть отрицательной" in str(response.data)

@pytest.mark.django_db
def test_review_owner_can_edit_but_other_user_cannot(api_client, user):
    from django.contrib.auth import get_user_model
    other = get_user_model().objects.create_user(username="igor", password="strong-pass-123")
    category = Category.objects.create(name="Books", slug="books")
    product = Product.objects.create(name="Django", description="Guide", price=10, category=category)
    review = Review.objects.create(product=product, author=user, text="Good", rating=5)
    api_client.force_authenticate(user=other)
    assert api_client.patch(f"/api/reviews/{review.pk}/", {"text": "Changed"}).status_code == 403
    api_client.force_authenticate(user=user)
    assert api_client.patch(f"/api/reviews/{review.pk}/", {"text": "Changed"}).status_code == 200

@pytest.mark.django_db
def test_review_create_requires_authentication(api_client):
    category = Category.objects.create(name="Books", slug="books")
    product = Product.objects.create(name="Django", description="Guide", price=10, category=category)
    response = api_client.post("/api/reviews/", {"product": product.pk, "text": "Good", "rating": 5})
    assert response.status_code == 401
