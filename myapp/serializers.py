from rest_framework import serializers
from .models import myproject
class myprojectSerializer(serializers.ModelSerializer):
    class Meta:
        model = myproject
        fields = ["task", "completed", "timestamp", "updated", "user"]