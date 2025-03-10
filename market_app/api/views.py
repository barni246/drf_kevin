from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerDetailSerializer, SellerCreateSerializer
from market_app.models import Market, Seller



@api_view(['GET', 'POST'])
def markets_view(request):
    
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True) # "many=True" serializer muss informiert werden, dass es eine Liste von Market bekommt und nicht nur ein object
        return Response(serializer.data)  
     
    if request.method == 'POST':
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # hier wird create Methode von serializer aufgerufen
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors) #  return Response({"error": "Market not found"}, status=status.HTTP_404_NOT_FOUND)

        
        
@api_view(['GET', 'DELETE', 'PUT'])        
def market_single_view(request, pk):
    
    if request.method == 'GET':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        return Response(serializer.data)   
    
    if request.method == 'PUT':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
       
    if request.method == 'DELETE':
        market = Market.objects.get(pk=pk)
        serializer = MarketSerializer(market)
        market.delete()   # serializer kann ncht löschen nur umwandeln
        return Response(serializer.data) 
        # return Response({"message": "Market deleted successfully"}, status=204)  
            
        
        
@api_view(['GET', 'POST'])
def sellers_view(request):
    
    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerDetailSerializer(sellers, many=True)
        return Response(serializer.data)  
     
    if request.method == 'POST':
        serializer = SellerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors) 
        





# @api_view()
# def first_view(request):
#     return Response({"message": "Hello, world!"})


# @api_view(['GET', 'POST'])
# def markets_view(request):
#     if request.method == 'GET':
#          return Response({"message": "Hello, world!"})
#     if request.method == 'POST':
#         try:
#             msg = request.data['message']
#             return Response({"your_message": msg}, status=status.HTTP_201_CREATED)
#         except:
#             return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

