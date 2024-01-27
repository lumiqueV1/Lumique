from django.contrib import admin


from .models import UserProfile
from .models import Photos
from .models import Vote


admin.site.register(UserProfile)
admin.site.register(Photos)
admin.site.register(Vote)
