from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',
         views.DashboardView.as_view(),
         name='dashboard'),

    path('my-blogs',
         views.MyBlogs.as_view(),
         name='my_blogs'),

    path('my-liked-blogs',
         views.MyLikedBlogs.as_view(),
         name='liked_blogs'),

    path('add-blog',
         views.AddBlogPost.as_view(),
         name='add_blog'),

    path('<int:pk>/update-blog',
         views.UpdateBlogPost.as_view(),
         name='update_blog'),

    path('<int:pk>/delete-blog',
         views.DeleteBlogPost.as_view(),
         name='delete_blog'),

    path('<int:pk>/blogpost',
         views.BlogPost.as_view(),
         name='blog_post'),

    path('<int:pk>/comments',
         views.BlogComments.as_view(),
         name='comments'),

    path('<int:pk>/update-comment',
         views.UpdateComment.as_view(),
         name='update_comment'),

    path('<int:pk>/like',
         views.LikePost.as_view(),
         name='blog_likes')
]
