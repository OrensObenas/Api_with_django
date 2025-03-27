from decimal import Decimal
from rest_framework import serializers
from .models import MenuItem, Category
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory', 'stock', 'price_after_tax', 'category', 'category_id']
        #id = serializers.IntegerField()
        #title = serializers.CharField(max_length=225)
        
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    
    
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title']) #Pour éviter les injections XSS
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
    
    
"""     def validate_title(self, value): #Pour la sanitization et éviter les injections XSS
        return bleach.clean(value) """