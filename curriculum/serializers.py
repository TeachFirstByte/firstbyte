from rest_framework import serializers
from .models import LessonResource, LessonResourceExternalLink, Material, LessonPlan

class LessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = ['owner', 'name', 'mime_type', 'semantic_type', 'file', 'create_time']
        read_only_fields = ['create_time']


class LessonResourceExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResourceExternalLink
        fields = ['name', 'semantic_type', 'owner', 'link', 'create_time']
        read_only_fields = ['create_time']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']
        read_only_fields = ['id']


class LessonPlanSerializer(serializers.ModelSerializer):
    # Replace with a User serializer that adds names,
    owner = serializers.CharField(source="owner.first_name", read_only=True)

    resources = LessonResourceSerializer(many=True, read_only=True)
    resource_links = LessonResourceExternalLinkSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True)


    class Meta:
        model = LessonPlan
        fields = [
            'owner', 'title', 'summary', 'grade_level',
            'total_prep_time', 'num_classes', 'single_class_time',
            'web_only', 'resources', 'resource_links', 'materials',
            'feedback_enabled', 'draft', 'last_modified_time',
            'create_time'
        ]
        read_only_fields = ['last_modified_time', 'create_time']
        depth = 1

    def create(self, validated_data):
        materials_data = validated_data.pop('materials')
        lesson_plan = LessonPlan.objects.create(**validated_data)
        for material_data in materials_data:
            material = Material.objects.create(**material_data)
            lesson_plan.materials.add(material)
        lesson_plan.save()
        return lesson_plan
