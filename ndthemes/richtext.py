"""Strip theme-breaking inline styles out of rich text.

NDT 4.0 flips ``data-theme`` on ``<body>`` between ``light`` and ``dark`` and
expects body copy to inherit ``color`` and the ``--font-default`` / ``--font-heading``
tokens. Pasting from Google Docs or Word brings inline runs such as
``style="font-size:10pt;font-family:Arial,sans-serif;color:#000000"`` along, and
inline styles outrank anything the theme (or ``@layer site``) can set — so the
text stays black on the dark canvas and renders in Arial rather than ND type.

djangocms-text re-allows the ``style`` attribute that nh3 would otherwise drop
(see ``djangocms_text.html.cms_additional_attributes``), so these declarations
have to be filtered here instead. Only the properties that fight the theme are
removed; declarations the editor legitimately produces, such as ``text-align``,
survive.
"""

import re

#: CSS properties removed from inline ``style`` attributes. The ``background``
#: and ``font`` shorthands are included because they can carry a colour and a
#: family/size respectively.
BLOCKED_DECLARATIONS = frozenset(
    {
        "color",
        "background",
        "background-color",
        "font",
        "font-family",
        "font-size",
    }
)

#: Tiptap marks that exist only to carry presentation. Once their declarations
#: are gone they render an empty ``<span>``, so they are dropped from the document.
PRESENTATION_ONLY_MARKS = frozenset({"textcolor", "highlight"})

#: Editor toolbar buttons whose only job is to hard-code a colour. The default
#: toolbars ship no font family or size pickers, so fonts only arrive via paste.
COLOR_TOOLBAR_ITEMS = frozenset({"TextColor", "Highlight", "BGColor"})

_STYLE_ATTR_RE = re.compile(r"""\sstyle\s*=\s*(?P<quote>["'])(?P<value>.*?)(?P=quote)""", re.DOTALL)


def scrub_declarations(style_value):
    """Return ``style_value`` without any :data:`BLOCKED_DECLARATIONS`."""
    kept = []
    for declaration in style_value.split(";"):
        if not declaration.strip():
            continue
        prop, sep, _value = declaration.partition(":")
        if sep and prop.strip().lower() in BLOCKED_DECLARATIONS:
            continue
        kept.append(declaration.strip())
    return ";".join(kept)


def scrub_inline_styles(html):
    """Return ``html`` with blocked declarations removed from ``style`` attributes.

    Attributes left empty are dropped entirely so the markup does not accumulate
    ``style=""`` noise. Idempotent, so it is safe to run on every save.
    """
    if not html or "style" not in html:
        return html

    def replace(match):
        kept = scrub_declarations(match.group("value"))
        if not kept:
            return ""
        quote = match.group("quote")
        return f" style={quote}{kept}{quote}"

    return _STYLE_ATTR_RE.sub(replace, html)


def _is_spent_mark(mark):
    """True when a presentation-only mark no longer carries anything worth keeping."""
    if not isinstance(mark, dict) or mark.get("type") not in PRESENTATION_ONLY_MARKS:
        return False
    attrs = mark.get("attrs") or {}
    return not any(attrs.get(key) for key in ("style", "class"))


def scrub_document(document):
    """Return a Tiptap document with blocked declarations removed.

    The editor keeps its own JSON copy of the content and prefers it over
    ``body`` when reopening a plugin, so the marks have to be cleaned there too
    or the next save would reintroduce the styling.
    """
    if isinstance(document, list):
        return [scrub_document(item) for item in document]
    if not isinstance(document, dict):
        return document

    scrubbed = {}
    for key, value in document.items():
        if key == "style" and isinstance(value, str):
            scrubbed[key] = scrub_declarations(value) or None
        elif key == "marks" and isinstance(value, list):
            marks = [scrub_document(mark) for mark in value]
            scrubbed[key] = [mark for mark in marks if not _is_spent_mark(mark)]
        else:
            scrubbed[key] = scrub_document(value)
    return scrubbed


def _without_color_tools(toolbar):
    """Drop colour buttons from a toolbar, plus any group left with only dividers."""
    groups = []
    for group in toolbar:
        kept = [item for item in group if item not in COLOR_TOOLBAR_ITEMS]
        while kept and kept[0] == "-":
            kept.pop(0)
        while kept and kept[-1] == "-":
            kept.pop()
        if kept:
            groups.append(kept)
    return groups


def hide_editor_color_tools():
    """Remove the editor's colour pickers, since saved colours are scrubbed anyway.

    Leaving the buttons in place would let editors pick a colour that silently
    disappears on save. The toolbars are derived from djangocms-text's own
    defaults rather than restated here, so upstream additions still appear.
    """
    from djangocms_text import settings as text_settings
    from djangocms_text.editors import DEFAULT_TOOLBAR_CMS, DEFAULT_TOOLBAR_HTMLField

    text_settings.TEXT_EDITOR_SETTINGS.setdefault("toolbar_CMS", _without_color_tools(DEFAULT_TOOLBAR_CMS))
    text_settings.TEXT_EDITOR_SETTINGS.setdefault(
        "toolbar_HTMLField", _without_color_tools(DEFAULT_TOOLBAR_HTMLField)
    )
