from django.shortcuts import render,get_object_or_404
from rest_framework import generics, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute

# Create your views here.
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2) # Pour définir le nombre de requette que peut un appel d'API
        page = request.query_params.get('page', default=1) # Pour définir le nombre de page sur lequel doit s'afficher la requette
        if category_name:
            items = items.filter(category__title = category_name)
        if to_price:
            items = items.filter(price= to_price)
        if ordering:
            ordering_fields = ordering.split(",") # Pour ordonner plusieurs champs
            items = items.order_by(*ordering_fields)
            
            
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serializer_item = MenuItemSerializer(items, many=True)
        return Response(serializer_item.data)
    
    elif request.method == 'POST':
        serializer_item = MenuItemSerializer(data=request.data)
        serializer_item.is_valid(raise_exception=True)
        serializer_item.save()
        return Response(serializer_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serializer_item = MenuItemSerializer(item)# We can add context here to show hyperlink of category
    return Response(serializer_item.data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager Should See this"})
    else:
        return Response({"message":"You are not authorized"}, 403)
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"succesful"})
    
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check(request):
    return Response({"message":"message for the logged in users only"})

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    search_fields = ['title']
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all() # Pour afficher les elements
    serializer_class = MenuItemSerializer # Pour Effectuer les operations CRUD