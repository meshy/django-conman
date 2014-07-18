from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Node(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=255, default='')
    # Cached location in tree. Reflects parent and slug on self and ancestors.
    url = models.TextField(db_index=True, editable=False)


    def __init__(self, *args, **kwargs):
        """
        Cache a copy of the loaded `url` value.

        This is so we can determine if it has been changed on save.
        """
        super().__init__(*args, **kwargs)
        self._original_url = self.url

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

        if not has_parent:
            self.url = '/'
        else:
            self.url = '{}{}/'.format(self.parent.url, self.slug)

        super().save(*args, **kwargs)

        # If our cached URL changed we need to update all descendants to
        # reflect the changes. Since this is a very expensive operation
        # on large sites we'll check whether our `url` actually changed
        # or if the updates weren't navigation related:
        if self.url == self._original_url:
            return

        nodes = self.get_descendants().order_by('lft')

        cached_urls = {self.id: self.url}
        for node in nodes:
            node.url = '{}{}/'.format(cached_urls[node.parent_id], node.slug)
            cached_urls[node.id] = node.url

            # Skip this logic on save so we do not recurse.
            super(Node, node).save()
    save.alters_data = True
