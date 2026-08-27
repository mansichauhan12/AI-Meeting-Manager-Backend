from rest_framework import serializers

class SearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    workspace_id = serializers.IntegerField(required=True)
