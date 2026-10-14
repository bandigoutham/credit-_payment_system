from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
class AuthenticationTests(APITestCase):
 def test_registration_hashes_password(self):
  r=self.client.post("/api/auth/register/",{"username":"test_user","email":"test@example.com","password":"Strong-Test-Password-123!"},format="json")
  self.assertEqual(r.status_code,201)
  user=get_user_model().objects.get(username="test_user")
  self.assertNotEqual(user.password,"Strong-Test-Password-123!")
  self.assertTrue(user.check_password("Strong-Test-Password-123!"))
 def test_me_requires_auth(self): self.assertEqual(self.client.get("/api/auth/me/").status_code,401)
