from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Vendor, User, Product

class TenantRBACTests(TestCase):
    def setUp(self):
        self.v1 = Vendor.objects.create(name='V1', contact_email='a@v1.com')
        self.v2 = Vendor.objects.create(name='V2', contact_email='b@v2.com')
        self.owner = User.objects.create_user(username='owner1', password='pass', role='owner', vendor=self.v1)
        self.staff = User.objects.create_user(username='staff1', password='pass', role='staff', vendor=self.v1)
        self.client = APIClient()
        Product.objects.create(vendor=self.v1, name='p1', price=10, stock=5)
        Product.objects.create(vendor=self.v2, name='p2', price=20, stock=5)

    def test_token_contains_tenant_and_role(self):
        resp = self.client.post('/api/auth/token/', {'username':'owner1','password':'pass'}, format='json')
        self.assertEqual(resp.status_code, 200)
        access = resp.data['access']
        import jwt
        payload = jwt.decode(access, options={"verify_signature": False})
        self.assertEqual(payload.get('role'), 'owner')
        self.assertEqual(payload.get('tenant_id'), self.v1.id)

    def test_owner_sees_only_their_products(self):
        resp = self.client.post('/api/auth/token/', {'username':'owner1','password':'pass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        r = self.client.get('/api/products/')
        self.assertEqual(r.status_code, 200)
        names = [p['name'] for p in r.data]
        self.assertIn('p1', names)
        self.assertNotIn('p2', names)
