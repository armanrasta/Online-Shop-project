from django.http import HttpResponseForbidden
from django.core.cache import cache

class DoSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = 60 # seconds
        self.request_limit = 5

    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f'ddos:{ip.address}'
        
        request_count = cache.get(cache_key, 0)
        request_count += 1
        
        if request_count > self.request_limit:
            # Too many requests within the time window; forbid the request.
            return HttpResponseForbidden("Request limit exceeded. Please try again later.")
            
        # Set or update the cache with the incremented request count.
        cache.set(cache_key, request_count, self.time_window)
         
        return None
    
    def __call__(self,request):
         return self.process_request(request) or self.get_response(request)

# settings.py
