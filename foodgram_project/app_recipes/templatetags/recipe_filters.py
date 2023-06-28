from django import template

register = template.Library()


@register.filter 
def addclass(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def get_tags(get):
    return get.getlist('tag')


@register.filter
def set_tag(request, tag):
    new_req = request.GET.copy()
    tags = new_req.getlist('tag')
    if tag.name in tags:
        tags.remove(tag.name)
    else:
        tags.append(tag.name)
    new_req.setlist('tag', tags)

    return new_req.urlencode()


@register.filter
def add_tags(tags):
    return '&' + '&'.join([f'tag={tag}' for tag in tags])
