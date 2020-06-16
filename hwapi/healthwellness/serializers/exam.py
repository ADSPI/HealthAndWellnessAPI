from rest_framework import serializers
from ..models import MedicalExam
from .doctor import DoctorSerializer


class MedicalExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalExam
        fields = '__all__'


class MedicalExamDoctorSerializer(serializers.ModelSerializer):

    doctor = DoctorSerializer(read_only=True, many=False)

    class Meta:
        model = MedicalExam
        fields = '__all__'
