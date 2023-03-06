import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
from django.conf import settings


@pytest.fixture
def client():
    return APIClient()


# m2m фикстура
@pytest.fixture
def courses_student_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, make_m2m=True, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('Student', **kwargs)

    return factory


# Проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_course_retrieve(client, courses_student_factory):
    # Arrange
    course = courses_student_factory()
    url = reverse('courses-detail', args=(str(course.pk),))

    # Act
    response = client.get(url)
    data = response.json()

    # Assert
    assert response.status_code == HTTP_200_OK
    assert data.get('name') == course.name


# Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_course_list(client, courses_student_factory):
    # Arrange
    course = courses_student_factory(_quantity=10)
    url = reverse('courses-list')

    # Act
    response = client.get(url)
    data = response.json()

    # Assert
    assert response.status_code == HTTP_200_OK
    assert len(data) == len(course)


# Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_course_filter_id(client, courses_student_factory):
    # Arrange
    course = courses_student_factory(_quantity=10)
    course_id = course[3].pk
    url = f"{reverse('courses-list')}?id={course_id}"

    # Act
    response = client.get(url)
    data = response.json()

    # Assert
    assert response.status_code == HTTP_200_OK
    assert data[0].get('name') == course[3].name
    assert len(data) == 1


# Проверка фильтрации списка курсов по полю name
@pytest.mark.django_db
def test_course_filter_name(client, courses_student_factory):
    # Arrange
    course = courses_student_factory(_quantity=10)
    course_name = course[3].name
    url = f"{reverse('courses-list')}?name={course_name}"

    # Act
    response = client.get(url)
    data = response.json()

    # Assert
    assert response.status_code == HTTP_200_OK
    assert data[0].get('name') == course[3].name
    assert len(data) == 1


# Тест успешного создания курса
@pytest.mark.django_db
def test_course_create(client):
    # Arrange
    student = Student.objects.create(name='student1')
    url = reverse('courses-list')
    count = Course.objects.count()

    # Act
    response = client.post(url, data={'name': 'course1', 'students': student.pk})
    data = response.json()

    # Assert
    assert response.status_code == HTTP_201_CREATED
    assert data.get('name') == 'course1'
    assert Course.objects.count() == count + 1


# Тест успешного обновления курса
@pytest.mark.django_db
def test_course_update(client, courses_student_factory):
    # Arrange
    course = courses_student_factory()
    url = reverse('courses-detail', args=(str(course.pk),))

    # Act
    response = client.patch(url, data={'name': 'test_name'})
    data = response.json()

    # Assert
    assert response.status_code == HTTP_200_OK
    assert data.get('name') == 'test_name'


# Тест успешного удаления курса.
@pytest.mark.django_db
def test_course_delete(client, courses_student_factory):
    # Arrange
    course = courses_student_factory(_quantity=50)
    course_id = course[3].pk
    url = reverse('courses-detail', args=(str(course_id),))
    count = Course.objects.count()

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == HTTP_204_NO_CONTENT
    assert Course.objects.count() == count - 1


@pytest.mark.parametrize("max_count_student, http_status_code",
                         [
                             (0, HTTP_400_BAD_REQUEST),
                             (2, HTTP_201_CREATED)
                         ])
# Тест проверки валидации на максимальное число студентов на курсе — 20.
@pytest.mark.django_db
def test_validate(max_count_student, http_status_code, client, course_factory, student_factory):
    # Arrange
    settings.MAX_STUDENTS_PER_COURSE = max_count_student
    url = reverse('courses-list')
    data = {
        'name': course_factory().name,
        'students': [student_factory().id],
    }

    # Act
    response = client.post(url, data=data)

    # Assert
    assert response.status_code == http_status_code

# Вариант без использования model_bakery
# @pytest.mark.django_db
# def test_course_retrieve(client):
#     # Arrange
#     student = Student.objects.create(name='student1')
#     course = Course.objects.create(name='курс1')
#     student_course = course.students.add(student)
#
#     # Act
#     url = reverse('courses-detail', args=(str(course.pk),))
#     response = client.get(url)
#
#     # Assert
#     assert response.status_code == HTTP_200_OK
#     data = response.json()
#     assert data.get('name') == course.name
