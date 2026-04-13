# SPDX-FileCopyrightText: 2026-present Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>
#
# SPDX-License-Identifier: MIT

import argparse
import string
import sys
from pybtex.database import parse_file, parse_string

DEFAULT_FORMAT = '{formated_authors}, "{title}," {journal} {volume} ({year}) {pages}. DOI: {doi}. [{eprint}]'


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
        help="custom format string with placeholders: {author}, {title}, "
             "{journal}, {volume}, {year}, {pages}, {doi}, {eprint}, {formated_authors}"
             "(default: %(default)r)",
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
            fields["formated_authors"] = clean_field(authors, args.char)

            # Raise a error here if key that is None is requested in format string
            used_keys = {fname for _, fname, _, _ in string.Formatter().parse(args.format) if fname}
            for k in used_keys:
                v = entry.fields.get(k)
                if not k in fields.keys():
                    if v is None:
                        raise ValueError(f"Entry '{key}' is missing required field '{k}'")
                    else:
                        fields[k] = clean_field(v.strip("{}"), args.char)


            print(args.format.format_map(fields))


if __name__ == "__main__":
    main()
