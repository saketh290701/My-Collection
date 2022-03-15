from django.contrib import admin




from .models import Post,Author,Tag,CommentModel
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("title",)}
    list_filter = ("author",) #used to filter  
    list_display =("title","author",)

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ("user_name","post")


admin.site.register(Post,PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(CommentModel,CommentModelAdmin)

