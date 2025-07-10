from django import template

register = template.Library()

@register.filter
def filter_user_rate(rates, user):
    """Kullanıcının mevcut puanını döndürür"""
    return rates.filter(user=user).first()
