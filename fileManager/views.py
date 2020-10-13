from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework import status

from drf_haystack.viewsets import HaystackViewSet

from .serializers import FileSerializer, FileSearchSerializer
from .models import File, User
from .safeutil import copyfile, move
from .utils import get_base_fixed_path, check_file_path_exists_or_create_dir

from django.http import Http404
from django.conf import settings
from django.db.models import Q, Sum

import os
from os import path
import pathlib
import shutil


class UserFileCopy(APIView):
    def post(self, request):
        data = request.data
        filename = data['filename']
        destination_path = data['destination']

        user = User.objects.get(email=request.user)

        file_size_obj = File.objects.filter(owner_id=user.id).values(
            'size').annotate(total=Sum('size'))

        for f in file_size_obj:
            space_allocated = f['total']

        limit = 1024 * 1024 * 1024
        if space_allocated > limit:
            return Response({"Not Enough Free Space to copy and additional Space required in bytes": abs(limit-space_allocated)})

        common_path, file_update_base_path = get_base_fixed_path(user.id)
        destination_path = common_path + destination_path

        check_file_path_exists_or_create_dir(destination_path)

        src_path = common_path + filename
        destination_path = destination_path + filename

        dst = file_update_base_path + data['destination'] + filename

        if path.isfile(src_path):
            copyfile(src_path, destination_path)
            f = File(name=filename.split('.')[
                     0], docfile=dst, owner_id=user.id, size=os.path.getsize(src_path))
            f.save()
            return Response({"File copied to new path": str(destination_path)}, status=status.HTTP_201_CREATED)

        return Response({"File path doesn't exist": src_path})


class UserFileOperations(UpdateAPIView):
    def post(self, request):
        data = request.data
        user = User.objects.get(email=request.user)
        src = data['old_path']
        dst = data['new_path']

        name = pathlib.Path(src).name
        common_path, file_update_base_path = get_base_fixed_path(user.id)

        src_filepath = common_path + src
        dst_filepath = common_path + dst

        dst = file_update_base_path + dst + name
        check_file_path_exists_or_create_dir(dst_filepath)

        if path.isfile(src_filepath):
            shutil.move(src_filepath, dst_filepath)
            file_obj = File.objects.filter(Q(owner_id=user.id) & Q(
                name=name.split('.')[0])).first()
            file_obj.docfile = dst
            file_obj.save()
            return Response({"File moved to new path": str(dst_filepath)}, status=status.HTTP_201_CREATED)

        return Response({"File path doesn't exist": src})

    def put(self, request):
        data = request.data
        user = User.objects.get(email=request.user)
        src_filename = data['old_filename']
        dst_filename = data['new_filename']

        name = pathlib.Path(src_filename).name

        common_path, file_update_base_path = get_base_fixed_path(user.id)
        src_filename = common_path + src_filename
        dst_filename = common_path + dst_filename
        print(src_filename, dst_filename)

        if path.isfile(src_filename):
            print(data['old_filename'].split('.')[0])
            try:
                os.rename(src_filename, dst_filename)
            except:
                os.remove(dst_filename)
                os.rename(src_filename, dst_filename)
            file_obj = File.objects.filter(Q(owner_id=user.id) & Q(
                name=name.split('.')[0])).first()
            print(type(file_obj), file_obj)
            file_obj.name = data['new_filename'].split('.')[0]
            file_obj.docfile = file_update_base_path + data['new_filename']
            file_obj.save()
            return Response({"File name changed to": str(dst_filename)}, status=status.HTTP_201_CREATED)

        return Response({"File path doesn't exist": src_filename})


class UserFileUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        file_serializer = FileSerializer(
            data=request.data, context={'request': request})
        limit = 1024 * 1024 * 1024
        space_allocated = 0
        doc_file_uploaded_size = request.data['docfile'].size
        file_size_obj = File.objects.filter(owner_id=user.id).values(
            'size').annotate(total=Sum('size'))
        for f in file_size_obj:
            space_allocated = f['total']
        space_left = limit-space_allocated
        if space_left < doc_file_uploaded_size:
            return Response({"Not Enough Free Space to upload file and additional Space required in bytes": abs(space_left-doc_file_uploaded_size)})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data['name']
        name = pathlib.Path(data).name
        user = User.objects.get(email=request.user)
        common_path, file_update_base_path = get_base_fixed_path(user.id)
        filepath = common_path + data
        if path.isfile(filepath):
            file_obj = File.objects.filter(
                Q(name=name.split('.')[0]) & Q(owner_id=user.id)).first()
            file_obj.delete()
            return Response({"File deleted is ": str(request.data['name'])}, status=status.HTTP_201_CREATED)
        return Response({"File path doesn't exist": filepath})


class FileSearchView(HaystackViewSet):
    index_models = [File]
    serializer_class = FileSearchSerializer
