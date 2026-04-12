# SPDX-FileCopyrightText: 2026-present Alexander Puck Neuwirth <alexander@neuwirth-informatik.de>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
from pathlib import Path

LOI_BIB = str(Path(__file__).parent / "loi.bib")


def test_eprint_filter_1908_06987():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "1908.06987"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Monni, P. F., Nason, P., Re, E., Wiesemann, M., Zanderighi, G.,'
        ' "MiNNLO$_{PS}$: a new method to match NNLO QCD to parton showers,"'
        ' JHEP 05 (2020) 143.'
        ' DOI: 10.1007/JHEP05(2020)143.'
        ' [1908.06987]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_1612_04333():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "1612.04333"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Campbell, J. M., Ellis, R. K., Williams, C.,'
        ' "Direct Photon Production at Next-to–Next-to-Leading Order,"'
        ' Phys. Rev. Lett. 118 (2017) 222001.'
        ' DOI: 10.1103/PhysRevLett.118.222001.'
        ' [1612.04333]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_1904_01044():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "1904.01044"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Chen, X., Gehrmann, T., Glover, N., Höfer, M., Huss, A.,'
        ' "Isolated photon and photon+jet production at NNLO QCD accuracy,"'
        ' JHEP 04 (2020) 166.'
        ' DOI: 10.1007/JHEP04(2020)166.'
        ' [1904.01044]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_1610_02275():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "1610.02275"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Jezo, T., Klasen, M., König, F.,'
        ' "Prompt photon production and photon-hadron jet correlations with POWHEG,"'
        ' JHEP 11 (2016) 033.'
        ' DOI: 10.1007/JHEP11(2016)033.'
        ' [1610.02275]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_2409_01424():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "2409.01424"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Ježo, T., Klasen, M., Neuwirth, A. P.,'
        ' "Prompt photon production with two jets in POWHEG,"'
        ' JHEP 02 (2025) 125.'
        ' DOI: 10.1007/JHEP02(2025)125.'
        ' [2409.01424]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_2402_00596():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "2402.00596"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Ebert, M., Rottoli, L., Wiesemann, M., Zanderighi, G., Zanoli, S.,'
        ' "Jettiness formulation of the MiNNLO$_{PS}$ method,"'
        ' JHEP 07 (2024) 085.'
        ' DOI: 10.1007/JHEP07(2024)085.'
        ' [2402.00596]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_2504_11357():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "2504.11357"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Alioli, S., Billis, G., Broggio, A., Stagnitto, G.,'
        ' "NNLO predictions with nonlocal subtractions and fiducial power corrections in GENEVA,"'
        ' JHEP 01 (2026) 065.'
        ' DOI: 10.1007/JHEP01(2026)065.'
        ' [2504.11357]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_2602_16029():
    DEFAULT_FORMAT = '{authors}, "{title}," [{eprint}]'
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "2602.16029", "--format", DEFAULT_FORMAT],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Belloni, F., Chiesa, M., Oleari, C., Re, E.,'
        ' "Towards the inclusion of NLO EW corrections in the MiNLO method in Drell-Yan processes,"'
        ' [2602.16029]'
    )
    assert result.stdout.strip() == expected


def test_eprint_filter_1912_05451():
    result = subprocess.run(
        [sys.executable, "-m", "bib2plain", LOI_BIB, "--eprint", "1912.05451"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = (
        'Bierlich, C. et al.,'
        ' "Robust Independent Validation of Experiment and Theory: Rivet version 3,"'
        ' SciPost Phys. 8 (2020) 026.'
        ' DOI: 10.21468/SciPostPhys.8.2.026.'
        ' [1912.05451]'
    )
    assert result.stdout.strip() == expected

