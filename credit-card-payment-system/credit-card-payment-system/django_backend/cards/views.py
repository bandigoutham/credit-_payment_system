from rest_framework import viewsets,permissions
from .models import Card
from .serializers import CardSerializer
from audit_logs.models import AuditEvent
class CardViewSet(viewsets.ModelViewSet):
 serializer_class=CardSerializer; permission_classes=[permissions.IsAuthenticated]
 http_method_names=["get","post","delete","head","options"]
 def get_queryset(self): return Card.objects.filter(user=self.request.user,is_active=True)
 def perform_create(self,serializer):
  card=serializer.save()
  AuditEvent.objects.create(actor=self.request.user,action="CARD_REFERENCE_CREATED",target_type="Card",target_id=str(card.pk),metadata={"card_type":card.card_type,"last4":card.last4})
 def perform_destroy(self,instance):
  instance.is_active=False; instance.save(update_fields=["is_active"])
  AuditEvent.objects.create(actor=self.request.user,action="CARD_REFERENCE_DEACTIVATED",target_type="Card",target_id=str(instance.pk))
