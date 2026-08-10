from django.http import JsonResponse
from django.shortcuts import render

from cms.models import PageContent

from .models import PageContentIndex, PageTag, Setting


def search_results(request):
    """Global site search across page titles and indexed plugin content."""
    query = request.GET.get("q", "").strip()
    pages = []

    if query:
        matching_content = PageContent.admin_manager.filter(title__icontains=query)
        for content in matching_content:
            if content.page not in pages:
                pages.append(content.page)

        content_pages = PageContentIndex.objects.filter(content__icontains=query)
        for content_page in content_pages:
            if content_page.page not in pages:
                pages.append(content_page.page)

    filter_tags = PageTag.objects.filter(search_category=True)
    category_results = {}

    for page in pages:
        extension = getattr(page, "pagepreviewextension", None)
        if not extension:
            continue
        for page_tag in extension.tags.all():
            if page_tag in filter_tags:
                category_results.setdefault(page_tag, [])
                if page not in category_results[page_tag]:
                    category_results[page_tag].append(page)

    return render(
        request,
        "search.html",
        {
            "query": query,
            "search_results": pages,
            "category_results": category_results,
        },
    )


def handler404(request, *args, **kwargs):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def manifest(request):
    site_name_setting = Setting.objects.filter(key="Site Name").first()
    site_name = site_name_setting.value if site_name_setting else "ND Theme CMS"

    return JsonResponse(
        {
            "lang": "en",
            "dir": "ltr",
            "name": site_name,
            "short_name": request.get_host(),
            "start_url": "/",
            "display": "minimal-ui",
            "theme_color": "#0c2340",
            "background_color": "#0c2340",
            "icons": [
                {
                    "src": "https://static.nd.edu/images/monogram/gold/monogram-192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": "https://static.nd.edu/images/monogram/gold/monogram-512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
        }
    )
