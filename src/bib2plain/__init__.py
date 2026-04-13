# SPDX-FileCopyrightText: 2026-present Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>
#
# SPDX-License-Identifier: MIT

import argparse
import re
import sys
from pybtex.database import parse_file, parse_string

DEFAULT_FORMAT = (
    '{formated_authors}, "{title},"'
    '{?journal: {journal}}'
    '{?volume: {volume}}'
    '{?year: ({year})}'
    '{?pages: {pages}.}'
    '{?doi: DOI: {doi}.}'
    '{?eprint: [{eprint}]}'
)

def fmt_names(persons):
    out = []
    for p in persons:
        last = " ".join(p.last_names)
        initials = []
        for n in p.first_names + p.middle_names:
            if n:
                initials.append(n[0] + ".")
        out.append(f"{last}, {' '.join(initials)}")
    return ", ".join(out)


class TemplateError(ValueError):
    pass


def render_template(template, data):
    return _render(template, data)


def _render(template, data):
    out = []
    i = 0
    n = len(template)

    while i < n:
        if template[i] != "{":
            out.append(template[i])
            i += 1
            continue

        if i + 1 < n and template[i + 1] == "?":
            field, inner, new_i = _parse_optional_block(template, i)
            value = data.get(field)
            if value:
                out.append(_render(inner, data))
            i = new_i
            continue

        end = template.find("}", i + 1)
        if end == -1:
            raise TemplateError(f"Unmatched '{{' at position {i}")

        token = template[i + 1 : end]
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            raise TemplateError(f"Invalid placeholder '{{{token}}}' at position {i}")

        if token not in data:
            raise TemplateError(f"Missing required field: {token}")

        out.append(str(data[token]))
        i = end + 1

    return "".join(out)


def _parse_optional_block(template, start):
    assert template.startswith("{?", start)

    j = start + 2
    field_start = j
    while j < len(template) and template[j] != ":":
        j += 1

    if j >= len(template):
        raise TemplateError(f"Unterminated optional block starting at position {start}")

    field = template[field_start:j].strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", field):
        raise TemplateError(f"Invalid optional field name '{field}' at position {start}")

    inner_start = j + 1
    depth = 1
    k = inner_start

    while k < len(template):
        if template[k] == "{":
            depth += 1
        elif template[k] == "}":
            depth -= 1
            if depth == 0:
                inner = template[inner_start:k]
                return field, inner, k + 1
        k += 1

    raise TemplateError(f"Unterminated optional block starting at position {start}")


def clean_field(value, char):
    # Substitute special latex characters in authors
    # (latex, unicode, ascii)
    latex_char_table = [
                (r'{\"o}', 'ö', 'oe'),
                (r'{\"a}', 'ä', 'ae'),
                (r'{\"u}', 'ü', 'ue'),
                (r'{\v{z}}', 'ž', 'z'),
                (r'{\textendash}', '–', '-'),
            ]
    for latex, uni, asc in latex_char_table:
        replacement = uni if char == "unicode" else asc
        value = value.replace(latex, replacement)
    return value

def main():
    parser = argparse.ArgumentParser(
        description="Convert .bib files to plain-text references."
    )
    parser.add_argument(
        "bibfiles",
        nargs="*",
        metavar="FILE",
        help=".bib file(s) to process (reads stdin if omitted)",
    )
    # ascii vs unicode
    parser.add_argument(
        "--char",
        choices=["unicode", "ascii"],
        default="unicode",
        help="character set for special LaTeX characters (default: unicode)",
    )
    parser.add_argument(
        "--eprint",
        metavar="ID",
        help="only show entries whose eprint field matches ID",
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        help="custom format string with placeholders: {field} (required), "
             "{?field: ...} (optional, rendered only if field is present). "
             "Available fields: formated_authors, title, journal, volume, year, "
             "pages, doi, eprint, etc. (default: %(default)r)",
    )
    parser.add_argument(
        "--no-other-to-et-al",
        action="store_true",
        default=False,
        help="disable replacing 'others' with 'et al.' in author lists",
    )
    args = parser.parse_args()

    if args.bibfiles:
        bibs = [parse_file(f) for f in args.bibfiles]
    else:
        bibs = [parse_string(sys.stdin.read(), bib_format="bibtex")]

    for bib in bibs:

        for key, entry in bib.entries.items():
            eprint = entry.fields.get("eprint")

            if args.eprint and args.eprint != eprint:
                continue

            fields = {}

            authors = fmt_names(entry.persons.get("author", []))
            if not args.no_other_to_et_al:
                authors = authors.replace(", others, ", " et al.")
                authors = authors.replace(", others", " et al.")
            if authors:
                fields["formated_authors"] = clean_field(authors, args.char)

            for k, v in entry.fields.items():
                fields[k] = clean_field(v.strip("{}"), args.char)

            try:
                print(render_template(args.format, fields))
            except TemplateError as e:
                raise ValueError(f"Entry '{key}': {e}") from e


if __name__ == "__main__":
    main()
