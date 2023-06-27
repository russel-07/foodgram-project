from django import template

register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})


@register.filter(name='parse_tags')
def parse_tags(get):
    return get.getlist('get_tags')


@register.filter(name='set_tag_qs')
def set_tag_qs(request, tag):
    new_req = request.GET.copy()
    print('########################')
    print(new_req)
    tags = new_req.getlist('get_tags')
    print(tags)
    print(tag.id)

    if str(tag.id) in tags:
        tags.remove(str(tag.id))
    else:
        tags.append(str(tag.id))

    print(tags)
    
    new_req.setlist('get_tags', tags)
    print(new_req)
    print(new_req.urlencode())
    return new_req.urlencode()
