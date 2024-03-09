from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import force_authenticate
# from django.contrib.auth.models import User
from users.models import User
from lms.models import Lesson, Course, Subscription
import json


class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом
        self.lesson_user1 = []
        self.lesson_user2 = []
        self.deleted_user2 = []
        self.user1 = User.objects.create(email='test1@sky.pro', password='123qaz')
        self.user2 = User.objects.create(email='test2@sky.pro', password='123qaz')
        self.client.force_authenticate(user=self.user1)
        self.course = Course.objects.create(title='Course 1', description='Курс Course 1')
        for item in range(1, 4):
            Lesson.objects.create(title=f'Lesson {item}', description=f'Урок Lesson {item}',
                                  course=self.course, owner=self.user1, video_link=None, preview=None)
        for item in range(4, 6):
            Lesson.objects.create(title=f'Lesson {item}', description=f'Урок Lesson {item}',
                                  course=self.course, owner=self.user2, video_link=None, preview=None)
        lessons = Lesson.objects.filter(owner=self.user1)
        for lsn in lessons:
            self.lesson_user1.append(
                {"id": lsn.id, "title": lsn.title, "description": lsn.description, "preview": None, "video_link": None,
                 "course": lsn.course.id})
        lessons = Lesson.objects.filter(owner=self.user2)
        for lsn in lessons:
            self.lesson_user2.append(
                {"id": lsn.id, "title": lsn.title, "description": lsn.description, "preview": None, "video_link": None,
                 "course": lsn.course.id})
            if lsn.title == 'Lesson 4':
                self.updated_user2 = {"id": lsn.id, "title": lsn.title, "description": f'{lsn.description} обновлено',
                                      "preview": None, "video_link": None, "course": lsn.course.id}
            else:
                self.deleted_user2.append(
                    {"id": lsn.id, "title": lsn.title, "description": lsn.description, "preview": None,
                     "video_link": None, "course": lsn.course.id})
        self.post_data = {"title": 'Lesson 6', "description": 'Урок Lesson 6', "preview": None, "video_link": None,
                          "course": self.course.pk}
        print('setUp - OK')

    def tearDown(self):
        print('tearDown')
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        print('tearDown - OK')

    def test_get(self):
        # Тестирование GET-запроса к API
        print('get')
        url = '/lesson/'
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), self.lesson_user1)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results'), self.lesson_user2)
        print('get - OK')

    def test_post(self):
        # Тестирование POST-запроса к API
        print('post')
        url = '/lesson/create/'
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, data=json.dumps(self.post_data, indent=4), content_type='application/json')
        lesson6 = Lesson.objects.filter(title='Lesson 6')
        id = lesson6[0].id
        posted_data = self.post_data
        posted_data['id'] = id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), posted_data)
        print('post - OK')

    def test_update(self):
        # Тестирование UPDATE-запроса к API
        print('update')
        lesson4 = Lesson.objects.filter(title='Lesson 4')
        description = lesson4[0].description
        id = lesson4[0].id
        course_id = lesson4[0].course.pk
        update_user2 = {'title': 'Lesson 4', 'description': f'{description} обновлено', 'course': f'{course_id}'}
        url = f'/lesson/update/{id}/'
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, update_user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.updated_user2)
        print('update - OK')

    def test_delete(self):
        # Тестирование DELETE -запроса к API
        print('delete')
        lesson4 = Lesson.objects.filter(title='Lesson 4')
        id = lesson4[0].id
        url = f'/lesson/delete/{id}/'
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = '/lesson/'
        response = self.client.get(url)
        self.assertEqual(response.json().get('results'), self.deleted_user2)
        print('delete - OK')


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        print('setUp')
        self.user1 = User.objects.create(email='test1@sky.pro', password='123qaz')
        self.user2 = User.objects.create(email='test2@sky.pro', password='123qaz')
        print(self.user1.pk, self.user2.pk)
        self.client.force_authenticate(user=self.user2)
        self.course = Course.objects.create(title='Course 1', description='Курс Course 1')
        self.post_subscription = {'user_id': self.user2.pk, 'course_id': self.course.pk}
        self.client.force_authenticate(user=self.user1)
        Subscription.objects.create(user_id=self.user1.pk, course_id=self.course.pk)



    def test_post(self):
        # Тестирование POST-запроса к API
        print('post')
        url = '/subscription/create/'
        print('post', self.post_subscription)
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, data=json.dumps(self.post_subscription, indent=4), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка добавлена'})
        print('post - OK')

    def test_delete(self):
        # Тестирование DELETE -запроса к API
        print('delete')
        subscription = Subscription.objects.filter(user_id=self.user1.pk)
        id = subscription[0].id
        url = f'/subscription/delete/{id}/'
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})
        url = '/lesson/'
        response = self.client.get(url)
        print('resp', response.json())
        self.assertEqual(response.json().get('results'), [])
        print('delete - OK')
