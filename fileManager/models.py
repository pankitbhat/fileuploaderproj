from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


import os


def file_size(value):
    limit = 1024 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 GiB.')


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class File(models.Model):
    docfile = models.FileField(
        upload_to=user_directory_path, blank=False, null=False, validators=[file_size])
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name='file_upload', on_delete=models.CASCADE)
    size = models.IntegerField(default=0)


def _delete_file(path):
    if os.path.isfile(path):
        print("***********")
        print(path)
        os.remove(path)


@receiver(post_delete, sender=File)
def delete_file(sender, instance, *args, **kwargs):
    if instance.docfile:
        _delete_file(instance.docfile.path)
