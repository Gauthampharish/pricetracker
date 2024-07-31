from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Alert
from .serializers import AlertSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class AlertViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing alert instances.
    """
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    
    def get_queryset(self):
        """
        Optionally restricts the returned alerts to a given user,
        by filtering against the `user_id` field.
        """
        return self.queryset.filter(user_id=self.request.user)

    @swagger_auto_schema(
        request_body=AlertSerializer,
        responses={201: openapi.Response('Created', AlertSerializer)},
    )
    def create(self, request, *args, **kwargs):
            """
            Creates a new alert instance.

            This method sets the `user_id` field to the current user when creating a new alert.
            It validates the incoming data using the serializer and, if valid, creates the alert.
            If the data is invalid, it returns a 400 Bad Request response with the validation errors.
            If the data is valid, it returns a 201 Created response with the created alert data.

            Args:
                request (Request): The HTTP request object containing the alert data.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Response: A DRF Response object with the created alert data or validation errors.
            """
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
   
    def list(self, request, *args, **kwargs):

        """
        Retrieves a list of alert instances for the current user.
        This method caches the response data for 5 minutes to improve performance.

        Args:
            self: The instance of the viewset.
            request (Request): The HTTP request object containing the request data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A DRF Response object with the list of alert instances or cached data.
        """
        user_id = request.user.id
        filter_params = request.query_params.dict()
        cache_key = f"user_alerts_{user_id}_{str(filter_params)}"

        cached_alerts = cache.get(cache_key)
        if cached_alerts is not None:
            
            return Response(cached_alerts)

        # If not cached, fetch from the database
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            response_data = serializer.data

        # Cache the response data for 5 minutes
        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
            
            """
            """
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
