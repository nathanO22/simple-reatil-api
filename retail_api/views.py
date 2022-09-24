from rest_framework import status 
from .models import Inventory
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InventorySerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsAdminOrReadOnly

class InventoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, format=None):

        objs = Inventory.objects.all()
        serializer = InventorySerializer(objs, many=True)

        data = {
            'message': 'success',
            'data_count': objs.count(),
            'data': serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body = InventorySerializer())   
    @action(methods=['POST'], detail=True)
    def post(self, request, format = None):

        serializer = InventorySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            
            data = {
                'message': 'Success'
            }

            return Response(data, status =status.HTTP_201_CREATED)

        else:
            data = {
                "message": "failed",
                "error": "serializer.errors"
            }

            return Response(data, status =status.HTTP_400_BAD_REQUEST)

class InventoryDetailView(APIView):
    """
    Retrieves, updates, and deletes an inventory instance.
    """

    def get_object(self, inventory_id):
        """Get a single category instance using the specified category_id."""

        try:
            return Inventory.objects.get(id=inventory_id)
        except Inventory.DoesNotExist:
            raise NotFound(detail = {"message": "Item not found."})

    def get(self, request, inventory_id, format = None):
        obj = self.get_object(inventory_id)
        serializer = InventorySerializer(obj)

        data = {
            "message": "success",   
            "data": serializer.data
        }
        
        return Response(data, status =status.HTTP_200_OK)

    def put(self, request, inventory_id, format = None):
        obj = self.get_object(inventory_id)
        serializer = InventorySerializer(obj, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()

            data = {
                "message": "success"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "message": "failed",
                "error": serializer.errors,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, inventory_id, format = None):
        obj = self.get_object(inventory_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
