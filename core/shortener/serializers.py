from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'created_at', 'created_by', 'clicks']
        read_only_fields = ['short_code', 'created_at', 'clicks']

    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_code}/')
        return f'/{obj.short_code}/'
