from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from markup.utils.ChoiceFields import *
from markup.utils.document_upload import *
from markup.utils.validators import *


class MainUser(AbstractUser):
    role = models.IntegerField(choices=ROLES, default=GUEST)
    # folders = models.ManyToManyField('Folder', through='AllowedFolder', related_name='participants')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    avatar = models.FileField(upload_to=avatar_image_path, validators=[validate_file_size, validate_extension],
                              default='Default/Default.png')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


# abstract model for folders and imagePacks
class HierarchyElement(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id}:{self.name}'


class Folder(HierarchyElement):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subfolders', blank=True, null=True)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'


class ImagePack(HierarchyElement):
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='imagePack')

    class Meta:
        verbose_name = 'Image Pack'
        verbose_name_plural = 'Image Packs'


# Many to Many relation
class AllowedImagePack(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="member")
    imagePack = models.ForeignKey(ImagePack, on_delete=models.CASCADE, related_name="membership")

    class Meta:
        unique_together = ('user', 'imagePack')


class Image(models.Model):
    name = models.CharField(max_length=150)
    imagePack = models.ForeignKey(ImagePack, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension])

    def __str__(self):
        return f'{self.file.name}'


class Label(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.id}:{self.name}'


class Attachments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(MainUser, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True


class PolygonManager(models.Manager):
    def by_user(self, user):
        return self.filter(created_by=user)


class Polygon(Attachments):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=3000, blank=True)
    points = models.CharField(max_length=1000)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='polygons')
    objects = PolygonManager()

    class Meta:
        verbose_name = 'Polygon'
        verbose_name_plural = 'Polygons'

    def __str__(self):
        return '{}: {}'.format(self.id, self.label.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.label.name
        }


class CommentManager(models.Manager):
    def for_user(self, user):
        return self.filter(created_by=user)


class Comment(Attachments):
    text = models.CharField(max_length=3000)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='comments')
    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return '{}: {}'.format(self.id, self.text)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.text
        }
