from django import template

register = template.Library()


@register.simple_tag
def mediapath(image_path) -> str:
    return f'/media/{image_path}' if image_path else '#'

