from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
class CardOwnershipTests(APITestCase):
 def setUp(self):
  self.user=get_user_model().objects.create_user(username="owner",password="Strong-Test-Password-123!")
  self.other=get_user_model().objects.create_user(username="other",password="Strong-Test-Password-123!")
 def auth(self,user): self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {AccessToken.for_user(user)}")
 def test_card_only_visible_to_owner(self):
  self.auth(self.user)
  r=self.client.post("/api/cards/",{"provider_token":"demo-token","card_type":"VISA","last4":"1234","expiry_month":12,"expiry_year":2028},format="json")
  self.assertEqual(r.status_code,201); card_id=r.data["id"]
  self.auth(self.other)
  self.assertEqual(self.client.delete(f"/api/cards/{card_id}/").status_code,404)
