from django.conf import settings
from django.db import models
class AuditEvent(models.Model):
 actor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
 action=models.CharField(max_length=80); target_type=models.CharField(max_length=80)
 target_id=models.CharField(max_length=80,blank=True); metadata=models.JSONField(default=dict,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=["-created_at"]
