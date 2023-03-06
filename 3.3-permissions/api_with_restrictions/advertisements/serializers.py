from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context["request"]
        status = data.get('status')
        max_open_ads = 10
        quantity_open_ads = Advertisement.objects.filter(creator=request.user, status='OPEN').count()
        # Если у пользователя больше 10 открытых объявлений И (он передает не передает статус в запросе ИЛИ
        # передает статус OPEN И текущий статус объявления CLOSED - выдаем ошибку
        if quantity_open_ads >= max_open_ads and \
                (status is None or status == 'OPEN' and self.instance.status == 'CLOSED'):
            raise serializers.ValidationError(
                f'Вы превысили максимальное количество открытых объявлений: {max_open_ads}')
        return data
