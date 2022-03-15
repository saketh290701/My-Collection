from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views import View

from .models import Post,Author,Tag
from .forms import CommentForm 

# Create your views here.

# def helper_get_date(post):
#     return post['completed_date']




class indexView(ListView):
    template_name="blog/index.html"
    model = Post
    ordering = ["-completed_date"]
    context_object_name = "latest_posts"

    def get_queryset(self):
        queryset=  super().get_queryset()
        data = queryset[:3]
        return data

'''

def index(request):
    latest_posts=Post.objects.all().order_by("-completed_date")[:3]
    # sorted_posts=sorted(all_posts , key=helper_get_date)
    # latest_posts=sorted_posts[-3:]
    return render(request,"blog/index.html",{
        "latest_posts":latest_posts,
    })
'''
class postsView(ListView):
    template_name = "blog/all-posts-page.html"
    model = Post
    ordering = ["-completed_date"]
    context_object_name = "all_posts"


'''
def posts(request):
    all_posts=Post.objects.all()
    return render(request,"blog/all-posts-page.html",{
        "all_posts":all_posts,

    })
'''


class post_detailView(View):
    # template_name="blog/post-detail.html"
    # model = Post   #->since we use View and not Detailview
    def is_favourited_post(slef,request,post_id):
        StoredPosts = request.session.get("stored_posts")
        if StoredPosts is not None:
            favouritedPosts = post_id in StoredPosts
        else:
            favouritedPosts = False

        return favouritedPosts
         

    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        
        
        context = {
            "post" : post,
            "post_tags" : post.tags.all(),    #->to aplly tags in our post-detail page
            "comment_form" : CommentForm(),
            "comments" : post.comments.all().order_by("-id"), #name given to post section in CommentModel model
            "favourited_books" : self.is_favourited_post(request,post.id),
        }
        return render(request,"blog/post-detail.html",context)


    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # the commit=False ables not to hit the database but just craete a model instance
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))

        context={
                "post" : post,
                "post_tags" : post.tags.all(),    #->to aplly tags in our post-detail page
                "comment_form" : CommentForm(),
                "comments" : post.comments.all().order_by("-id"), #name given to post section in CommentModel model
                "favourited_books" : self.is_favourited_post(request,post.id),
            }
        return render(request,"blog/post-detail.html",context)



    # def get_context_data(self, **kwargs):
    #    context =  super().get_context_data(**kwargs)
    # #    context["posts_tag"] = self.object.tags.all()     #->to aplly tags in our post-detail page

    #    context["comment_form"] = CommentForm()
    #    return context                            

'''
def post_detail(request,slug):
    identified_post=Post.objects.get(slug=slug)
    #identified_post=get_object_or_404(Post,slug=slug)
    return render(request,"blog/post-detail.html",{
        "post":identified_post,
    })
'''


class FavouriteView(View):

    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts) == 0:
            context["favPosts"]=[]
            context["has_posts"]=False
        
        else:
            favPosts = Post.objects.filter(id__in=stored_posts)
            context["favPosts"]=favPosts
            context["has_posts"] = True

        return render(request,"blog/favourites.html",context)

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts= []

        post_id = int(request.POST["post_id"])
        post_slug = Post.objects.get(id=post_id).slug

        if post_id not in stored_posts:
            stored_posts.append(post_id) #based on name giuven in form
            
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect(reverse("post-detail-page",args=[post_slug]))