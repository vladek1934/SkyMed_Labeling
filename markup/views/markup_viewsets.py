import logging

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=True)
    def polygons(self, request, pk):
        # permission: admin
        self.permission_classes = (IsAdminUser,)
        self.check_permissions(request)

        polygons = Image.objects.get(id=pk).polygons.all()
        serializer = ImageSerializer(polygons, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def my_polygons(self, request, pk):
        # permission: auth

        polygons = Image.objects.get(id=pk).polygons.filter(created_by=self.request.user)
        serializer = PolygonSerializer(polygons, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk):
        # permission: admin
        self.permission_classes = (IsAdminUser,)
        self.check_permissions(request)

        comments = Image.objects.get(id=pk).comments.all()
        serializer = FolderSerializer(comments, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def my_comment(self, request, pk):
        # permission: auth

        comment = Image.objects.get(id=pk).comments.get(created_by=self.request.user)
        serializer = FolderSerializer(comment)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminUser,)


class PolygonViewSet(viewsets.ModelViewSet):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = (IsAdminUser,)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAdminUser,)
