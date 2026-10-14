from datetime import date
from rest_framework import serializers
from .models import Card
class CardSerializer(serializers.ModelSerializer):
 masked_card_number=serializers.CharField(read_only=True)
 class Meta:
  model=Card
  fields=("id","card_type","masked_card_number","last4","expiry_month","expiry_year","is_active","created_at","provider_token")
  read_only_fields=("id","masked_card_number","is_active","created_at")
  extra_kwargs={"provider_token":{"write_only":True}}
 def validate_last4(self,value):
  if len(value)!=4 or not value.isdigit(): raise serializers.ValidationError("last4 must contain exactly four digits.")
  return value
 def validate_expiry_month(self,value):
  if not 1<=value<=12: raise serializers.ValidationError("expiry_month must be between 1 and 12.")
  return value
 def validate(self,attrs):
  year=attrs.get("expiry_year",getattr(self.instance,"expiry_year",None)); month=attrs.get("expiry_month",getattr(self.instance,"expiry_month",None))
  if year and month and (year,month)<(date.today().year,date.today().month): raise serializers.ValidationError("Card reference is expired.")
  return attrs
 def create(self,validated_data): return Card.objects.create(user=self.context["request"].user,**validated_data)
