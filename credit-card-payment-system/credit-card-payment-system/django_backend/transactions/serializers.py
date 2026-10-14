from rest_framework import serializers
from .models import Transaction
class TransactionSerializer(serializers.ModelSerializer):
 card_last4=serializers.CharField(source="card.last4",read_only=True,allow_null=True)
 class Meta:
  model=Transaction
  fields=("public_transaction_id","card_last4","amount","currency","status","description","failure_reason","created_at","updated_at")
