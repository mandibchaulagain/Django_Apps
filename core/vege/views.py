from django.shortcuts import render,redirect, get_object_or_404
from .models import Recipe
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post, Comment, Like
from .forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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

        # Validate inputs
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            })

        # Validate password
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.error(request, 'Password must be at least 8 characters long, contain letters and numbers.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            })

        # Create the user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('/login/')
    
    return render(request, 'register.html')


def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = request.user

        # Check if current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('/change_password/')

        # Check if new passwords match
        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return redirect('/change_password/')

        try:
            # Validate the new password
            validate_password(new_password, user=user)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect('/change_password/')

        # Update password after validation
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully! Please log in again.")
        return redirect('/login/')

    return render(request, 'change_password.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def post_list(request):
    posts = Post.objects.filter(privacy = Post.PUBLIC).order_by('-created_at')
    # .order_by('-created_at')

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

    # Get the users who liked the post (to be passed to the modal)
    liked_users = post.likes.values_list('user__username', flat=True)

    # Check if the current user has liked the post
    user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Handle liking/unliking
    if request.method == 'POST':
        if 'like' in request.POST:
            # Like or Unlike the post based on current state
            if not user_has_liked:
                Like.objects.create(post=post, user=request.user)
            else:
                Like.objects.filter(post=post, user=request.user).delete()
            # Update the user_has_liked value for the next request
            user_has_liked = not user_has_liked
        elif 'comment' in request.POST:
            # Add a new comment
            content = request.POST.get('content')
            Comment.objects.create(post=post, author=request.user, content=content)

        # Redirect to the same page after POST request to avoid resubmission
        return redirect('post_detail', post_id=post_id)

    # GET request or redirected after POST
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'user_has_liked': user_has_liked,
        'liked_users': liked_users  # Pass the list of users who liked the post
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

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'user_profile.html', context)

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure only the author can edit the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Redirect to the list of posts after saving
    else:
        form = PostForm(instance=post)  # Prepopulate the form with the post data

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure that only the post's author can delete the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect('post_list')  # Redirect to the post list after deletion

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure that only the comment's author can delete the comment
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    comment.delete()
    return redirect('post_detail', post_id=comment.post.id)  # Redirect back to the post's detail page