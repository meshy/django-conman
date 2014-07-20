import importlib

from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from .utils import split_path


class NodeManager(TreeManager):
    def best_match_for_path(self, path):
        """
        Return the best match for a path. If the path as given is unavailable,
        continues to search by chopping path components off the end.

        Tries hard to avoid unnecessary database lookups by comparing all
        possible matching URL prefixes and choosing the longest match.

        Node.objects.best_match_for_path('/photos/album/2008/09') might return
        the Node with url '/photos/album/'.

        Adapted from feincms/module/page/models.py:71 in FeinCMS v1.9.5.
        """
        paths = split_path(path)

        extra = {'length': 'LENGTH(url)'}
        qs = self.filter(url__in=paths).extra(select=extra).order_by('-length')
        try:
            return qs[0]
        except IndexError:
            msg = 'No matching Node for URL. (Have you made a root Node?)'
            raise self.model.DoesNotExist(msg)


class Node(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    handler = models.CharField(max_length=255, choices=settings.NAV_NODE_HANDLERS)
    slug = models.SlugField(max_length=255, default='')
    # Cached location in tree. Reflects parent and slug on self and ancestors.
    url = models.TextField(db_index=True, editable=False)

    objects = NodeManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_originals()

    def get_handler_class(self):
        """Imports a class from the python path string in `self.handler`."""
        module_name, class_name = self.handler.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def handle(self, request, path):
        """Pass request and the remainder of the url through to the handler"""
        handler_class = self.get_handler_class()
        handler = handler_class(self)
        # Strip the node url from the rest of the path
        path = path[len(self.url) - 1:]
        # Deal with the request
        return handler.handle(request, path)

    def reset_originals(self):
        """
        Cache a copy of the loaded `url` value.

        This is so we can determine if it has been changed on save.
        """
        self._original_parent_id = self.parent_id
        self._original_slug = self.slug

    def save(self, *args, **kwargs):
        """
        Update the `url` attribute of this node and all descendants.

        Quite expensive when called with a node high up in the tree.

        Adapted from feincms/module/page/models.py:248 in FeinCMS v1.9.5.
        """
        has_parent = bool(self.parent_id)
        has_slug = bool(self.slug)

        # Must have both or neither
        if has_parent != has_slug:
            raise ValueError('Node can be a root, or have a slug, not both.')

        def make_url(parent_url, slug):
            return '{}{}/'.format(parent_url, slug)

        parent_changed = self._original_parent_id != self.parent_id
        slug_changed = self._original_slug != self.slug
        url_changed = parent_changed or slug_changed or not self.url

        if url_changed:
            self.url = make_url(self.parent.url, self.slug) if has_parent else '/'

        super().save(*args, **kwargs)
        self.reset_originals()

        # If the URL changed we need to update all descendants to
        # reflect the changes. Since this is a very expensive operation
        # on large sites we'll check whether our `url` actually changed
        # or if the updates weren't navigation related:
        if not url_changed:
            return

        nodes = self.get_descendants().order_by('lft')

        cached_urls = {self.id: self.url}
        for node in nodes:
            parent_path = cached_urls[node.parent_id]
            node.url = cached_urls[node.id] = make_url(parent_path, node.slug)

            # Skip this logic on save so we do not recurse.
            super(Node, node).save()
    save.alters_data = True
