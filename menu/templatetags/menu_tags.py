from django import template
from menu.models import MenuItem
from django.utils.safestring import mark_safe
from django.core.cache import cache

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    cache_key = f'menu_{menu_name}'
    menu_html = cache.get(cache_key)
    if menu_html is not None:
        return mark_safe(menu_html)
    
    menu_items = MenuItem.objects.filter(parent=None).prefetch_related('children')
    menu_html = ''

    for item in menu_items:
        menu_html += '<li>'
        if item.url and (current_url == item.url or current_url.startswith(item.url + '/')):
            menu_html += '<a href="{}" class="active">{}</a>'.format(item.url, item.name)
        else:
            menu_html += '<a href="{}">{}</a>'.format(item.url, item.name)

        if item.children.all():
            menu_html += '<ul>'
            for child in item.children.all():
                menu_html += '<li>'
                if child.url and (current_url == child.url or current_url.startswith(child.url + '/')):
                    menu_html += '<a href="{}" class="active">{}</a>'.format(child.url, child.name)
                else:
                    menu_html += '<a href="{}">{}</a>'.format(child.url, child.name)
                menu_html += '</li>'
            menu_html += '</ul>'

        menu_html += '</li>'

    cache.set(cache_key, menu_html)

    return mark_safe(menu_html)
