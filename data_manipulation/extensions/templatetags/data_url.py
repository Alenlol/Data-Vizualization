from django import template

register = template.Library()

# Experimenting with abstract url
@register.simple_tag()
def get_url(request):
    url = request.path.strip('/').split('/')
    print(url)
    return ['home'] + url[:-1]