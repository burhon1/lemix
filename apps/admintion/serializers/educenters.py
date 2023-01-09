from rest_framework import serializers

from admintion.models import EduCenters

class EducentersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EduCenters
        fields = "__all__"