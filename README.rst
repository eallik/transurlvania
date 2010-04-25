Multilang URLs
==============

Introduction
------------

This application provides a collection of URL-related utilities for
multi-lingual projects.

Features
--------

* **Localizable URLs** - the same page can have a different url in a different
  language. (eg /products/ can be /produits/ in French)

* **Language-in-Path** - a replacement for Django's language cookie that
  makes URLs language-specific by storing the language code in the URL path.

* **Language-in-Domain** - a replacement for Django's language cookie that
  makes URLs language-specific by mapping each domain for the site onto a
  language.


Installation
------------

* Add ``multilang_urls`` to ``INSTALLED_APPS`` in your settings file

* Add the following middlewares to ``MIDDLEWARE_CLASSES`` in your settings file:

  * ``multilang.middleware.URLCacheResetMiddleware`` (must be before the
    ``SessionMiddleware``)

  * ``multilang.middleware.MultilangMiddleware``


Usage
-----

Localizing URLs
~~~~~~~~~~~~~~~

Use the ``turl`` function in ``urlresolvers`` in place of the usual ``url``
function when declaring URL patterns, combined with the ``ugettext_noop``
gettext function and the URLs you declare will become translatable using the
normal gettext translation system.

Any language-aware models that define ``get_absolute_url`` should decorate it with
``multilang_permalink``, from ``multilang.decorators`` so that the returned URLs
will be properly translated to the language of the object. The method should
return a list or tuple with this pattern::

    ('name_of_view_or_url', language_of_object, view_args, view_kwargs)

``language_of_object`` should be the language code of the object, so if the
model uses multilang's translatable DB solution, it would be
``self.language``.


Language Setting Via URL or Domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use LangInPathMiddleware and special root URLconf to embed the language code
in the URL path.

Use LangInDomainMiddleware and the ``MULTILANG_LANGUAGE_DOMAINS`` setting
to have language determination based on the domain name.*

This supersedes Django's usual language detection, so any language specific url
has a predictable language when visited. This also means that the individual,
language-specific resources of the site can all be identified by URL.

See ``multilang/tests/settings.py`` and ``multilang/tests/lang_prefixed_urls.py``
for an example.


* You will also need to edit ``urls_dev.py`` to replace::

    from urls import urlpatterns

  with::

    from lang_prefixed_urls import urlpatterns


* Use the ``multilang.utils.complete_url`` utility function to build full urls
  (ie. with the domain)


Translation Switching
~~~~~~~~~~~~~~~~~~~~~

Add MultilangMiddleware to the list of middleware classes and add the
"translate" context processor to the list of template context processors to
use the "``this_page_in_lang``" template tag. It will attempt to find the URL
that represents the page being displayed, but in the language requested. If it
is unable to determine an equivalent translation it will use the optional
fallback url argument.

Use the provided decorators to annotate any views whose translations should
be determined in a special way.

To make a model compatible with this system, it needs to implement a
``get_translation`` method. The provided translatable DB solution does this.


Language Based Blocking
~~~~~~~~~~~~~~~~~~~~~~~

The BlockLocaleMiddleware will block non-admins from accessing the site in any language
listed in the ``BLOCKED_LANGUAGES`` setting in the settings file.