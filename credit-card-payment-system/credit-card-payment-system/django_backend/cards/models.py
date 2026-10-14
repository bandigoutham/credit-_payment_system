from django.conf import settings
from django.db import models
class Card(models.Model):
 CARD_TYPES=[("VISA","VISA"),("MASTERCARD","MASTERCARD"),("RUPAY","RUPAY"),("AMEX","AMEX"),("OTHER","OTHER")]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="cards")
 provider_token=models.CharField(max_length=255)
 card_type=models.CharField(max_length=20,choices=CARD_TYPES,default="OTHER")
 last4=models.CharField(max_length=4); expiry_month=models.PositiveSmallIntegerField(); expiry_year=models.PositiveSmallIntegerField()
 is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  ordering=["-created_at"]
  constraints=[models.UniqueConstraint(fields=["user","provider_token"],name="uniq_user_provider_token")]
 @property
 def masked_card_number(self): return f"**** **** **** {self.last4}"
