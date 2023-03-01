from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['address', 'products']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'positions', 'address', ]

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # заполняем связанную таблицу StockProduct с помощью списка positions
        # 1 вариант
        for pos in positions:
            StockProduct.objects.create(stock=stock, **pos)

        # 2ой вариант
        # for pos in positions:
        #     StockProduct.objects.create(
        #         product=pos['product'],
        #         quantity=pos['quantity'],
        #         price=pos['price'],
        #         stock_id=stock.pk,
        #     )

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # обновляем связанную таблиу StockProduct с помощью списка positions
        for pos in positions:
            StockProduct.objects.update_or_create(stock=stock, product=pos['product'], defaults=pos)

        return stock
