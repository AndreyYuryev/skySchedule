from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from lms.serializer import LessonSerializer, CourseSerializer, SubscriptionSerializer
from lms.models import Lesson, Course, Subscription
from users.models import User
from lms.permissions import IsOwner
from users.permissions import IsModerator
from lms.paginators import LessonPaginator, CoursePaginator
from rest_framework.response import Response
from lms.tasks import inform_by_course_update


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    # queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if (self.action == 'list' or self.action == 'retrieve'
                or self.action == 'update' or self.action == 'partial_update'):
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'list':
            return Course.objects.filter(owner=self.request.user)
        else:
            return Course.objects.all()

    def perform_update(self, serializer):
        course = serializer.save()
        inform_by_course_update.delay(course.pk)
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonListAPIView(generics.ListAPIView):
    """ Lesson List API description """
    serializer_class = LessonSerializer
    # queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = LessonPaginator

    def get_queryset(self):
        if not self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = Subscription
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user_id = self.request.data.get('user_id')
        course_id = self.request.data.get('course_id')
        courses = Course.objects.filter(pk=course_id)
        users = User.objects.filter(pk=user_id)
        if courses.exists() and users.exists():
            subs_items = Subscription.objects.filter(user_id=user_id, course_id=course_id)
            if not subs_items.exists():
                subscription = Subscription.objects.create(course=Course.objects.get(pk=course_id),
                                                           user=User.objects.get(pk=user_id))
                subscription.save()
                message = 'подписка добавлена'
            else:
                message = 'подписка актуальна'
        else:
            message = 'подписка невозможна'
        return Response({"message": message})


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        subscription_id = kwargs.get('pk')
        subs_items = Subscription.objects.filter(pk=subscription_id)
        if subs_items.exists():
            subscription = Subscription.objects.get(pk=subscription_id)
            subscription.delete()
            message = 'подписка удалена'
        else:
            message = 'подписка не существует'
        return Response({"message": message})
