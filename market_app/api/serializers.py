from rest_framework import serializers
from market_app.models import Market


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