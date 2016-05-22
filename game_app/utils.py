import re


def remove_tags(text):
    if isinstance(text, str):
        p = re.compile(r'<.*?>')
        return p.sub('', text)
    else:
        return text


def get_paginator_list(page):
    all_imgs = FBImg.objects.filter(Q(active=True) & Q(is_temp=False))
    paginator = Paginator(all_imgs, settings.ITEMS_PER_PAGE)
    try:
        entries_list = paginator.page(page)
    except PageNotAnInteger:
        entries_list = paginator.page(1)
    except EmptyPage:
        raise Http404()
    return {
        'entries_list': entries_list,
        'num_pages': paginator.num_pages
        }