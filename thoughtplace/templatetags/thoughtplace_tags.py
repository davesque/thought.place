from hashlib import md5

from lxml import html
from lxml.html.clean import Cleaner

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def add_placeholder(field):
    tree = html.fragment_fromstring(str(field))

    tree.attrib['placeholder'] = f'{field.help_text}'

    return mark_safe(html.tostring(tree).decode('utf-8'))


@register.filter
def add_classes(field, class_name):
    tree = html.fragment_fromstring(str(field))

    if 'class' not in tree.attrib:
        tree.attrib['class'] = ''

    existing_classes = tree.attrib['class']
    tree.attrib['class'] = f'{existing_classes} {class_name}'

    return mark_safe(html.tostring(tree).decode('utf-8'))


@register.filter
def remove_tags(html_str, tags):
    content_hash = md5(html_str.encode('utf-8')).hexdigest()
    wrapper_class = f'remove-tags-wrapper-{content_hash}'

    html_str = f'<div class="{wrapper_class}">{html_str}</div>'
    tree = html.document_fromstring(html_str)

    cleaner = Cleaner()
    cleaner.kill_tags = tags.split()

    tree = cleaner.clean_html(tree)
    tree = tree.find_class(wrapper_class)[0]

    return mark_safe(html.tostring(tree).decode('utf-8'))
