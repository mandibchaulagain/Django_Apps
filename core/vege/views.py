from django.shortcuts import render,redirect, get_object_or_404
from .models import Recipe
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post, Comment, Like
from .forms import PostForm

@login_required(login_url='/login/')
# Create your views here.
def recipes(request):
    if request.method == "POST":

        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        user = request.user
        Recipe.objects.create(
            recipe_image= recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            user = user,
        )
        return redirect('/recipes/')
    queryset = Recipe.objects.all()

    if request.GET.get('search_re'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search_re'))


    context= {'recipes':queryset}
    return render(request, 'recipe.html',context)

def delete_recipe(request,id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/recipes/')

def update_recipe(request,id):
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        if recipe_image:
            queryset.recipe_image = recipe_image
        queryset.save()
        return redirect('/recipes/')

    context = {'recipe_data' : queryset}
    return render(request,'update_recipe.html',context)

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, 'Username already exists!')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,   
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully!')
        return redirect('/register/')
    return render(request,'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    # Add user_has_liked flag for each post and like counts
    user_likes = Like.objects.filter(user=request.user)
    liked_posts = [like.post.id for like in user_likes]
    posts_with_likes = []

    # Add like count to each post and get users who liked the post
    for post in posts:
        post.like_count = Like.objects.filter(post=post).count()
        liked_users = post.likes.values_list('user__username', flat=True)
        posts_with_likes.append({
            'post': post,
            'liked_users': liked_users
        })

    if request.method == "POST":
        # Handle like/unlike actions
        if 'like' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)

            # Toggle like status
            if post.id in liked_posts:
                Like.objects.filter(post=post, user=request.user).delete()
                liked_posts.remove(post.id)
            else:
                Like.objects.create(post=post, user=request.user)
                liked_posts.append(post.id)

        # Handle comment actions
        elif 'comment' in request.POST:
            post_id = request.POST.get('post_id')
            comment_content = request.POST.get('comment_content')
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, author=request.user, content=comment_content)

        # Redirect to the same page after handling the POST request
        return redirect('post_list')

    # Return the posts with like and comment count
    return render(request, 'post_list.html', {
        'posts_with_likes': posts_with_likes,
        'liked_posts': liked_posts,  # Pass liked posts to template
    })

# Post detail view with comments and like/unlike functionality
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    # Check if the current user has liked the post
    user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Handle liking/unliking
    if request.method == 'POST':
        if 'like' in request.POST:
            # Like the post
            if not user_has_liked:
                Like.objects.create(post=post, user=request.user)
            else:
                # Unlike the post
                Like.objects.filter(post=post, user=request.user).delete()
            # Update the user_has_liked value for the next request
            user_has_liked = not user_has_liked
        elif 'comment' in request.POST:
            # Add a new comment
            content = request.POST.get('content')
            Comment.objects.create(post=post, author=request.user, content=content)


    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'user_has_liked': user_has_liked  # Pass this to the template
    })

# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')  # Redirect to the list of posts after saving
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
