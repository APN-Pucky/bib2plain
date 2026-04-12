# SPDX-FileCopyrightText: 2026-present Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>
#
# SPDX-License-Identifier: MIT

import argparse
from pybtex.database import parse_file

DEFAULT_FORMAT = '{authors}, "{title}," {journal} {volume} ({year}) {pages}. DOI: {doi}. [{eprint}]'


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


def main():
    parser = argparse.ArgumentParser(
        description="Convert .bib files to plain-text references."
    )
    parser.add_argument(
        "bibfiles",
        nargs="+",
        metavar="FILE",
        help=".bib file(s) to process",
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
        help="custom format string with placeholders: {authors}, {title}, "
             "{journal}, {volume}, {year}, {pages}, {doi}, {eprint} "
             "(default: %(default)r)",
    )
    parser.add_argument(
        "--no-other-to-et-al",
        action="store_true",
        default=False,
        help="disable replacing 'others' with 'et al.' in author lists",
    )
    args = parser.parse_args()

    for bibfile in args.bibfiles:
        bib = parse_file(bibfile)

        for key, entry in bib.entries.items():
            eprint = entry.fields.get("eprint")

            if args.eprint and args.eprint != eprint:
                continue

            authors = fmt_names(entry.persons.get("author", []))
            if not args.no_other_to_et_al:
                authors = authors.replace(", others, ", " et al.")
                authors = authors.replace(", others", " et al.")
            title = entry.fields.get("title").strip("{}")
            journal = entry.fields.get("journal")
            volume = entry.fields.get("volume")
            year = entry.fields.get("year")
            pages = entry.fields.get("pages")
            doi = entry.fields.get("doi")

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
                replacement = uni if args.char == "unicode" else asc
                authors = authors.replace(latex, replacement)
                title = title.replace(latex, replacement) if title else None

            fields = {
                "authors": authors,
                "title": title,
                "journal": journal,
                "volume": volume,
                "year": year,
                "pages": pages,
                "doi": doi,
                "eprint": eprint,
            }
            print(args.format.format_map(fields))


if __name__ == "__main__":
    main()