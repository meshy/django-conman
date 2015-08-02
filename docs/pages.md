# ConMan Pages

ConMan Pages allow adding rich content to your site using [Sir Trevor](https://madebymany.github.io/sir-trevor-js/).

## Configuration

* Add `conman.pages` to `INSTALLED_APPS`.
* Add `sirtrevor` to `INSTALLED_APPS`.
* Add Django SirTrevor urls to `urls.py` (above ConMan's urls):

```python
urlpatterns = [
    url(r'^sirtrevor/', include('sirtrevor.urls')),
    url(r'', include('conman.routes.urls')),
]
```

* Run database migrations: `python manage.py migrate`
