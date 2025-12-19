import json
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Post, User


# Public endpoints
@require_http_methods(["GET"])
def view_post(request, post_id):
    """Get a single post by ID"""
    try:
        post = get_object_or_404(Post, id=post_id)
        return JsonResponse(post.to_dict())
    except Exception as _e:
        return JsonResponse({"error": "Post not found"}, status=404)


@require_http_methods(["GET"])
def timeline(request, number):
    """Get recent posts (timeline)"""
    try:
        number = int(number)
        if number <= 0:
            return JsonResponse({"error": "Invalid number"}, status=400)

        posts = Post.objects.all()[:number]
        posts_data = [post.to_dict() for post in posts]
        return JsonResponse(posts_data, safe=False)
    except ValueError:
        return JsonResponse({"error": "Invalid number format"}, status=400)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


@require_http_methods(["GET"])
def like_post(request, post_id):
    """Like a post (increment like count)"""
    try:
        with transaction.atomic():
            post = get_object_or_404(Post, id=post_id)
            post.liked += 1
            post.save()
            return JsonResponse({"liked": post.liked})
    except Exception as _e:
        return JsonResponse({"error": "Post not found"}, status=404)


# Authenticated endpoints
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def create_post(request):
    """Create a new post"""
    try:
        data = json.loads(request.body)
        content = data.get("content", "").strip()
        related_id = data.get("related")

        if not content:
            return JsonResponse({"error": "Content is required"}, status=400)

        if len(content) > 1000:
            return JsonResponse(
                {"error": "Content too long (max 1000 characters)"}, status=400
            )

        # Validate related post if provided
        related_post = None
        if related_id:
            try:
                related_post = Post.objects.get(id=related_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Related post not found"}, status=404)

        # Create new post
        post = Post(
            account=request.user,
            content=content,
            related=related_post,
            time=int(time.time()),
        )
        post.save()

        return JsonResponse({"id": post.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def edit_post(request, post_id):
    """Edit an existing post (owner only)"""
    try:
        post = get_object_or_404(Post, id=post_id)

        # Check if user is the owner
        if post.account != request.user:
            return JsonResponse({"error": "Permission denied"}, status=403)

        data = json.loads(request.body)
        content = data.get("content", "").strip()
        related_id = data.get("related")

        if not content:
            return JsonResponse({"error": "Content is required"}, status=400)

        if len(content) > 1000:
            return JsonResponse(
                {"error": "Content too long (max 1000 characters)"}, status=400
            )

        # Validate related post if provided
        related_post = None
        if related_id:
            try:
                related_post = Post.objects.get(id=related_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Related post not found"}, status=404)

        # Update post
        post.content = content
        post.related = related_post
        post.save()

        return JsonResponse({})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def delete_post(request, post_id):
    """Delete a post (owner only)"""
    try:
        post = get_object_or_404(Post, id=post_id)

        # Check if user is the owner
        if post.account != request.user:
            return JsonResponse({"error": "Permission denied"}, status=403)

        post.delete()
        return JsonResponse({})

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


# Authentication endpoints
@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    """Create a new user account"""
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        # Create new user
        User.objects.create_user(username=username, password=password)

        return JsonResponse({"message": "Account created successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """User login"""
    try:
        data = json.loads(request.body)
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as _e:
        return JsonResponse({"error": "Internal server error"}, status=500)


@require_http_methods(["POST"])
def logout_view(request):
    """User logout"""
    logout(request)
    return JsonResponse({"message": "Logout successful"})
