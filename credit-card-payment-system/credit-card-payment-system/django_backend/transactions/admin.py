from django.contrib import admin
from .models import Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
 list_display=("public_transaction_id","user","amount","currency","status","created_at")
 list_filter=("status","currency","created_at"); search_fields=("public_transaction_id","user__username")
 readonly_fields=tuple(f.name for f in Transaction._meta.fields)
 def has_add_permission(self,request): return False
 def has_delete_permission(self,request,obj=None): return False
