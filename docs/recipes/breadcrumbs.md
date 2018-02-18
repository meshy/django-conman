# Breadcrumbs

To add breadcrumbs to your page, add the following to your template:

```django
{% for ancestor in route.get_ancestors %}
    <a href="{{ ancestor.get_absolute_url }}">
        {{ ancestor }}
    </a>
{% endfor %}
<span>{{ route }}</span>
```

Styling the links is left as an exercise for the reader.
