from rest_framework import serializers
from django.contrib.auth.models import User
from markup.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'description',)

    def get_extra(self, obj):
        categories = obj.categories.filter(allowed=self.context.get('request').user)
        if categories:
            return True
        return False


# class CategorySerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'description',)


class LabelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Label
        fields = '__all__'


class PolygonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    attributes = serializers.CharField(required=False, allow_blank=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Polygon
        fields = ('id', 'name', 'label', 'attributes', 'points', 'image')

    def get_name(self, obj):
        return obj.label.name


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    extra = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'name', 'file', 'extra')

    def get_extra(self, obj):
        polygons = obj.polygons.filter(created_by=self.context.get('request').user)
        if polygons:
            return True
        return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_by = UserSerializer(read_only=True)
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'