from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from .models import File
from .search_indexes import FileIndex

import os


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta():
        model = File
        fields = ('docfile', 'name', 'timestamp', 'owner', 'size')

    def validate(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['name'] = os.path.splitext(
            validated_data['docfile'].name)[0]
        validated_data['size'] = validated_data['docfile'].size
        return validated_data

    def create(self, validated_data):
        return File.objects.create(**validated_data)


class FileSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [FileIndex]
        fields = ["title"]
