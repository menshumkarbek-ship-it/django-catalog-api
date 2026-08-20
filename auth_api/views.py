from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer, RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def perform_create(self, serializer):
        user = serializer.save()
        send_mail("Добро пожаловать в Catalog", f"Здравствуйте, {user.username}!", settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        token = RefreshToken.for_user(user)
        response.data["access"] = str(token.access_token)
        response.data["refresh"] = str(token)
        return response

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"email": "Укажите email."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = request.build_absolute_uri(f"/api/password-reset-confirm/{uid}/{token}/")
            send_mail("Сброс пароля Catalog", f"Перейдите по ссылке для сброса пароля: {link}", settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        return Response({"detail": "Если аккаунт существует, письмо отправлено."})

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, uidb64, token):
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if not user or not default_token_generator.check_token(user, token):
            return Response({"detail": "Ссылка недействительна или устарела."}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get("password")
        if not password or len(password) < 8:
            return Response({"password": "Пароль должен содержать минимум 8 символов."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response({"detail": "Пароль успешно изменен."})
