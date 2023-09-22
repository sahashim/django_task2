from django.views.generic import ListView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .models import Post, Category
from .forms import *


@login_required
def delete_post(request, slug):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, slug=slug)
    context = {'post': post}

    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html', context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request, 'The post has been deleted successfully.')
        return redirect('posts')


@login_required
def edit_post(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, slug=slug)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': id}
        return render(request, 'blog/post_form.html', context)

    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'blog/post_form.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'GET':
        context = {'form': PostForm()}
        return render(request, 'blog/post_form.html', context)
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('posts')
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'blog/post_form.html', {'form': form})


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):
    queryset = Post.objects.filter(status='PB')
    template_name = 'blog/detail.html'
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        print(post)
        session_key = 'viewed_post_{}'.format(post.id)
        if not request.session.get(session_key, False):
            post.views +=1
            post.save()

        context = {
            'post' : post,
            'post_dict': {
                'title':post.title,
                'description':post.description,
                'author':post.author,
                'views':post.views,
                'date_published':post.publish,
            }

        }
        return render(request, 'blog/detail.html',context)

@login_required
def post_detail(request, slug):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(status='PB')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                                  'comments': comments,
                                                  'new_comment': new_comment,
                                                  'comment_form': comment_form
                                           })



class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = (str(self.kwargs['slug'])).replace("-"," ")
        return Post.objects.filter(category__title=category)