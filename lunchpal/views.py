from datetime import date

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from lunchpal.models import Restaurant, Menu
from lunchpal.serializers import RestaurantSerializer, MenuSerializer
from lunchpal.permissions import (
    IsSuperuserOrManager,
    IsManager,
    IsSuperuserOrEmployee,
)


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    View to list and create restaurants.
    Only superusers and restaurant managers can create restaurants.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [
        IsAuthenticated,
        IsSuperuserOrManager,
    ]

    def perform_create(self, serializer):
        serializer.save()


class MenuViewSet(viewsets.ModelViewSet):
    """
    View to create and update a menu for a restaurant.
    Only restaurant managers can update a menu.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsManager]


class CurrentDayMenuView(generics.ListAPIView):
    """
    View to get the current day menu.
    """

    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(date=date.today())


class VoteMenuView(generics.GenericAPIView):
    """
    View for employees or superusers to vote for the menu.
    """

    permission_classes = [IsAuthenticated, IsSuperuserOrEmployee]

    def post(self, request, *args, **kwargs):
        menu_id = self.kwargs.get("menu_id")
        try:
            menu = Menu.objects.get(id=menu_id)
            menu.votes += 1
            menu.save()
            return Response(
                {"Success": "Your vote has been recorded."},
                status=status.HTTP_200_OK,
            )
        except Menu.DoesNotExist:
            return Response(
                {"Error": "Menu not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CurrentDayResultView(generics.GenericAPIView):
    """
    View to get the winner for today's votes.
    """

    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        today = date.today()

        menu = Menu.objects.filter(date=today).order_by("-votes").first()

        if menu:
            serializer = MenuSerializer(menu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"Error": "No menus found for today."},
                status=status.HTTP_404_NOT_FOUND,
            )
