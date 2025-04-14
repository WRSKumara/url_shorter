
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import ShortenedURL
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """Home page with URL shortening form"""
    return render(request, 'shortener/home.html')

@csrf_exempt
def create_short_url(request):
    """Create a shortened URL"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            original_url = data.get('url')
            
            if not original_url:
                return JsonResponse({'error': 'URL is required'}, status=400)
            
            # Generate short code
            short_code = ShortenedURL.create_short_code()
            
            # Create and save the shortened URL
            shortened_url = ShortenedURL(
                original_url=original_url,
                short_code=short_code
            )
            shortened_url.save()
            
            # Build the full shortened URL
            short_url = request.build_absolute_uri(f'/{short_code}/')
            
            return JsonResponse({
                'short_url': short_url,
                'original_url': original_url
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def redirect_to_original(request, short_code):
    """Redirect to the original URL from a short code"""
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    shortened_url.clicks += 1
    shortened_url.save()
    return redirect(shortened_url.original_url)