
from django.db import models
from datetime import date
from django.core.validators import MinLengthValidator
from django.forms import EmailField
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    caption=models.CharField(max_length=50)

    def __str__(self):
        return self.caption




class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    title=models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    # image_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="posts",null = True)
    completed_date=models.DateField()
    slug=models.SlugField(unique=True,db_index=True)
    content=models.TextField(validators=[MinLengthValidator(30)])
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True,related_name="Posts")
    tags=models.ManyToManyField(Tag)


    def __str__(self):
        return self.title

    def save(self,*args , **kwargs):
        self.slug =slugify(self.title)
        super().save(*args,**kwargs)



class CommentModel(models.Model):
    user_name = models.CharField( max_length=50)
    user_email = models.EmailField()
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name = "comments")
