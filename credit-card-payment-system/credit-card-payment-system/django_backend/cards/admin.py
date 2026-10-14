from django.contrib import admin
from .models import Card
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
 list_display=("id","user","card_type","last4","expiry_month","expiry_year","is_active","created_at")
 list_filter=("card_type","is_active"); search_fields=("user__username","last4")
 exclude=("provider_token",)
