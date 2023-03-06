from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attr):
        http_method = self.context["request"].method
        if http_method == 'POST':
            student_count = len(attr.get('students'))
            if student_count >= settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(f'Вы превысили максимальное число студентов на курсе:'
                                      f' {settings.MAX_STUDENTS_PER_COURSE}')

        return attr
