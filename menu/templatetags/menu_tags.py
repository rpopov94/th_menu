from django import template
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
    menu_items = MenuItem.objects.filter(name=menu_name).prefetch_related('children')
    return render_menu(menu_items, current_url)
