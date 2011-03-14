from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import get_language

from transurlvania.settings import LANGUAGE_DOMAINS


def complete_url(url, lang=None):
    """
    Takes a url (or path) and returns a full url including the appropriate
    domain name (based on the LANGUAGE_DOMAINS setting).
    """
    if not url.startswith('http://'):
        lang = lang or get_language()
        domain = LANGUAGE_DOMAINS.get(lang)
        if domain:
            url = u'http://%s%s' % (domain[0], url)
        else:
            raise ImproperlyConfigured(
                'Not domain specified for language code %s' % lang
            )
    return url


class MultiLangModel(object):
    """A mixin that provides the `get_translation` method used by the
    `this_page_in_lang` template tag.

    Classes inheriting from this mixin should provide an extended
    `get_absolute_url` method that takes an optional extra argument
    `lang`. When that argument is specified, it should return the URL
    in that language.

    Example:

        def get_absolute_url(self, lang=None):
            slug = self.get_translated('slug', lang)
            return reverse_for_language('blogpost_detail', lang,
                                        args=(slug, ))

    """

    def get_translation(self, lang):
        """Returns proxies for the `this_page_in_lang` template tag."""
        return TranslatedVersionProxy(self, lang)


class TranslatedVersionProxy(object):
    """A proxy class that emulates different language versions of a
    model object whose language versions are all actually stored in
    the same object.

    """

    def __init__(self, obj, lang):
        """Initializes this proxy with a wrapped object and a language."""
        self.obj, self.lang = obj, lang

    def get_absolute_url(self):
        """Calls the `get_absolute_url` method of the wrapped object
        with the language as the second argument.

        """
        return self.obj.get_absolute_url(lang=self.lang)
