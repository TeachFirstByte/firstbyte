from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db import transaction

from rest_framework import serializers

from .util import all_in_or_all_not_in, all_same_length
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

class NullableIntegerField(serializers.IntegerField):
    def to_representation(self, value):
        if value is None:
            return ''
        return super().to_representation(value)

    def to_internal_value(self, data):
        if data == '':
            return None
        return super().to_internal_value(data)


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

    material_ids = serializers.ListField(
        child=NullableIntegerField(),
        write_only=True,
        required=False
    )
    material_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    lesson_resource_ids = serializers.ListField(
        child=NullableIntegerField(),
        write_only=True,
        required=False
    )
    lesson_resource_names = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    lesson_resource_types = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    lesson_resource_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    def validate(self, data):
        """Validates the lesson resource and materials writeable fields."""
        lesson_resource_keys = [
            'lesson_resource_ids',
            'lesson_resource_names',
            'lesson_resource_types',
        ]
        if not all_in_or_all_not_in(lesson_resource_keys, data):
            raise serializers.ValidationError(
                "Lesson resources lists must all be present together, or not at all"
            )
        if not all_same_length(lesson_resource_keys, data):
            raise serializers.ValidationError("Lesson resources lists must all be the same length")

        material_keys = [
            'material_ids',
            'material_names'
        ]
        if not all_in_or_all_not_in(material_keys, data):
            raise serializers.ValidationError(
                "Material lists must all be present together, or not at all"
            )
        if not all_same_length(material_keys, data):
            raise serializers.ValidationError("Material lists must all be the same length")

        return data

    @staticmethod
    def get_resources(ids, names, types, files, **create_kwargs):
        """Retrieves and updates lesson resources given lists."""
        for index, r_id in enumerate(ids):
            resource = None
            try:
                if r_id:
                    resource = LessonResource.objects.get(id=r_id)
            except ObjectDoesNotExist:
                pass

            if resource is None:
                resource = LessonResource(**create_kwargs)
                resource.file = files.pop(0)

            resource.name = names[index]
            resource.semantic_type = types[index]

            resource.save()
            yield resource

    @classmethod
    def save_resources(cls, instance, validated_data, **create_kwargs):
        """Retrieve and save resources given validated data."""
        resource_ids = validated_data.pop('lesson_resource_ids', [])
        resource_names = validated_data.pop('lesson_resource_names', [])
        resource_types = validated_data.pop('lesson_resource_types', [])
        resource_files = validated_data.pop('lesson_resource_files', [])

        for resource in cls.get_resources(resource_ids, resource_names, resource_types, resource_files, **create_kwargs):
            instance.resources.add(resource)

    @staticmethod
    def get_materials(ids, names, **create_kwargs):
        """Retrieves and updates materials given lists."""
        for index, m_id in enumerate(ids):
            material = None
            try:
                if m_id:
                    material = Material.objects.get(id=m_id)
            except ObjectDoesNotExist:
                pass

            if material is None:
                material = Material(**create_kwargs)

            material.name = names[index]
            material.save()
            yield material

    @classmethod
    def save_materials(cls, instance, validated_data, **create_kwargs):
        """Retrieves and saves materials given validated data."""
        material_ids = validated_data.pop('material_ids', [])
        material_names = validated_data.pop('material_names', [])

        for material in cls.get_materials(material_ids, material_names, **create_kwargs):
            instance.materials.add(material)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['user']

        lesson_plan = LessonPlan.objects.create(
            title=validated_data['title'],
            summary=validated_data['summary'],
            grade_level=validated_data['grade_level'],
            total_prep_time=validated_data['total_prep_time'],
            num_classes=validated_data['num_classes'],
            single_class_time=validated_data['single_class_time'],
            web_only=validated_data['web_only'],
            feedback_enabled=validated_data['feedback_enabled'],
            draft=validated_data['draft'],
            owner=user
        )
        self.save_resources(lesson_plan, validated_data, owner=user)
        self.save_materials(lesson_plan, validated_data)
        lesson_plan.save()

        return lesson_plan

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['user']

        instance.title = validated_data.get('title', instance.title)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.grade_level = validated_data.get('grade_level', instance.grade_level)

        instance.total_prep_time = validated_data.get('total_prep_time', instance.total_prep_time)
        instance.num_classes = validated_data.get('num_classes', instance.num_classes)
        instance.single_class_time = validated_data.get('single_class_time', instance.single_class_time)

        instance.web_only = validated_data.get('web_only', instance.web_only)
        instance.feedback_enabled = validated_data.get('feedback_enabled', instance.feedback_enabled)
        instance.draft = validated_data.get('draft', instance.draft)

        # One list is present so they all are, as asserted during validation

        if 'lesson_resource_ids' in validated_data:
            for original_resource in instance.resources.all():
                if original_resource.id not in validated_data['lesson_resource_ids']:
                    original_resource.delete()

            instance.resources.clear()
            self.save_resources(instance, validated_data, owner=user)

        if 'material_ids' in validated_data:
            for original_material in instance.materials.all():
                if original_material.id not in validated_data['material_ids']:
                    original_material.delete()

            instance.materials.clear()
            self.save_materials(instance, validated_data)

        instance.save()
        return instance
