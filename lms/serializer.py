from rest_framework import serializers
from lms.models import Lesson, Course, Subscription
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_link'), ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_counter = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'lesson_counter', 'lesson', 'owner', ]

    def get_lesson_counter(self, instance):
        return instance.lesson.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    subscribed = serializers.HiddenField(default=True)

    class Meta:
        model = Subscription
        fields = '__all__'
