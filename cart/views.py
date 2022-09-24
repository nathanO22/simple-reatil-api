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

# class CartEditView(APIView):

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsUserAuthenticated]

#     def get_cart_item(self, cart_id):
#         """
#         Tries to retrieves a cart item from the database with the given id.
#         If the cart does not exist, it returns an error message.
#         """
        
#         try:
#             return Cart.objects.get(id=cart_id)
#         except Cart.DoesNotExist:
#             raise NotFound(detail={'message': 'cart-item with id does not exist.'})
   

#     @swagger_auto_schema(method='delete')
#     @action(methods=['DELETE'], detail=True)
#     def delete(self, request, cart_id, format=None):
#         """Delete a single cart item relating to a logged in user.
#            Returns a reponse message 'success' if deleted successfully and status code of 204.
#            when a pending cart item is deleted the quantity is added to the quantity of the item model.
#         """
#         try:
#             user_id = request.user.id
#             object = CustomUser.objects.get(id=user_id)

            
#             if request.user == object and request.user in CustomUser.objects.all():
#                 obj = self.get_cart_item(cart_id=cart_id)
#                 try: 
#                     p = Item.objects.get(item_name=obj.cart_item)
#                     p.quantity_available+=obj.quantity
#                     p.save()
                
#                     obj.delete()
#                     return Response(status=status.HTTP_204_NO_CONTENT)
#                 except Cart.DoesNotExist:
#                     raise NotFound(detail={'message': 'Cart does not exist'})

#             else:
#                 raise PermissionDenied(detail={'message': 'user is forbidden to acces another user data or user is anonymous.'})
            
#         except CustomUser.DoesNotExist:
#             raise NotFound(detail={'message': 'User is an anonyousUser.'})