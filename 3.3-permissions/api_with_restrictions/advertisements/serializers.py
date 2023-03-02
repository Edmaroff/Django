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
        """Метод для валидации. Вызывается при создании и обновлении"""
        http_method = self.context["request"].method
        user = self.context["request"].user
        quantity_open_ads = Advertisement.objects.filter(creator=user, status='OPEN').count()
        max_open_ads = 10
        if http_method == 'POST':
            # Если у пользователя больше 10 открытых объявлений и он пытается открыть
            # новое объявление - выкидываем ошибку валидации.
            if quantity_open_ads >= max_open_ads and data.get('status', 'OPEN') == 'OPEN':
                raise serializers.ValidationError(f'Вы превысили максимальное количество открытых объявлений: '
                                                  f'{max_open_ads}')
        elif http_method in ["PUT", "PATCH"]:
            # Статус текущей записи
            status_current_ads = self.instance.status

            # Если у пользователя больше 10 открытых записей И пользователь передает
            # изменения статуса на OPEN И статус текущей записи CLOSED
            if quantity_open_ads >= max_open_ads and data.get('status') == 'OPEN' and status_current_ads == 'CLOSED':
                raise serializers.ValidationError(f'Вы превысили максимальное количество открытых объявлений: '
                                                  f'{max_open_ads}')
        return data
