from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.


from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display=('q_title','user')
    search_fields=('q_title','content')

admin.site.register(UserProfile)
# admin.site.register(user)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
# admin.site.register(Notification)
# admin.site.register(UserProfile)
admin.site.register(Comment)

class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','comment')
admin.site.register(UpVote)
admin.site.register(DownVote)