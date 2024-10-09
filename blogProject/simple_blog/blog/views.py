from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from users.models import Follow


def post_list(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.all()

        paginator = Paginator(all_posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        your_posts = Post.objects.filter(author=request.user).order_by('-created_at')

        # Fetch posts from users you follow
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        following_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        return render(request, 'blog/post_list.html', {
            'all_posts': all_posts,
            'your_posts': your_posts,
            'following_posts': following_posts,
            'page_obj': page_obj,
        })
    else:
        return redirect('login')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and request.user == post.author:
        post.delete()
        return redirect('post_list')
    return redirect('post_detail', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)


def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)  # Search for posts with title containing the query

    return render(request, 'blog/search_result.html', {'posts': posts, 'query': query})