from django.shortcuts import render, get_object_or_404
from .models import Post

def home_view(request):
    return render(request, 'home.html')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "home/post_detail.html", {"post": post})
