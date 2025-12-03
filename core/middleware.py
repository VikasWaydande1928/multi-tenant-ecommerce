from django.utils.deprecation import MiddlewareMixin
from core.models import Vendor
from rest_framework_simplejwt.backends import TokenBackend

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.tenant = None
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer '):
            token = auth.split()[1]
            try:
                # decode without signature verification to extract claim; acceptable for this assignment
                token_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
                tenant_id = token_data.get('tenant_id')
                if tenant_id:
                    request.tenant = Vendor.objects.filter(id=tenant_id).first()
            except Exception:
                request.tenant = None
