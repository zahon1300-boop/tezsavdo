from django import template

register = template.Library()

@register.filter
def first_image(mahsulot):
    """Return first product image URL or fallback placeholder"""
    if hasattr(mahsulot, 'rasmlar') and mahsulot.rasmlar.exists():
        return mahsulot.rasmlar.first().rasm.url
    return '/static/images/placeholder.svg'

@register.filter
def variant_image(variant):
    """Return variant image URL or fallback placeholder"""
    if hasattr(variant, 'rasmlar') and variant.rasmlar.exists():
        return variant.rasmlar.first().rasm.url
    if hasattr(variant, 'image') and variant.image:
        return variant.image.url
    return '/static/images/placeholder.svg'

@register.filter
def product_image(mahsulot):
    """Alias for first_image"""
    return first_image(mahsulot)
