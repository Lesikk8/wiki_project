from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Page, Section, PageVersion, AccessRight
from .forms import PageForm, SectionForm, SearchForm


def home(request):
    pages = Page.objects.filter(is_published=True).order_by('-updated_at')[:10]
    sections = Section.objects.filter(parent=None)
    return render(request, 'wiki/home.html', {
        'pages': pages,
        'sections': sections,
    })


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    versions = page.versions.all()[:5]
    return render(request, 'wiki/page_detail.html', {
        'page': page,
        'versions': versions,
    })


def section_detail(request, slug):
    section = get_object_or_404(Section, slug=slug)
    pages = section.pages.filter(is_published=True)
    children = section.children.all()
    return render(request, 'wiki/section_detail.html', {
        'section': section,
        'pages': pages,
        'children': children,
    })


@login_required
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            PageVersion.objects.create(
                page=page,
                title=page.title,
                content=page.content,
                edited_by=request.user,
                comment='Початкова версія',
            )
            messages.success(request, 'Сторінку створено!')
            return redirect('page_detail', slug=page.slug)
    else:
        form = PageForm()
    return render(request, 'wiki/page_form.html', {'form': form, 'action': 'Створити'})


@login_required
def page_edit(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            old_content = page.content
            page = form.save()
            PageVersion.objects.create(
                page=page,
                title=page.title,
                content=old_content,
                edited_by=request.user,
                comment=request.POST.get('comment', ''),
            )
            messages.success(request, 'Сторінку оновлено!')
            return redirect('page_detail', slug=page.slug)
    else:
        form = PageForm(instance=page)
    return render(request, 'wiki/page_form.html', {'form': form, 'action': 'Редагувати', 'page': page})


@login_required
def page_delete(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Сторінку видалено!')
        return redirect('home')
    return render(request, 'wiki/page_confirm_delete.html', {'page': page})


def page_history(request, slug):
    page = get_object_or_404(Page, slug=slug)
    versions = page.versions.all()
    return render(request, 'wiki/page_history.html', {
        'page': page,
        'versions': versions,
    })


def search(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ''
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Page.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True,
        )
    return render(request, 'wiki/search.html', {
        'form': form,
        'results': results,
        'query': query,
    })


@login_required
def section_create(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Розділ створено!')
            return redirect('home')
    else:
        form = SectionForm()
    return render(request, 'wiki/section_form.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'wiki/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'wiki/register.html', {'form': form})
