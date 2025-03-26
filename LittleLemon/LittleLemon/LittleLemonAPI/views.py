from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view()
def menu_items(request):
    items = MenuItem.objects.select_related('category').all()
    serializer_item = MenuItemSerializer(items, many=True)
    return Response(serializer_item.data)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer_item = MenuItemSerializer(item)
    return Response(serializer_item.data)


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all() # Pour afficher les elements
    serializer_class = MenuItemSerializer # Pour Effectuer les operations CRUD