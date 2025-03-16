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
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    name = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True, validators=[validate_markets])
    sellers = serializers.ListField(child=serializers.IntegerField(), write_only=True, validators=[validate_sellers])
    
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
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True, validators=[validate_markets]) 
    sellers = serializers.ListField(child=serializers.IntegerField(), write_only=True, validators=[validate_sellers]) 

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('sellers')
        product = Product.objects.create(**validated_data)
        product.markets.set(Market.objects.filter(id__in=market_ids))
        product.sellers.set(Seller.objects.filter(id__in=seller_ids))
        return product

     

    
    
    
