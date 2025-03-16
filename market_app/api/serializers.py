from rest_framework import serializers
from market_app.models import Market, Seller, Product


def validate_markets(value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("Ein oder mehrere Market-IDs existieren nicht.")
        return value
    
def validate_sellers(value):
        sellers = Seller.objects.filter(id__in=value)
        if len(sellers) != len(value):
            raise serializers.ValidationError("Ein oder mehrere Seller-IDs existieren nicht.")
        return value      
 
def validate_no_x(value):
    errors = []
    
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')
        
    if errors:
        raise serializers.ValidationError(errors)
    
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)
    
    def create(self, validated_data):   # create in django exsistiert, wir müssen es überschreiben, es wird immer bei POST aufgerufen
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data): # wenn es um instance geht, dann wird diese Funktion aufgerufen
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
    # def validate_location(self, value):
    #     if 'X'in value:
    #         raise serializers.ValidationError('no X in location')
    #     return value
    
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = MarketSerializer(many=True, validators=[validate_markets])
    # markets = serializers.StringRelatedField(many=True) # Related String Methode, wird nur in Model angegebene Feld angezeigt.
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.contact_info = validated_data.get('contact_info', instance.contact_info)
        if 'markets' in validated_data:
            instance.markets.set(Market.objects.filter(id__in=validated_data['markets']))  
        instance.save()
        return instance
    
           
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True, validators=[validate_markets]) # "child" ist hier für Datentyp gedacht, es wurde integer datentyp festgelegt für  "Unterfeld"

    def create(self, validated_data): 
        market_ids = validated_data.pop('markets')  # Holt die Markt-IDs und entfernt sie aus den Daten
        seller = Seller.objects.create(**validated_data)  # Erstellt den Seller ohne Märkte
        markets = Market.objects.filter(id__in=market_ids)  # Holt die Market-Objekte aus der Datenbank
        seller.markets.set(markets)  # Verknüpft den Seller mit den Märkten  # "seller.markets" kommt von model Seller
        return seller

    
class ProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)

    # Eingabe (IDs)  POST/PUT 
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    sellers = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['markets'] = MarketSerializer(instance.markets.all(), many=True).data
        data['sellers'] = SellerDetailSerializer(instance.sellers.all(), many=True).data
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)

        if 'markets' in validated_data:
            instance.markets.set(Market.objects.filter(id__in=validated_data['markets']))  
        if 'sellers' in validated_data:
            instance.sellers.set(Seller.objects.filter(id__in=validated_data['sellers']))  

        instance.save()
        return instance

    
class ProductCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)

    # Eingabe IDs
    markets = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, validators=[validate_markets]
    )
    sellers = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, validators=[validate_sellers]
    )

    # Objekte
    markets_data = MarketSerializer(many=True, read_only=True)
    sellers_data = SellerDetailSerializer(many=True, read_only=True)

    def validate(self, data):
        if not data.get('markets'):
            raise serializers.ValidationError({"markets": "Mindestens ein Markt ist erforderlich."})
        if not data.get('sellers'):
            raise serializers.ValidationError({"sellers": "Mindestens ein Verkäufer ist erforderlich."})
        return data

    def create(self, validated_data):
        market_ids = validated_data.pop('markets', [])
        seller_ids = validated_data.pop('sellers', [])

        product = Product.objects.create(**validated_data)

        if market_ids:
            product.markets.set(Market.objects.filter(id__in=market_ids))
        if seller_ids:
            product.sellers.set(Seller.objects.filter(id__in=seller_ids))

        return product

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['markets'] = MarketSerializer(instance.markets.all(), many=True).data
        data['sellers'] = SellerDetailSerializer(instance.sellers.all(), many=True).data
        return data
