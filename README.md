# bib2plain

[![PyPI - Version](https://img.shields.io/pypi/v/bib2plain.svg)](https://pypi.org/project/bib2plain)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bib2plain.svg)](https://pypi.org/project/bib2plain)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)
- [Examples](#examples)

## Installation

```console
pip install bib2plain
```

## License

`bib2plain` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Examples 

```console
$ inspirehep2bib Chen:2019zmr | bib2plain
Chen, X., Gehrmann, T., Glover, N., Höfer, M., Huss, A., "Isolated photon and photon+jet production at NNLO QCD accuracy," JHEP 04 (2020) 166. DOI: 10.1007/JHEP04(2020)166. [1904.01044]
```

```console
$ inspirehep2bib 1904.01044 | bib2plain
Chen, X., Gehrmann, T., Glover, N., Höfer, M., Huss, A., "Isolated photon and photon+jet production at NNLO QCD accuracy," JHEP 04 (2020) 166. DOI: 10.1007/JHEP04(2020)166. [1904.01044]
```

```console
$ arxiv2bib 1101.0001 1102.0002 1103.0003 | bib2plain
Kajisawa, M., Ichikawa, T., Yoshikawa, T., Yamada, T., Onodera, M., Akiyama, M., Tanaka, I., "MOIRCS Deep Survey. X. Evolution of Quiescent Galaxies as a Function of Stellar Mass at 0.5<z<2.5," None None (2010) None. DOI: 10.1093/pasj/63.sp2.S403. [1101.0001v2]
Ludlow, A. D., Navarro, J. F., Boylan-Kolchin, M., Springel, V., Jenkins, A., Frenk, C. S., White, S. D. M., "The Density and Pseudo-Phase-Space Density Profiles of CDM halos," None None (2011) None. DOI: 10.1111/j.1365-2966.2011.19008.x. [1102.0002v1]
Khoury, J., Lehners, J., Ovrut, B. A., "Supersymmetric Galileons," None None (2011) None. DOI: 10.1103/PhysRevD.84.043521. [1103.0003v2]
```
