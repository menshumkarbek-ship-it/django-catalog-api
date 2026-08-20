from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("reviews", ReviewViewSet)
urlpatterns = router.urls
