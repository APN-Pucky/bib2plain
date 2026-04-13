# SPDX-FileCopyrightText: 2026-present Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
from pathlib import Path

LOI_BIB = str(Path(__file__).parent / "loi.bib")


def test_eprint_filter_2602_16029():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "2602.16029"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Belloni, F., Chiesa, M., Oleari, C., Re, E.,'
        ' "Towards the inclusion of NLO EW corrections in the MiNLO method in Drell-Yan processes,"'
        ' (2026)'
        ' [2602.16029]'
    )
    assert result.stdout.strip() == expected