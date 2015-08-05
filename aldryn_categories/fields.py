# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# import warnings

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.utils.safestring import mark_safe

# For South, where used.
try:
    from south.modelsinspector import add_introspection_rules
except:  # pragma: no cover
    add_introspection_rules = False


class CategoryModelChoiceField(ModelChoiceField):
    """Displays choices hierarchically as per their position in the tree."""
    def label_from_instance(self, obj):
        prefix = ''
        try:
            if obj.depth > 1:
                prefix = '&nbsp;&nbsp;' * (obj.depth - 1)

            return mark_safe("{prefix}{name}".format(
                prefix=prefix, name=obj.safe_translation_getter('name')
            ))
        except AttributeError:
            raise ImproperlyConfigured(
                "CategoryModelChoiceField should only be used for ForeignKey "
                "relations to the aldryn_categories.Category model.")


class CategoryForeignKey(ForeignKey):
    """
    Simply a normal ForeignKey field, but with a custom *default* form field
    which hierarchically displays the set of choices.
    """

    # This is necessary for Django 1.7.4+
    def get_internal_type(self):
        return 'ForeignKey'

    def formfield(self, form_class=CategoryModelChoiceField,
                  choices_form_class=None, **kwargs):
        kwargs["form_class"] = form_class
        kwargs["choices_form_class"] = choices_form_class
        return super(CategoryForeignKey, self).formfield(**kwargs)


class CategoryOneToOneField(OneToOneField):
    """
    Simply a normal OneToOneField field, but with a custom *default* form field
    which hierarchically displays the set of choices.
    """
    # This is necessary for Django 1.7.4+
    def get_internal_type(self):
        return 'ForeignKey'

    def formfield(self, form_class=CategoryModelChoiceField,
                  choices_form_class=None, **kwargs):
        kwargs["form_class"] = form_class
        kwargs["choices_form_class"] = choices_form_class
        return super(OneToOneField, self).formfield(**kwargs)


class CategoryMultipleChoiceField(ModelMultipleChoiceField):
    """Displays choices hierarchically as per their position in the tree."""
    def label_from_instance(self, obj):
        prefix = ''
        try:
            if obj.depth > 1:
                prefix = '&nbsp;&nbsp;' * (obj.depth - 1)

            return mark_safe("{prefix}{name}".format(
                prefix=prefix, name=obj.safe_translation_getter('name')
            ))
        except AttributeError:
            raise ImproperlyConfigured(
                "CategoryMultipleChoiceField should only be used for M2M "
                "relations to the aldryn_categories.Category model.")


class CategoryManyToManyField(ManyToManyField):
    """
    Simply a normal ManyToManyField, but with a custom *default* form field
    which hierarchically displays the set of choices.
    """

    # This is necessary for Django 1.7.4+
    def get_internal_type(self):
        return 'ManyToManyField'

    def formfield(self, form_class=CategoryMultipleChoiceField,
                  choices_form_class=None, **kwargs):
        kwargs["form_class"] = form_class
        kwargs["choices_form_class"] = choices_form_class
        return super(CategoryManyToManyField, self).formfield(**kwargs)


# This is necessary for South
if add_introspection_rules:
    add_introspection_rules([], [
        "^aldryn_categories\.fields\.CategoryForeignKey",
        "^aldryn_categories\.fields\.CategoryManyToManyField",
        "^aldryn_categories\.fields\.CategoryOneToOneField"
    ])
