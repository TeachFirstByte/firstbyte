from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from .models import LessonResource, LessonResourceExternalLink, Material, LessonPlan, GradeLevels


class LessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = ['id', 'owner', 'name', 'mime_type', 'semantic_type', 'file', 'create_time']
        read_only_fields = ['id', 'create_time']


class LessonResourceExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResourceExternalLink
        fields = ['id', 'name', 'semantic_type', 'owner', 'link', 'create_time']
        read_only_fields = ['id', 'create_time']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name']
        read_only_fields = ['id']


class LessonPlanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    # Replace with a User serializer that adds names,
    owner = serializers.CharField(source="owner.first_name", read_only=True)

    title = serializers.CharField()
    summary = serializers.CharField()
    grade_level = serializers.ChoiceField(choices=GradeLevels)

    total_prep_time = serializers.DurationField()
    num_classes = serializers.IntegerField()
    single_class_time = serializers.DurationField()

    web_only = serializers.BooleanField()
    feedback_enabled = serializers.BooleanField()
    draft = serializers.BooleanField()

    last_modified_time = serializers.DateTimeField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    slug = serializers.CharField(read_only=True)

    resources = LessonResourceSerializer(many=True, read_only=True)
    resource_links = LessonResourceExternalLinkSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)

    material_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=True
    )

    resource_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    filetypes = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    filenames = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        user = self.context['user']
        if not user.is_authenticated:
            raise PermissionDenied()

        materials_data = [{'name': material_name} for material_name in validated_data.pop('material_names', [])]
        resource_names = validated_data.pop('filenames', [])
        resource_types = validated_data.pop('filetypes', [])
        files = validated_data.pop('files', [])

        lesson_plan = LessonPlan.objects.create(**validated_data, owner=user)
        for material_data in materials_data:
            material = Material.objects.create(**material_data)
            lesson_plan.materials.add(material)

        new_resources_data = [
            {
                'owner': user,
                'name': resource_name,
                'semantic_type': resource_type,
                'file': file
            } for resource_name, resource_type, file in zip(resource_names, resource_types, files)
        ]
        for new_resource_data in new_resources_data:
            resource = LessonResource.objects.create(**new_resource_data)
            lesson_plan.resources.add(resource)

        lesson_plan.save()
        return lesson_plan
