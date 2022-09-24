from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Cart, Inventory, CartItem
from accounts.models import User 
from accounts.permissions import IsAdminOrReadOnly, IsUserAuthenticated, IsUserOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from .serializers import CartSerializer,  Cart_Serializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied

# Create your views here.
class CartView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserAuthenticated]

    def get(self, request, format=None):
        """
        Retrieves a logged in user cart from the database, only pending items are shown.
        Anonymoususer are restricted from using this method.
        returns an error message if user is not logged in.
        """
        if request.user in User.objects.all():

            user_id = request.user.id
            object = User.objects.get(id=user_id)
            # products = CartItem.objects.all
            obj = object.user.all()

            serializer = CartSerializer(obj, many=True)

            data = {
                'message': 'successful',
                'total orders': obj.count(),
                'data': serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(detail={'error': 'User does not exist, check your credentials or create an account if you do not have one.'})

    @swagger_auto_schema(method='post', request_body=Cart_Serializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """
        Adds items to the cart of a user in the database to the cart model only if the  
        item quantity available in the database is greater than quantity demanded.
        Accessible only to logged in users.

        """  
        data = {}
        data['products'] = request.data['products']
        data['quantity'] = request.data['quantity']
        data['user'] = request.user.id
        try:
            cart_item = CartItem.objects.get(id=data['products'])          
            cart_item_price = cart_item.price
            data['item_cost'] = data['quantity'] * cart_item_price
            print(cart_item)
            

            if request.user in User.objects.all():
                
                if data['quantity'] > cart_item['quantity']:
                    return Response(data={'message': 'Requested quantity is higher than quantity available in store'}, status=status.HTTP_403_FORBIDDEN)

                else:
                    cart_item['quantity'] -= data['quantity'] 
                    cart_item.save()
                    serializer = CartSerializer(data=data)
                    
                    if serializer.is_valid():
                        serializer.save()
                        
                        data = {
                            "message":"item successfully added to cart",
                        }

                        return Response(data, status = status.HTTP_200_OK)

                    else:
                        data = {
                            "message":"failed",
                            "error":serializer.errors
                        }
                    
                    return Response(data, status = status.HTTP_400_BAD_REQUEST)

            else:
                raise PermissionDenied(detail={'message': 'User does not exist, check your credentials or create an account if you do not have one.'})

        except CartItem.DoesNotExist:
            raise NotFound(detail={'message': 'Item with id does not exist'})