from django.views.generic.base import TemplateView, View
from django.shortcuts import redirect, render
from django.contrib.auth import logout

from django import forms

from .models import Blogs, Comments, Likes
from .forms import BlogForm, CommentsForm

from pdb import set_trace


class DashboardView(TemplateView):
    def get(self, request):

        if request.user.is_authenticated:
            blog = Blogs.objects.all()  # returns query set

            return render(request, 'blogs/dashboard.html', {'blogs': blog})
        else:
            return redirect('users:login')


class BlogPost(TemplateView):

    def get(self, request, **kwargs):

        blog = Blogs.objects.get(id=kwargs.get('pk'))
        comment = Comments.objects.filter(blog=blog)

        total_likes = Likes.objects.filter(like=True,
                                           blog=blog).count()

        commentform = CommentsForm()  # initialize form

        context = {
            'post': blog,
            'comments': comment,
            'form': commentform,
            'likes': total_likes
        }

        return render(request, 'blogs/blogpost.html', context)


class AddBlogPost(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            addform = BlogForm()

            return render(request, 'blogs/add-blog.html', {'form': addform})
        else:
            return redirect('users:login')

    def post(self, request):
        addform = BlogForm(request.POST)

        if addform.is_valid():
            # turn into blog object and saved into memory because of missing field
            add_blog = addform.save(commit=False)
            add_blog.author = request.user  # official user
            addform.save()

            return redirect('blog:dashboard')
        else:
            return render(request, 'blogs/add-blog.html', {'form': addform})


class UpdateBlogPost(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            blogpost = Blogs.objects.get(id=kwargs.get('pk'))

            if blogpost.author == request.user:
                # binded ang instance sa model form
                updateform = BlogForm(instance=blogpost)

                context = {
                    'form': updateform,
                    'blogpost': blogpost
                }

                return render(request, 'blogs/update-blog.html', context)
            else:
                return redirect('blog:blog_post', blogpost.id)
        else:
            return redirect('users:login')

    def post(self, request, **kwargs):
        blogpost = Blogs.objects.get(id=kwargs.get('pk'))
        updateform = BlogForm(request.POST, instance=blogpost)

        if blogpost.author == request.user:
            if updateform.is_valid():
                updateform.save()

                return redirect('blog:blog_post', blogpost.id)
            else:
                return redirect('blog:blog_post', blogpost.id)
        else:
            return redirect('users:login')


class DeleteBlogPost(TemplateView):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            blog = Blogs.objects.get(id=kwargs.get('pk'))
            blog.delete()

            return render(request, 'blogs/delete-blog.html')
        else:
            return redirect('users:login')


class MyBlogs(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            blog = Blogs.objects.filter(author=request.user)

            return render(request, 'blogs/my-blogs.html', {'blogs': blog})
        else:
            return redirect('users:login')


class BlogComments(View):
    def get(self, request, **kwargs):

        # DELETE COMMENT
        if request.user.is_authenticated:
            current_comment = Comments.objects.get(id=kwargs.get('pk'))

            current_comment.delete()
            return redirect('blog:blog_post', current_comment.blog.id)

        else:
            return redirect('blog:blog_post', current_comment.blog.id)

    def post(self, request, **kwargs):
        blog = Blogs.objects.get(id=kwargs.get('pk'))
        comment = Comments.objects.filter(blog=blog)

        commentform = CommentsForm(request.POST)

        # ADD COMMENT
        if commentform.is_valid():
            add_comment = commentform.save(
                commit=False)  # turn into comment object and save into memory, missing user field
            add_comment.user = request.user  # official user
            add_comment.blog = blog

            add_comment.save()

            return redirect('blog:blog_post', pk=kwargs.get('pk'))
        else:
            context = {
                'form': commentform,
                'post': blog,
                'comments': comment
            }
            return render(request, 'blogs/blogpost.html', context)


class UpdateComment(View):
    def get(self, request, **kwargs):
        # UPDATE COMMENT
        if request.user.is_authenticated:
            current_comment = Comments.objects.get(id=kwargs.get('pk'))

            update_form = CommentsForm(instance=current_comment)

            return render(request, 'blogs/update-comment.html', {'form': update_form})
        else:
            return redirect('users:login')

    def post(self, request, **kwargs):
        current_comment = Comments.objects.get(id=kwargs.get('pk'))

        update_form = CommentsForm(request.POST, instance=current_comment)

        if update_form.is_valid():
            update_form.save()

            return redirect('blog:blog_post', current_comment.blog.id)
        else:
            return redirect('blog:blog_post', current_comment.blog.id)


class LikePost(View):
    def get(self, request, **kwargs):
        blog = Blogs.objects.get(id=kwargs.get('pk'))

        try:  # check if there is an error
            blog_like = Likes.objects.get(
                user=request.user,
                blog=blog)  # query if there is an instance

            blog_like.like = not blog_like.like  # negate the value, handles like/unlike
            blog_like.save()

            return redirect('blog:blog_post', blog.id)
        except:  # executes when there is an error in try block
            new_like = Likes.objects.create(user=request.user,
                                            blog=blog)

            return redirect('blog:blog_post', blog.id)


class MyLikedBlogs(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:

            # likes is the model, user is the field
            blog = Blogs.objects.filter(
                likes__user=request.user, likes__like=True)

            # get all blogs where the user in the likes model is equal to the current user, and the like value is true

            return render(request, 'blogs/my-liked-blogs.html', {'blogs': blog})
        else:
            return redirect('users:login')
