from rest_framework import serializers
from translation.models import TranslationItem
from vn_core.models import VisualNovel


class StatsSerializer(serializers.Serializer):
    visual_novel = serializers.CharField()
    statistics = serializers.CharField()
    moderators = serializers.CharField()
    translator = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return TranslationItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.visual_novel = validated_data.get('visual_novel', instance.title)
        instance.statistics = validated_data.get('statistics', instance.statistics)
        instance.moderators = validated_data.get('moderators', instance.moderators)
        instance.translator = validated_data.get('translator', instance.translator)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance