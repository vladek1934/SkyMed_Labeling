import logging

from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class FolderViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FolderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action in ['list', ]:
            return Folder.objects.filter(Q(participants=self.request.user) & Q(type=ROOT) & Q(parent=None))
        else:
            return Folder.objects.filter(participants=self.request.user)

    # @action(methods=['GET'], detail=True)
    # def images(self, request, pk):
    #     folder = Folder.objects.get(id=pk).prefetch_related('images')
    #     images = folder.images
    #     print(images)
    #     serializer = ImageSerializer(data=images)
    #
    #     if serializer.is_valid():
    #         print(serializer.data)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllowedFolderViewSet(viewsets.ModelViewSet):
    queryset = AllowedFolder.objects.all()
    serializer_class = AllowedFolderSerializer
    permission_classes = (IsAdminUser,)
