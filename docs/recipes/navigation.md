# Navigation

Let's assume you have created a subclass of `Route` called `Page`, and you want
to use a list of these pages as the main navigation of your website.

You will need to add this list to the context to every page. The best way to do
this is with a [template context processor][context-processor]. Let's make one
of those:

```python
# example_module/context_processors.py
from example_module.models import Page

def nav_pages(request):
    return {'nav_pages': Page.objects.with_level(1)}


# settings.py
TEMPLATES['OPTIONS']['context_processors'].append(
    'example_module.context_processors.nav_pages'
)
```

The [`with_level(1)`](/reference/route.md#with_level) call we make here limits
the items in the queryset down to those on the first level of navigation. It
does not include the `Route` with `url='/'`.

!!! Note
    You also probably don't really want to use `.append` on your `TEMPLATES`
    setting like this. It would be better to add to the appropriate place where
    it's already defined. We've just done it like this for brevity.


Now that this has been exposed to the templates, we can add the pages into the
navigation in your base template:

```django
<nav>
    {% for page in nav_pages %}
        <a href="{{ page.get_absolute_url }}">
            {{ page }}
        </a>
    {% endfor %}
</nav>
```

[context-processor]: https://docs.djangoproject.com/en/stable/ref/templates/api/#writing-your-own-context-processors
