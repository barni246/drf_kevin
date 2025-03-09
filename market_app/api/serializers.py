from rest_framework import serializers
from market_app.models import Market, Seller


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
    
    def create(self, validated_data):   # create in django egsistiert, wir müssen es überschreiben, es wird immer bei POST aufgerufen
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
    markets = MarketSerializer(many=True, read_only=True)
        
    
        
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(),write_only=True) # "child" ist hier für Datentyp gedacht, es wurde integer datentyp festgelegt
    
    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if(markets) != len(value):
            raise serializers.ValidationError("One or more Markets not found")
        return value
    
    # def create(self, validated_data): 
    #     market_ids = validated_data.pop('markets') 
    #     seller = Seller.objects.create(**validated_data)
    #     markets = Market.objects.filter(id__in=market_ids)
    #     seller.markets.set(markets)  # "seller.markets" kommt von model Seller
    #     return seller
    
    def create(self, validated_data): 
        market_ids = validated_data.pop('markets')  # Holt die Markt-IDs und entfernt sie aus den Daten
        seller = Seller.objects.create(**validated_data)  # Erstellt den Seller ohne Märkte
        markets = Market.objects.filter(id__in=market_ids)  # Holt die Market-Objekte aus der Datenbank
        seller.markets.set(markets)  # Verknüpft den Seller mit den Märkten
        return seller
