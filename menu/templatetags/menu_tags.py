from django import template
from django.core.cache import cache
from django.utils.safestring import mark_safe
from menu.models import MenuItem

register = template.Library()

def render_menu(menu_items, current_url):
    menu_html = '<ul>'
    for item in menu_items:
        menu_html += '<li>'
        if item.url and (current_url == item.url or current_url.startswith(item.url + '/')):
            menu_html += '<a href="{}" class="active">{}</a>'.format(item.url, item.name)
        else:
            menu_html += '<a href="{}">{}</a>'.format(item.url, item.name)

        if item.children.all():
            menu_html += render_menu(item.children.all(), current_url)

        menu_html += '</li>'
    menu_html += '</ul>'

    return mark_safe(menu_html)

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    cache_key = f'menu_{menu_name}'
    menu_items = cache.get(cache_key)
    if menu_items is None:
        menu_items = list(MenuItem.objects.filter(parent=None).prefetch_related('children'))
        cache.set(cache_key, menu_items)
    return render_menu(menu_items, current_url)
