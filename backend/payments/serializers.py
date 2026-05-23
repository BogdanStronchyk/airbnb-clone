from rest_framework import serializers
from .models import CancellationPolicy, Payout

class CancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationPolicy
        fields = ['id', 'name', 'description', 'days_before_start', 'refund_percentage']
