from rest_framework import serializers
from ..models import MedicalExam


class MedicalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalExam
        fields = '__all__'
