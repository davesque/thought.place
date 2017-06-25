from lxml import html

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def add_placeholder(field):
    tree = html.fragment_fromstring(str(field))

    optional = '' if field.field.required else ' Optional.'
    help_text = f' {field.help_text}' if field.help_text else ''

    tree.attrib['placeholder'] = f'{field.label}.{optional}{help_text}'

    return mark_safe(html.tostring(tree).decode('utf-8'))


@register.filter
def add_classes(field, class_name):
    tree = html.fragment_fromstring(str(field))

    if 'class' not in tree.attrib:
        tree.attrib['class'] = ''

    existing_classes = tree.attrib['class']
    tree.attrib['class'] = f'{existing_classes} {class_name}'

    return mark_safe(html.tostring(tree).decode('utf-8'))
