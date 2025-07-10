from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from .models import Page, Rate
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from user.models import UserProgress
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.template.loader import render_to_string

from rest_framework import viewsets, generics, permissions
from .serializers import RateSerializer, PageSerializer
from .models import Rate
from rest_framework.exceptions import ValidationError

def get_seo_context(page_title, description, keywords):
    return {
        'page_title': f"{page_title} | MEO-BlogAI",
        'meta_description': description[:160],
        'meta_keywords': keywords,
        'og_title': page_title,
        'og_description': description[:200],  #
    }

def tr_slugify(text):
    tr_chars = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for char in tr_chars:
        text = text.replace(char, tr_chars[char])
    return slugify(text)

# Ana sayfa
def index(request):
    try:
        latest_contents = Page.objects.filter(
            category__in=['python', 'javascript', 'java', 'csharp', 'nlp', 'machinelearning']
        ).order_by('-last_update')[:3]

        content_images = {
            'python': 'img/python.jpeg',
            'javascript': 'img/javascript.jpeg',
            'java': 'img/java.jpeg',
            'csharp': 'img/csharp.jpeg',
            'nlp': 'img/nlp.jpeg',
            'machinelearning': 'img/makine.jpeg'
        }

        for content in latest_contents:
            if content.category: 
                content.image_url = content_images.get(content.category.lower(), 'img/default-slide.jpg')
            else:
                content.image_url = 'img/default-slide.jpg'

        seo_context = get_seo_context(
            "Programlama ve Yapay Zeka Eğitimleri",
            "Ücretsiz programlama dersleri, yazılım eğitimleri ve yapay zeka içerikleri. Python, JavaScript, Java ve daha fazlası için MEO-BlogAI.",
            "programlama, yazılım, python, javascript, java, yapay zeka, eğitim"
        )

        context = {
            "latest_contents": latest_contents,
            "pages": Page.objects.all(),
            **seo_context
        }
        return render(request, 'pages/index.html', context)
    except Exception as e:
        print(f"Index error: {e}")  # Debug için
        return render(request, 'pages/index.html', {"error": str(e)})

# Hakkında sayfası
def about(request):
    return render(request, 'pages/about.html')

def show_language_page(request, language):
    if not request.user.is_authenticated:
        return redirect('login')
        
    pages = Page.objects.filter(category=language.lower()).order_by('id')
    
    # Slug eksikse oluştur
    for page in pages:
        if not page.slug:
            page.slug = tr_slugify(page.title)
            page.save()
    
    first_page = pages.first() if pages.exists() else None

    context = {
        "pages": pages,
        "first_page": first_page,
        "language": language.title(),
    }
    return render(request, 'pages/language_page.html', context)

def get_language_detail(request, language, slug):
    try:
        page = get_object_or_404(Page, category=language.lower(), slug=slug)
        context = {
            "page": page,
            "is_admin": request.user.is_superuser,
            "pages": Page.objects.filter(category=language.lower()),
            "language": language,
            "average_rating": page.average_rate(),
            "rates": page.rates.all()
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            content = render_to_string('pages/detail.html', context, request=request)
            return JsonResponse({
                'status': 'success',
                'content': content,
                'title': f"{page.title} - {language} Dersleri"
            })

        return render(request, 'pages/language_page.html', context)
    except Exception as e:
        print(f"Hata: {e}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=404)
        raise

def python(request):
    return show_language_page(request, "python")

def python_detail(request, slug):
    return get_language_detail(request, "python", slug)

def csharp(request):
    return show_language_page(request, "csharp")

def csharp_detail(request, slug):
    return get_language_detail(request, "csharp", slug)

def javascript(request):
    return show_language_page(request, "javascript")

def javascript_detail(request, slug):
    return get_language_detail(request, "javascript", slug)

def java(request):
    return show_language_page(request, "java")

def java_detail(request, slug):
    return get_language_detail(request, "java", slug)



def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Page.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    else:
        results = []
    
    context = {
        'query': query,
        'results': results,
        'count': len(results)
    }
    return render(request, 'pages/search.html', context)

def is_admin(user):
    return user.is_superuser

@require_POST
@user_passes_test(is_admin)
def delete_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        category = page.category
        page.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Sayfa başarıyla silindi',
            'redirect_url': f'/courses/{category}/'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@user_passes_test(is_admin)
def save_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        page.title = request.POST.get('title')
        page.content = request.POST.get('content')
        page.category = request.POST.get('category')
        page.save()
        return JsonResponse({
            'status': 'success',
            'message': 'İçerik başarıyla güncellendi'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@user_passes_test(is_admin)
def edit_page(request, page_id):
    try:
        page = get_object_or_404(Page, id=page_id)
        if request.method == "GET":
            context = {
                'page': page,
                'categories': ['python', 'javascript', 'java', 'csharp', 'nlp', 'machinelearning']
            }
            return render(request, 'pages/edit_page.html', context)
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class PageViewset(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class RateListCreateView(generics.ListCreateAPIView):
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        page_id = self.kwargs.get('page_id')
        return Rate.objects.filter(page_id=page_id)

    def perform_create(self, serializer):
        page_id = self.kwargs.get('page_id')
        user = self.request.user
        if Rate.objects.filter(page_id=page_id, user=user).exists():
            raise ValidationError("Bu sayfa için zaten puan verdiniz.")
        serializer.save(page_id=page_id, user=user)

def add_rate(request, page_id):
    if request.method == 'POST':
        page = get_object_or_404(Page, id=page_id)
        value = request.POST.get('value')
        comment = request.POST.get('comment', '').strip()

        if not value:
            messages.error(request, "Lütfen bir puan seçin!")
            return redirect('language_detail', language=page.category, slug=page.slug)

        try:
            rate = Rate.objects.update_or_create(
                page=page,
                user=request.user,
                defaults={
                    'score': int(value),
                    'comment': comment
                }
            )[0]
            messages.success(request, "Değerlendirmeniz kaydedildi!")
        except Exception as e:
            print(f"Rate error: {e}")
            messages.error(request, "Değerlendirme kaydedilirken bir hata oluştu!")
            
        return redirect('language_detail', language=page.category, slug=page.slug)
    return HttpResponseBadRequest()

def get_page_content(request, language, slug):
    try:
        page = get_object_or_404(Page, category=language, slug=slug)
        context = {
            'page': page,
            'average_rating': page.average_rate(),
            'language': language,
            'is_admin': request.user.is_superuser,
            'rates': Rate.objects.filter(page=page)
        }
        return JsonResponse({
            'status': 'success',
            'content': render_to_string('pages/detail.html', context, request=request),
            'title': page.title
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)