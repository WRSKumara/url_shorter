
# Create your models here.
from django.db import models
import random
import string

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
    
    @classmethod
    def create_short_code(cls, length=6):
        """Generate a random short code of specified length"""
        chars = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(chars) for _ in range(length))
            if not cls.objects.filter(short_code=short_code).exists():
                return short_code