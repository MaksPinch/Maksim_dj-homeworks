import random


import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
from random import randint

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    course_object = courses[0]
    course_id = course_object.id
    url = reverse('courses-detail', kwargs={'pk': course_id})
    resp = client.get(url)

    assert resp.status_code == 200
    json = resp.json()

    assert json['id'] == course_object.id
    assert json['name'] == course_object.name
    assert json['students'] == []

@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    courses = course_factory(_quantity=13)
    url = reverse('courses-list')
    resp = client.get(url)

    assert resp.status_code == 200
    json = resp.json()
    assert len(json) == 13


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    random_number = random.randint(0, 4)
    course_object = courses[random_number]
    course_id = course_object.id

    url = reverse('courses-detail', kwargs={'pk': course_id})
    resp = client.get(url)

    assert resp.status_code == 200
    json = resp.json()
    assert json['id'] == course_object.id
    assert json['name'] == course_object.name
    assert json['students'] == []


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'DRF test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_name_filter(client):
    course = Course.objects.create(name='Maths')
    filter = {'name':'Maths'}

    resp = client.get('/api/v1/courses/', data=filter)

    assert resp.status_code == 200
    data = resp.json()
    filterd_course = data[0]
    assert filterd_course['name'] == course.name

@pytest.mark.django_db
def test_put_course(client, course_factory):
    courses = course_factory(_quantity=5)
    course_object = courses[3]
    course_id = course_object.id
    url = reverse('courses-detail', kwargs={'pk': course_id})

    response = client.put(url, data={'name': 'Art'})
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == course_id
    assert data['name'] == 'Art'


@pytest.mark.django_db
def test_patch_course(client, course_factory):
    courses = course_factory(_quantity=100)
    course_object = courses[67]
    course_id = course_object.id
    url = reverse('courses-detail', kwargs={'pk': course_id})

    response = client.patch(url, data={'name': 'Literature'})
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == course_id
    assert data['name'] == 'Literature'

@pytest.mark.django_db
def test_remove_course(client, course_factory):
    courses = course_factory(_quantity=100)
    course_to_delete = courses[50]
    url = reverse('courses-detail', kwargs={'pk': course_to_delete.id})
    count = Course.objects.count()

    response = client.delete(url)
    final_count = Course.objects.count()

    assert response.status_code == 204
    assert final_count == count - 1




