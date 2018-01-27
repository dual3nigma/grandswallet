from django.db.transaction import atomic
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models
from grandswallet.authentication import (
    TokenVerificationAuthentication, TokenDocumentsAuthentication
)


class SignUpView(APIView):
    permission_classes = []
    serializer_class = serializers.CustomerSerializer

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        merchant = serializer.save()
        token = models.CustomerToken.objects.create(
            user=merchant.user
        )

        return Response({
            'token': token.key
        })


class VerificationView(APIView):
    authentication_classes = [
        TokenVerificationAuthentication
    ]

    serializer_class = serializers.VerificationSerializer

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = request.user.verification_codes.filter(
            is_active=True, code=serializer.validated_data['code']
        ).first()

        if not code:
            return Response({
                'detail': 'El código no es válido.'
            }, status=status.HTTP_400_BAD_REQUEST)

        models.CustomerVerified.objects.create(
            user=request.user,
            code=code
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentsView(APIView):
    authentication_classes = [
        TokenDocumentsAuthentication
    ]

    serializer_class = serializers.DocumentSerializer

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            customer=request.user.customer
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(RetrieveAPIView):
    serializer_class = serializers.CustomerSerializer

    def get_object(self):
        return self.request.user.customer


class AccountsView(ListAPIView):
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        return self.request.user.customer.accounts.all()