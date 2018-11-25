from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Attachment
from .forms import PostForm, CommentForm, AttachmentForm


def post_list(request):
    object_list = Post.objects.order_by('-id')
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        attached = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        if attached.is_valid():
            attachment = attached.save(commit=False)
            attachment.post = post
            print("after attached.is_valid", attached.is_valid())
            print("attachment.upfiles", attachment.upfiles != None)
            if attachment.upfiles != None:
                attachment.save()
                print("attachment save")
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm
        attached = AttachmentForm
        return render(request, 'blog/post_edit.html', {'form': form, 'attached': attached})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             print("request.FILES", request.FILES)
#             print("upoad file is : ", form.files)
#             #print("urls : ", form.files.urls)
#             #print("file name : ", form.files.name)
#             return render(request, 'blog/uploaded.html', {'form': form})
#     else:
#         form = UploadFileForm()
#         return render(request, 'blog/upload.html', {'form': form})
