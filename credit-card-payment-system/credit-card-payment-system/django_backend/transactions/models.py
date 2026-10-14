import uuid
from django.conf import settings
from django.db import models
from cards.models import Card
def transaction_id(): return "txn_"+uuid.uuid4().hex
class Transaction(models.Model):
 STATUS_CHOICES=[("PENDING","PENDING"),("SUCCESS","SUCCESS"),("FAILED","FAILED")]
 public_transaction_id=models.CharField(max_length=40,unique=True,default=transaction_id)
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="transactions")
 card=models.ForeignKey(Card,null=True,blank=True,on_delete=models.SET_NULL,related_name="transactions")
 amount=models.DecimalField(max_digits=12,decimal_places=2); currency=models.CharField(max_length=3,default="INR")
 status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="PENDING")
 description=models.CharField(max_length=255,blank=True); idempotency_key=models.CharField(max_length=128)
 failure_reason=models.CharField(max_length=100,blank=True)
 created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta:
  ordering=["-created_at"]
  constraints=[models.UniqueConstraint(fields=["user","idempotency_key"],name="uniq_user_idempotency_key")]
  indexes=[models.Index(fields=["user","created_at"]),models.Index(fields=["status","created_at"])]
