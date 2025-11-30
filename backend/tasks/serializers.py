from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.CharField(allow_null=True, required=False)
    estimated_hours = serializers.FloatField(required=False)
    importance = serializers.IntegerField(required=False)
    dependencies = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
