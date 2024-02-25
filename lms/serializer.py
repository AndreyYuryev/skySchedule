from rest_framework import serializers
from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_counter = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'lesson_counter', ]

    def get_lesson_counter(self, instance):
        return instance.lesson_set.count()
