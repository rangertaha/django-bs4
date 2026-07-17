import re
from html.parser import HTMLParser

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.forms.formsets import formset_factory
from django.template import engines
from django.test import TestCase

from bs4.exceptions import BootstrapError
from bs4.text import text_concat, text_value
from bs4.utils import add_css_class, render_tag

RADIO_CHOICES = (
    ("1", "Radio 1"),
    ("2", "Radio 2"),
)

MEDIA_CHOICES = (
    (
        "Audio",
        (
            ("vinyl", "Vinyl"),
            ("cd", "CD"),
        ),
    ),
    (
        "Video",
        (
            ("vhs", "VHS Tape"),
            ("dvd", "DVD"),
        ),
    ),
    ("unknown", "Unknown"),
)


class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """

    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"}),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text="<i>my_help_text</i>")
    sender = forms.EmailField(
        label="Sender © unicode", help_text='E.g., "me@example.com"'
    )
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False,
        help_text='cc stands for "carbon copy." You will get a copy in your mailbox.',
    )
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        help_text="Check as many as you like.",
    )
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        help_text="Check as many as you like.",
    )
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Check as many as you like.",
    )
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Check as many as you like.",
    )
    addon = forms.CharField(
        widget=forms.TextInput(
            attrs={"addon_before": "before", "addon_after": "after"}
        ),
    )

    required_css_class = "bootstrap3-req"

    def clean(self):
        cleaned_data = super().clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling."
        )
        return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ""


def render_template(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = engines["django"].from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_template_with_bootstrap(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    if not context:
        context = {}
    return render_template("{% load bs4 %}" + text, context)


def render_template_with_form(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    if not context:
        context = {}
    if "form" not in context:
        context["form"] = TestForm()
    return render_template_with_bootstrap(text, context)


def render_formset(formset=None, context=None):
    """
    Create a template that renders a formset
    """
    if not context:
        context = {}
    context["formset"] = formset
    return render_template_with_form("{% bootstrap_formset formset %}", context)


def render_form(form=None, context=None):
    """
    Create a template that renders a form
    """
    if not context:
        context = {}
    if form:
        context["form"] = form
    return render_template_with_form("{% bootstrap_form form %}", context)


def render_form_field(field, context=None):
    """
    Create a template that renders a field
    """
    form_field = f"form.{field}"
    return render_template_with_form(
        "{% bootstrap_field " + form_field + " %}", context
    )


def render_field(field, context=None):
    """
    Create a template that renders a field
    """
    if not context:
        context = {}
    context["field"] = field
    return render_template_with_form("{% bootstrap_field field %}", context)


def get_title_from_html(html):
    class GetTitleParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.title = None

        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr == "title":
                    self.title = value

    parser = GetTitleParser()
    parser.feed(html)

    return parser.title


class SettingsTest(TestCase):
    def test_settings(self):
        from bs4.bootstrap import BOOTSTRAP4

        self.assertTrue(BOOTSTRAP4)

    def test_bootstrap_javascript_tag(self):
        res = render_template_with_form("{% bootstrap_javascript %}")
        self.assertEqual(
            res.strip(),
            '<script src="//cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"></script>',
        )

    def test_bootstrap_css_tag(self):
        res = render_template_with_form("{% bootstrap_css %}")
        self.assertIn(
            res.strip(),
            [
                '<link rel="stylesheet" href="//cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">',
                '<link href="//cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" rel="stylesheet">',
            ],
        )

    def test_settings_filter(self):
        res = render_template_with_form('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), "bootstrap3-req")
        res = render_template_with_form(
            '{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}'
        )
        self.assertEqual(res.strip(), "head")

    def test_required_class(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-req", res)

    def test_error_class(self):
        form = TestForm({})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-err", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-bound", res)


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template_with_form("")
        self.assertEqual(res.strip(), "")

    def test_text_template(self):
        res = render_template_with_form("some text")
        self.assertEqual(res.strip(), "some text")

    def test_bootstrap_template(self):
        res = render_template(
            '{% extends "bs4/base.html" %}'
            + "{% block bs4_content %}"
            + "test_bs4_content"
            + "{% endblock %}"
        )
        self.assertIn("test_bs4_content", res)

    def test_javascript_without_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=0 %}")
        self.assertIn("bootstrap", res)
        self.assertNotIn("jquery", res)

    def test_javascript_with_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=1 %}")
        self.assertIn("bootstrap", res)
        self.assertIn("jquery", res)


class FormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset="illegal")


class FormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form="illegal")

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
                self.assertIn(f'name="{field.name}"', res)

    def test_field_addons(self):
        form = TestForm()
        res = render_form(form)
        self.assertIn(
            '<div class="input-group"><span class="input-group-addon">before</span><input',
            res,
        )
        self.assertIn('><span class="input-group-addon">after</span></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = render_template_with_form(
            '{% bootstrap_form form exclude="cc_myself" %}', {"form": form}
        )
        self.assertNotIn("cc_myself", res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template_with_form(
            '{% bootstrap_form form layout="horizontal" %}', {"form": form}
        )
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)
        res = render_template_with_form(
            '{% bootstrap_form form layout="horizontal" '
            + 'horizontal_label_class="hlabel" '
            + 'horizontal_field_class="hfield" %}',
            {"form": form},
        )
        self.assertIn("hlabel", res)
        self.assertIn("hfield", res)

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template_with_form(
            '{% buttons layout="horizontal" %}{% endbuttons %}', {"form": form}
        )
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)

    def test_error_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-err", res)

        res = render_template_with_form(
            '{% bootstrap_form form error_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form(
            '{% bootstrap_form form error_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap3-err", res)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-req", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap3-req", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-bound", res)

        res = render_template_with_form(
            '{% bootstrap_form form bound_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form(
            '{% bootstrap_form form bound_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap3-bound", res)


class FieldTest(TestCase):
    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_show_help(self):
        res = render_form_field("subject")
        self.assertIn("my_help_text", res)
        self.assertNotIn("<i>my_help_text</i>", res)
        res = render_template_with_form(
            "{% bootstrap_field form.subject show_help=0 %}"
        )
        self.assertNotIn("my_help_text", res)

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = render_form_field("sender")
        self.assertEqual(
            get_title_from_html(res), TestForm.base_fields["sender"].help_text
        )
        res = render_form_field("cc_myself")
        self.assertEqual(
            get_title_from_html(res), TestForm.base_fields["cc_myself"].help_text
        )

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_required_field(self):
        required_field = render_form_field("subject")
        self.assertIn("required", required_field)
        self.assertIn("bootstrap3-req", required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn("required", not_required_field)
        # Required field with required=0
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field " + form_field + " set_required=0 %}"
        )
        self.assertNotIn("required", rendered)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field "
            + form_field
            + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn("required", res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn("required", res)

    def test_input_group(self):
        res = render_template_with_form(
            '{% bootstrap_field form.subject addon_before="$"  addon_after=".00" %}'
        )
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-addon">$', res)
        self.assertIn('class="input-group-addon">.00', res)

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form(
                '{% bootstrap_field form.subject size="' + param + '" %}'
            )
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form(
                '{% bootstrap_field form.subject size="' + param + '" %}'
            )
            self.assertNotIn("input-lg", res)
            self.assertNotIn("input-sm", res)
            self.assertNotIn("input-md", res)

        _test_size("sm", "input-sm")
        _test_size("small", "input-sm")
        _test_size("lg", "input-lg")
        _test_size("large", "input-lg")
        _test_size_medium("md")
        _test_size_medium("medium")
        _test_size_medium("")

    def test_datetime(self):
        field = render_form_field("datetime")
        self.assertIn("vDateField", field)
        self.assertIn("vTimeField", field)


class ComponentsTest(TestCase):
    def test_icon(self):
        res = render_template_with_form('{% bootstrap_icon "star" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star"></span>')
        res = render_template_with_form(
            '{% bootstrap_icon "star" title="alpha centauri" %}'
        )
        self.assertIn(
            res.strip(),
            [
                '<span class="glyphicon glyphicon-star" title="alpha centauri"></span>',
                '<span title="alpha centauri" class="glyphicon glyphicon-star"></span>',
            ],
        )

    def test_alert(self):
        res = render_template_with_form(
            '{% bootstrap_alert "content" alert_type="danger" %}'
        )
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissable">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-hidden="true">'
            + "&times;</button>content</div>",
        )


class MessagesTest(TestCase):
    def test_messages(self):
        class FakeMessage:
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """

            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(r"\s+")
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(None, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [
            FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")
        ]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello http://example.com
    </div>        """
        self.assertEqual(
            re.sub(pattern, "", res).replace('rel="nofollow"', ""),
            re.sub(pattern, "", expected).replace('rel="nofollow"', ""),
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello there
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))


class UtilsTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")

    def test_text_value(self):
        self.assertEqual(text_value(""), "")
        self.assertEqual(text_value(" "), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator="="), "1=2")
        self.assertEqual(text_concat(None, 2, separator="="), "2")

    def test_render_tag(self):
        self.assertEqual(render_tag("span"), "<span></span>")
        self.assertEqual(render_tag("span", content="foo"), "<span>foo</span>")
        self.assertEqual(
            render_tag("span", attrs={"bar": 123}, content="foo"),
            '<span bar="123">foo</span>',
        )


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(res.strip(), '<button class="btn btn-lg">button</button>')
        res = render_template_with_form(
            "{% bootstrap_button 'button' size='lg' href='#' %}"
        )
        self.assertIn(
            res.strip(),
            '<a class="btn btn-lg" href="#">button</a><a href="#" '
            + 'class="btn btn-lg">button</a>',
        )


class ShowLabelTest(TestCase):
    def test_show_label(self):
        form = TestForm()
        res = render_template_with_form(
            "{% bootstrap_form form show_label=False %}", {"form": form}
        )
        self.assertIn("sr-only", res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template_with_form(
            "{% bootstrap_formset formset show_label=False %}",
            {"formset": test_formset},
        )
        self.assertIn("sr-only", res)

    def test_button_with_icon(self):
        res = render_template_with_form(
            "{% bootstrap_button 'test' icon='info-sign' %}"
        )
        self.assertEqual(
            res.strip(),
            '<button class="btn"><span class="glyphicon glyphicon-info-sign"></span> test</button>',
        )


class PaginationTest(TestCase):
    def _page(self, num_items=250, per_page=10, number=13):
        from django.core.paginator import Paginator

        return Paginator(range(num_items), per_page).page(number)

    def test_context_middle_page(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page())
        self.assertEqual(context["current_page"], 13)
        self.assertEqual(context["num_pages"], 25)
        self.assertEqual(context["first_page"], 8)
        self.assertEqual(context["last_page"], 18)
        self.assertEqual(context["pages_shown"], list(range(8, 19)))
        self.assertEqual(context["pages_back"], 3)
        self.assertEqual(context["pages_forward"], 23)

    def test_context_short_paginator(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(num_items=30, number=1))
        self.assertIsNone(context["pages_back"])
        self.assertIsNone(context["pages_forward"])
        self.assertEqual(context["pages_shown"], [1, 2, 3])

    def test_context_last_page(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(number=25))
        self.assertIsNone(context["pages_forward"])
        self.assertEqual(context["last_page"], 25)

    def test_context_url_strips_page_parameter(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(
            self._page(), url="/items?page=3&q=x", extra="lang=en"
        )
        url = context["bootstrap_pagination_url"]
        self.assertNotIn("page=3", url)
        self.assertIn("q=x", url)
        self.assertIn("lang=en", url)
        self.assertTrue(url.endswith("&"))

    def test_context_extra_without_url(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(), extra="lang=en")
        self.assertEqual(context["bootstrap_pagination_url"], "?lang=en&")

    def test_context_sizes(self):
        from bs4.templatetags.bs4 import get_pagination_context

        small = get_pagination_context(self._page(), size="small")
        self.assertIn("pagination-sm", small["pagination_css_classes"])
        large = get_pagination_context(self._page(), size="large")
        self.assertIn("pagination-lg", large["pagination_css_classes"])

    def test_context_invalid_pages_to_show(self):
        from bs4.templatetags.bs4 import get_pagination_context

        with self.assertRaises(ValueError):
            get_pagination_context(self._page(), pages_to_show=0)

    def test_pagination_tag(self):
        res = render_template_with_bootstrap(
            '{% bootstrap_pagination page url="/items?page=2" size="large" %}',
            {"page": self._page()},
        )
        self.assertIn("pagination-lg", res)
        self.assertIn("page=1", res)
        self.assertIn('class="active"', res)


class ButtonsTagTest(TestCase):
    def test_buttons_tag_submit_and_reset(self):
        res = render_template_with_form(
            "{% buttons submit='Save' reset='Undo' %}{% endbuttons %}"
        )
        self.assertIn('type="submit"', res)
        self.assertIn("btn-primary", res)
        self.assertIn('type="reset"', res)
        self.assertIn("Save", res)
        self.assertIn("Undo", res)

    def test_buttons_tag_asvar(self):
        res = render_template_with_form(
            "{% buttons submit='Save' as var %}{% endbuttons %}<pre>{{ var }}</pre>"
        )
        self.assertIn("<pre>", res)
        # The captured variable is autoescaped when displayed.
        self.assertIn("type=&quot;submit&quot;", res)

    def test_button_sizes(self):
        res = render_template_with_form("{% bootstrap_button 'test' size='xs' %}")
        self.assertIn("btn-xs", res)
        res = render_template_with_form("{% bootstrap_button 'test' size='large' %}")
        self.assertIn("btn-lg", res)
        res = render_template_with_form("{% bootstrap_button 'test' size='md' %}")
        self.assertNotIn("btn-md", res)

    def test_button_invalid_size(self):
        with self.assertRaises(BootstrapError):
            render_template_with_form("{% bootstrap_button 'test' size='xxl' %}")

    def test_button_invalid_type(self):
        with self.assertRaises(BootstrapError):
            render_template_with_form(
                "{% bootstrap_button 'test' button_type='bogus' %}"
            )

    def test_button_link(self):
        res = render_template_with_form(
            "{% bootstrap_button 'go' href='/there' button_type='link' %}"
        )
        self.assertIn("<a", res)
        self.assertIn('href="/there"', res)

    def test_button_name_value_title(self):
        res = render_template_with_form(
            "{% bootstrap_button 'test' name='n' value='v' title='t' %}"
        )
        self.assertIn('name="n"', res)
        self.assertIn('value="v"', res)
        self.assertIn('title="t"', res)


class ErrorsTagTest(TestCase):
    def test_form_errors_tag(self):
        form = TestForm({"subject": ""})
        res = render_template_with_bootstrap(
            "{% bootstrap_form_errors form %}", {"form": form}
        )
        self.assertIn("non field errors styling", res)

    def test_form_errors_types(self):
        from bs4.forms import render_form_errors

        form = TestForm({"subject": ""})
        all_errors = render_form_errors(form)
        field_errors = render_form_errors(form, type="fields")
        non_field_errors = render_form_errors(form, type="non_fields")
        self.assertIn("non field errors styling", all_errors)
        self.assertIn("This field is required.", field_errors)
        self.assertNotIn("non field errors styling", field_errors)
        self.assertIn("non field errors styling", non_field_errors)
        self.assertNotIn("This field is required.", non_field_errors)

    def test_formset_errors_tag(self):
        TestFormSet = formset_factory(TestForm, min_num=1, validate_min=True)
        formset = TestFormSet({"form-TOTAL_FORMS": "0", "form-INITIAL_FORMS": "0"})
        res = render_template_with_bootstrap(
            "{% bootstrap_formset_errors formset %}", {"formset": formset}
        )
        self.assertIn("at least 1 form", res)


class MessageClassesTest(TestCase):
    def test_object_without_message_attributes(self):
        from bs4.templatetags.bs4 import bootstrap_message_classes

        self.assertEqual(bootstrap_message_classes(object()), "")

    def test_unknown_level_defaults_to_danger(self):
        from bs4.templatetags.bs4 import bootstrap_message_classes

        class FakeMessage:
            extra_tags = "custom"
            level = 99999

        classes = bootstrap_message_classes(FakeMessage())
        self.assertIn("custom", classes)
        self.assertIn("alert-danger", classes)


class UtilsExtraTest(TestCase):
    def test_handle_var(self):
        from bs4.utils import handle_var

        self.assertEqual(handle_var('"quoted"', {}), "quoted")
        self.assertEqual(handle_var("name", {"name": "resolved"}), "resolved")
        self.assertEqual(handle_var("missing", {}), "missing")

    def test_handle_var_variable_instance(self):
        from django.template import Variable

        from bs4.utils import handle_var

        self.assertEqual(handle_var(Variable("name"), {"name": 42}), 42)

    def test_render_link_tag(self):
        from bs4.utils import render_link_tag

        link = render_link_tag("//example.com/x.css", media="print")
        self.assertIn('href="//example.com/x.css"', link)
        self.assertIn('rel="stylesheet"', link)
        self.assertIn('media="print"', link)
        self.assertFalse(link.endswith("</link>"))

    def test_render_tag_without_close(self):
        from bs4.utils import render_tag

        self.assertEqual(render_tag("br", close=False), "<br>")


class AlertTest(TestCase):
    def test_alert_default_type(self):
        from bs4.components import render_alert

        res = render_alert("Watch out", alert_type=None, dismissable=False)
        self.assertIn("alert-info", res)
        self.assertNotIn("close", res)

    def test_icon_with_title(self):
        from bs4.components import render_icon

        res = render_icon("star", title="Starred")
        self.assertIn("glyphicon-star", res)
        self.assertIn('title="Starred"', res)


class RendererExtraTest(TestCase):
    def test_field_size_classes(self):
        res = render_form_field("subject", {"form": TestForm()})
        self.assertNotIn("input-sm", res)
        res = render_template_with_form("{% bootstrap_field form.subject size='sm' %}")
        self.assertIn("input-sm", res)
        res = render_template_with_form(
            "{% bootstrap_field form.subject size='large' %}"
        )
        self.assertIn("input-lg", res)

    def test_invalid_size_raises(self):
        with self.assertRaises(BootstrapError):
            render_template_with_form("{% bootstrap_field form.subject size='huge' %}")

    def test_set_disabled(self):
        res = render_template_with_form(
            "{% bootstrap_field form.subject set_disabled=True %}"
        )
        self.assertIn('disabled="disabled"', res)

    def test_inline_layout_with_errors(self):
        form = TestForm({"subject": ""})
        res = render_template_with_bootstrap(
            "{% bootstrap_form form layout='inline' %}", {"form": form}
        )
        self.assertIn("sr-only", res)
        self.assertIn("This field is required.", res)

    def test_select_date_widget(self):
        class DateForm(forms.Form):
            when = forms.DateField(widget=forms.SelectDateWidget)

        res = render_template_with_bootstrap(
            "{% bootstrap_form form %}", {"form": DateForm()}
        )
        self.assertIn("bootstrap3-multi-input", res)
        self.assertIn("col-xs-4", res)

    def test_clearable_file_input(self):
        class FileForm(forms.Form):
            upload = forms.FileField(required=False)

        res = render_template_with_bootstrap(
            "{% bootstrap_form form %}", {"form": FileForm()}
        )
        self.assertIn("col-xs-12", res)


class LabelTest(TestCase):
    def test_label_tag(self):
        res = render_template_with_bootstrap(
            '{% bootstrap_label "Email" label_for="id_email" label_class="control-label" label_title="Email address" %}'
        )
        self.assertEqual(
            res.strip(),
            '<label class="control-label" for="id_email" title="Email address">Email</label>',
        )


class PaginationEdgeTest(TestCase):
    def _page(self, num_items, number):
        from django.core.paginator import Paginator

        return Paginator(range(num_items), 10).page(number)

    def test_pages_back_clamped_to_one(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(250, 8))
        self.assertEqual(context["pages_back"], 1)

    def test_pages_forward_clamped_to_num_pages(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(200, 13))
        self.assertEqual(context["pages_forward"], 20)

    def test_url_without_query_string(self):
        from bs4.templatetags.bs4 import get_pagination_context

        context = get_pagination_context(self._page(250, 13), url="/items")
        self.assertEqual(context["bootstrap_pagination_url"], "/items?")


class RequiredWidgetTest(TestCase):
    def test_required_file_input_has_no_required_attribute(self):
        class FileForm(forms.Form):
            upload = forms.FileField(required=True)

        res = render_template_with_bootstrap(
            "{% bootstrap_form form %}", {"form": FileForm()}
        )
        self.assertNotIn('required="required"', res)

    def test_readonly_password_hash_is_static_control(self):
        from django.contrib.auth.forms import ReadOnlyPasswordHashField

        class HashForm(forms.Form):
            password = ReadOnlyPasswordHashField()

        res = render_template_with_bootstrap(
            "{% bootstrap_form form %}", {"form": HashForm()}
        )
        self.assertIn("form-control-static", res)

    def test_set_placeholder_disabled(self):
        from bs4 import bootstrap

        old = bootstrap.BOOTSTRAP4["set_placeholder"]
        bootstrap.BOOTSTRAP4["set_placeholder"] = False
        try:
            res = render_template_with_bootstrap(
                "{% bootstrap_form form %}", {"form": TestFormWithoutRequiredClass()}
            )
        finally:
            bootstrap.BOOTSTRAP4["set_placeholder"] = old
        self.assertNotIn('placeholder="Sender', res)


class ButtonSizeSmallTest(TestCase):
    def test_button_size_small(self):
        res = render_template_with_form("{% bootstrap_button 'test' size='sm' %}")
        self.assertIn("btn-sm", res)


class UtilsCssClassTest(TestCase):
    def test_remove_css_class(self):
        from bs4.utils import remove_css_class

        self.assertEqual(remove_css_class("btn btn-primary", "btn-primary"), "btn")
        self.assertEqual(remove_css_class("btn", "missing"), "btn")


class ParseTokenTest(TestCase):
    def test_positional_arguments(self):
        res = render_template_with_form("{% buttons 'extra' %}x{% endbuttons %}")
        self.assertIn("form-group", res)

    def test_malformed_arguments(self):
        from django.template.base import TemplateSyntaxError

        from bs4.utils import parse_token_contents

        class FakeToken:
            def split_contents(self):
                return ["buttons", ""]

        with self.assertRaises(TemplateSyntaxError):
            parse_token_contents(None, FakeToken())


class SetRequiredSettingTest(TestCase):
    def test_set_required_disabled_globally(self):
        from bs4 import bootstrap
        from bs4.forms import is_widget_required_attribute

        widget = forms.TextInput()
        widget.is_required = True
        old = bootstrap.BOOTSTRAP4["set_required"]
        bootstrap.BOOTSTRAP4["set_required"] = False
        try:
            self.assertFalse(is_widget_required_attribute(widget))
        finally:
            bootstrap.BOOTSTRAP4["set_required"] = old
        self.assertTrue(is_widget_required_attribute(widget))
