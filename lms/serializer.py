from rest_framework import serializers
from lms.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_counter = serializers.SerializerMethodField()
    # lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'lesson_counter', 'lesson',]

    def get_lesson_counter(self, instance):
        # return instance.lesson_set.count()
        return instance.lesson.count()


