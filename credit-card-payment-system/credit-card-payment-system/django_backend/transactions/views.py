import csv
from datetime import date
from decimal import Decimal,InvalidOperation
from django.http import HttpResponse
from django.db.models import Count,Sum
from django.db.models.functions import TruncDate
from rest_framework import viewsets,permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=TransactionSerializer; permission_classes=[permissions.IsAuthenticated]; lookup_field="public_transaction_id"
 def get_queryset(self):
  qs=Transaction.objects.filter(user=self.request.user).select_related("card").order_by("-created_at","-id"); p=self.request.query_params
  if p.get("status"):
   if p["status"] not in {"PENDING","SUCCESS","FAILED"}: raise ValidationError({"status":"Must be PENDING, SUCCESS, or FAILED."})
   qs=qs.filter(status=p["status"])
  for key,lookup in (("from_date","created_at__date__gte"),("to_date","created_at__date__lte")):
   if p.get(key):
    try: date.fromisoformat(p[key])
    except ValueError: raise ValidationError({key:"Use YYYY-MM-DD."})
    qs=qs.filter(**{lookup:p[key]})
  amounts={}
  for key,lookup in (("min_amount","amount__gte"),("max_amount","amount__lte")):
   if p.get(key):
    try: amount=Decimal(p[key])
    except InvalidOperation: raise ValidationError({key:"Must be a decimal amount."})
    if amount<0: raise ValidationError({key:"Must be non-negative."})
    amounts[key]=amount; qs=qs.filter(**{lookup:amount})
  if len(amounts)==2 and amounts["min_amount"]>amounts["max_amount"]: raise ValidationError({"amount":"min_amount cannot exceed max_amount."})
  return qs
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def transaction_export(request):
 response=HttpResponse(content_type="text/csv"); response["Content-Disposition"]='attachment; filename="transactions.csv"'
 writer=csv.writer(response); writer.writerow(["transaction_id","username","amount","currency","status","created_at"])
 for tx in Transaction.objects.select_related("user").order_by("-created_at").iterator():
  tid="'"+tx.public_transaction_id if tx.public_transaction_id.startswith(("=","+","-","@")) else tx.public_transaction_id
  writer.writerow([tid,tx.user.username,str(tx.amount),tx.currency,tx.status,tx.created_at.isoformat()])
 return response
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def daily_summary(request):
 rows=Transaction.objects.annotate(day=TruncDate("created_at")).values("day","status").annotate(count=Count("id"),total=Sum("amount")).order_by("-day","status")
 return Response([{"date":r["day"],"status":r["status"],"count":r["count"],"total":r["total"] or Decimal("0.00")} for r in rows])
