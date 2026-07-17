from importlib import import_module

from django.conf import settings

# Default settings
BOOTSTRAP4_DEFAULTS = {
    "jquery_url": "//code.jquery.com/jquery.min.js",
    "base_url": "//cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/",
    "css_url": None,
    "theme_url": None,
    "javascript_url": None,
    "javascript_in_head": False,
    "include_jquery": False,
    "horizontal_label_class": "col-md-3",
    "horizontal_field_class": "col-md-9",
    "set_required": True,
    "set_disabled": False,
    "set_placeholder": True,
    "required_css_class": "",
    "error_css_class": "has-error",
    "success_css_class": "has-success",
    "formset_renderers": {
        "default": "bs4.renderers.FormsetRenderer",
    },
    "form_renderers": {
        "default": "bs4.renderers.FormRenderer",
    },
    "field_renderers": {
        "default": "bs4.renderers.FieldRenderer",
        "inline": "bs4.renderers.InlineFieldRenderer",
    },
}

# Start with a copy of default settings
BOOTSTRAP4 = BOOTSTRAP4_DEFAULTS.copy()

# Override with user settings from settings.py
BOOTSTRAP4.update(getattr(settings, "BOOTSTRAP4", {}))


def get_bootstrap_setting(setting, default=None):
    """
    Read a setting
    """
    return BOOTSTRAP4.get(setting, default)


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bootstrap_setting("base_url") + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting("jquery_url")


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting("javascript_url") or bootstrap_url(
        "js/bootstrap.min.js"
    )


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return get_bootstrap_setting("css_url") or bootstrap_url("css/bootstrap.min.css")


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting("theme_url")


def get_renderer(renderers, **kwargs):
    layout = kwargs.get("layout", "")
    path = renderers.get(layout, renderers["default"])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting("formset_renderers")
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting("form_renderers")
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting("field_renderers")
    return get_renderer(renderers, **kwargs)
