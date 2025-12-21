Changes
=======

Unreleased
----------

Version 0.6.4
-------------

Released 2025-12-21

- Fix cache-poisoning error. `#345 <https://github.com/dajiaji/flask-paseto-extended/pull/345>`__
- Fix error on dependabot.yml. `#340 <https://github.com/dajiaji/flask-paseto-extended/pull/340>`__
- Introduce gh-action-pypi-publish. `#339 <https://github.com/dajiaji/flask-paseto-extended/pull/339>`__
- Refine dependabot to introduce cooldown. `#338 <https://github.com/dajiaji/flask-paseto-extended/pull/338>`__
- Refine SBOM config. `#337 <https://github.com/dajiaji/flask-paseto-extended/pull/337>`__
- Disable VEX feature. `#336 <https://github.com/dajiaji/flask-paseto-extended/pull/336>`__
- Bump checkout to v6. `#335 <https://github.com/dajiaji/flask-paseto-extended/pull/335>`__
- Fix template injection. `#334 <https://github.com/dajiaji/flask-paseto-extended/pull/334>`__
- Activate actionlint. `#333 <https://github.com/dajiaji/flask-paseto-extended/pull/333>`__
- Update workflow actions. `#332 <https://github.com/dajiaji/flask-paseto-extended/pull/332>`__
- Add VEX and SBOM support. `#331 <https://github.com/dajiaji/flask-paseto-extended/pull/331>`__
- Fix unpinned action. `#330 <https://github.com/dajiaji/flask-paseto-extended/pull/330>`__
- Introduce trivy. `#329 <https://github.com/dajiaji/flask-paseto-extended/pull/329>`__
- Refine pip-audit args. `#328 <https://github.com/dajiaji/flask-paseto-extended/pull/328>`__
- Introduce task. `#327 <https://github.com/dajiaji/flask-paseto-extended/pull/327>`__
- Fix artipacked. `#326 <https://github.com/dajiaji/flask-paseto-extended/pull/326>`__
- Fix excessive permissions. `#325 <https://github.com/dajiaji/flask-paseto-extended/pull/325>`__
- Drop support for Python 3.9. `#324 <https://github.com/dajiaji/flask-paseto-extended/pull/324>`__
- Use persist credentials. `#323 <https://github.com/dajiaji/flask-paseto-extended/pull/323>`__
- Apply pinact. `#322 <https://github.com/dajiaji/flask-paseto-extended/pull/322>`__
- Introduce pip-audit. `#321 <https://github.com/dajiaji/flask-paseto-extended/pull/321>`__
- Use dependency groups. `#320 <https://github.com/dajiaji/flask-paseto-extended/pull/320>`__
- Introduce workflow security. `#319 <https://github.com/dajiaji/flask-paseto-extended/pull/319>`__
- Update pre-commit CI config. `#311 <https://github.com/dajiaji/flask-paseto-extended/pull/311>`__, `#314 <https://github.com/dajiaji/flask-paseto-extended/pull/314>`__, `#316 <https://github.com/dajiaji/flask-paseto-extended/pull/316>`__
- Update dependencies.
    - Bump Werkzeug to 3.1.4. `#312 <https://github.com/dajiaji/flask-paseto-extended/pull/312>`__
- Update dev dependencies.
    - Bump sphinx to 8.1.3. `#341 <https://github.com/dajiaji/flask-paseto-extended/pull/341>`__
    - Bump mypy to 1.19.1. `#317 <https://github.com/dajiaji/flask-paseto-extended/pull/317>`__
    - Bump ruff to 0.14.10. `#313 <https://github.com/dajiaji/flask-paseto-extended/pull/313>`__, `#318 <https://github.com/dajiaji/flask-paseto-extended/pull/318>`__
- Update CI dependencies.
    - Bump codecov/codecov-action to 5.5.2. `#344 <https://github.com/dajiaji/flask-paseto-extended/pull/344>`__
    - Bump actions/upload-artifact to 6.0.0. `#343 <https://github.com/dajiaji/flask-paseto-extended/pull/343>`__
    - Bump astral-sh/setup-uv to 7.1.6. `#342 <https://github.com/dajiaji/flask-paseto-extended/pull/342>`__

Version 0.6.3
-------------

Released 2025-11-29

- Add support for Python 3.9. `#309 <https://github.com/dajiaji/flask-paseto-extended/pull/309>`__
- Remove --token from uv publish for dry-run. `#308 <https://github.com/dajiaji/flask-paseto-extended/pull/308>`__
- Integrate mypy into CI. `#303 <https://github.com/dajiaji/flask-paseto-extended/pull/303>`__
- Update dev dependencies.
    - Bump mypy to 1.19.0. `#307 <https://github.com/dajiaji/flask-paseto-extended/pull/307>`__
    - Bump ruff to 0.14.7. `#306 <https://github.com/dajiaji/flask-paseto-extended/pull/306>`__
    - Bump docutils to 0.22.3. `#305 <https://github.com/dajiaji/flask-paseto-extended/pull/305>`__

Version 0.6.2
-------------

Released 2025-11-24

- Introduce ruff. `#301 <https://github.com/dajiaji/flask-paseto-extended/pull/301>`__
- Update dev dependencies.
    - Bump pre-commit/black to 25.11.0. `#300 <https://github.com/dajiaji/flask-paseto-extended/pull/300>`__

Version 0.6.1
-------------

Released 2025-11-03

- Add support for Python 3.14. `#293 <https://github.com/dajiaji/flask-paseto-extended/pull/293>`__
- Migrate from poetry to uv. `#292 <https://github.com/dajiaji/flask-paseto-extended/pull/292>`__
- Update dependencies.
    - Bump flask to 3.1.0. `#281 <https://github.com/dajiaji/flask-paseto-extended/pull/281>`__
    - etc.
- Update dev dependencies.
    - Bump pre-commit/isort to 7.0.0. `#291 <https://github.com/dajiaji/flask-paseto-extended/pull/291>`__
    - etc.

Version 0.6.0
-------------

Released 2024-11-16

- Add support for Python 3.13. `#230 <https://github.com/dajiaji/flask-paseto-extended/pull/230>`__
- Drop support for Python 3.8. `#221 <https://github.com/dajiaji/flask-paseto-extended/pull/221>`__
- Fix link on README. `#197 <https://github.com/dajiaji/flask-paseto-extended/pull/197>`__
- Rename CI/CD files. `#195 <https://github.com/dajiaji/flask-paseto-extended/pull/195>`__
- Fix error on populating codecov token. `#194 <https://github.com/dajiaji/flask-paseto-extended/pull/194>`__
- Update dependencies.
    - Bump Flask/Werkzeug to v3. `#229 <https://github.com/dajiaji/flask-paseto-extended/pull/229>`__
    - Bump cryptography to 43.0.1. `#201 <https://github.com/dajiaji/flask-paseto-extended/pull/201>`__
- Update dev dependencies.
    - Bump coverage to 7.6.7. `#227 <https://github.com/dajiaji/flask-paseto-extended/pull/227>`__
    - Bump pre-commit to 4.0.1. `#226 <https://github.com/dajiaji/flask-paseto-extended/pull/226>`__
    - Bump pytest-cov to 6.0.0. `#225 <https://github.com/dajiaji/flask-paseto-extended/pull/225>`__
    - Bump sphinx-rtd-theme to 3.0.2. `#223 <https://github.com/dajiaji/flask-paseto-extended/pull/223>`__
    - Bump blacken-docs to 1.19.1. `#219 <https://github.com/dajiaji/flask-paseto-extended/pull/219>`__
    - Bump mypy to 1.13.0. `#217 <https://github.com/dajiaji/flask-paseto-extended/pull/217>`__
    - Bump tox to 4.23.2. `#216 <https://github.com/dajiaji/flask-paseto-extended/pull/216>`__
    - Bump pre-commit/black to 24.10.0. `#210 <https://github.com/dajiaji/flask-paseto-extended/pull/210>`__
    - Bump pre-commit/pre-commit-hooks to 5.0.0. `#210 <https://github.com/dajiaji/flask-paseto-extended/pull/210>`__
    - Bump pytest to 8.3.3. `#203 <https://github.com/dajiaji/flask-paseto-extended/pull/203>`__
    - Bump pre-commit/flake8 to 7.1.1. `#193 <https://github.com/dajiaji/flask-paseto-extended/pull/193>`__

Version 0.5.2
-------------

Released 2024-08-03

- Update dependencies.
    - Bump cryptography to 42.0.4. `#158 <https://github.com/dajiaji/flask-paseto-extended/pull/158>`__
- Update dev dependencies.
    - Bump codecov/codecov-action to v4. `#183 <https://github.com/dajiaji/python-cwt/pull/183>`__
    - Bump setuptools to 70.0.0. `#186 <https://github.com/dajiaji/flask-paseto-extended/pull/186>`__
    - Bump zipp to 3.19.1. `#185 <https://github.com/dajiaji/flask-paseto-extended/pull/185>`__
    - Bump certifi to 2024.7.4. `#184 <https://github.com/dajiaji/flask-paseto-extended/pull/184>`__
    - Bump urllib3 to 2.2.2. `#181 <https://github.com/dajiaji/flask-paseto-extended/pull/181>`__
    - Bump tox to 4.15.1. `#180 <https://github.com/dajiaji/flask-paseto-extended/pull/180>`__
    - Bump requests to 2.32.0. `#177 <https://github.com/dajiaji/flask-paseto-extended/pull/177>`__
    - Bump jinja2 to 3.1.4. `#175 <https://github.com/dajiaji/flask-paseto-extended/pull/175>`__
    - Bump idna to 3.7. `#171 <https://github.com/dajiaji/flask-paseto-extended/pull/171>`__
    - Bump sphinx-autodoc-typehints to 2.0.1. `#170 <https://github.com/dajiaji/flask-paseto-extended/pull/170>`__
    - Bump pre-commit/black to 24.4.2. `#169 <https://github.com/dajiaji/flask-paseto-extended/pull/169>`__
    - Bump blacken-docs to 1.18.0. `#392 <https://github.com/dajiaji/flask-paseto-extended/pull/169>`__
    - Bump pre-commit/flake8 to 7.1.0. `#380 <https://github.com/dajiaji/flask-paseto-extended/pull/169>`__
    - Bump pre-commit/pre-commit-hooks to 4.6.0. `#380 <https://github.com/dajiaji/flask-paseto-extended/pull/169>`__
    - Bump pytest-cov to 5.0.0. `#167 <https://github.com/dajiaji/flask-paseto-extended/pull/167>`__
    - Bump coverage to 7.4.4. `#164 <https://github.com/dajiaji/flask-paseto-extended/pull/164>`__
    - Bump pytest to 8.1.1. `#163 <https://github.com/dajiaji/flask-paseto-extended/pull/163>`__
    - Bump mypy to 1.9.0. `#162 <https://github.com/dajiaji/flask-paseto-extended/pull/162>`__

Version 0.5.1
-------------

Released 2024-01-27

- Add Python 3.12 to CI. `#149 <https://github.com/dajiaji/flask-paseto-extended/pull/149>`__
- Usee request_ctx instead of _request_ctx_stack. `#131 <https://github.com/dajiaji/flask-paseto-extended/pull/131>`__
- Add Python 3.12 to tox.ini. `#130 <https://github.com/dajiaji/flask-paseto-extended/pull/130>`__
- Fix .readthedocs.yml. `#129 <https://github.com/dajiaji/flask-paseto-extended/pull/129>`__
- Update dependencies.
    - Bump pyseto to 1.7.8. `#149 <https://github.com/dajiaji/flask-paseto-extended/pull/149>`__
    - Bump Werkzeug to 2.3.8. `#132 <https://github.com/dajiaji/flask-paseto-extended/pull/132>`__
    - Bump Flask-Login to 0.6.3. `#119 <https://github.com/dajiaji/flask-paseto-extended/pull/119>`__
    - Bump urllib3 to 2.0.7. `#114 <https://github.com/dajiaji/flask-paseto-extended/pull/114>`__
- Update dev dependencies.
    - Bump sphinx-autodoc-typehints to 1.25.3. `#148 <https://github.com/dajiaji/flask-paseto-extended/pull/148>`__
    - Bump coverage to 7.4.1. `#147 <https://github.com/dajiaji/flask-paseto-extended/pull/147>`__
    - Bump tox to 4.12.1. `#146 <https://github.com/dajiaji/flask-paseto-extended/pull/146>`__
    - Bump jinja2 to 3.1.3. `#144 <https://github.com/dajiaji/flask-paseto-extended/pull/144>`__
    - Bump pre-commit/flake8 to 7.0.0. `#143 <https://github.com/dajiaji/flask-paseto-extended/pull/143>`__
    - Bump pytest to 7.4.4. `#141 <https://github.com/dajiaji/flask-paseto-extended/pull/141>`__
    - Bump mypy to 1.8.0. `#139 <https://github.com/dajiaji/flask-paseto-extended/pull/139>`__
    - Bump pre-commit/black to 23.12.1. `#136 <https://github.com/dajiaji/flask-paseto-extended/pull/136>`__
    - Bump pre-commit/isort to 5.13.2. `#136 <https://github.com/dajiaji/flask-paseto-extended/pull/136>`__
    - Bump sphinx-rtd-theme to 2.0.0. `#134 <https://github.com/dajiaji/flask-paseto-extended/pull/134>`__
    - Bump actions to v4. `#126 <https://github.com/dajiaji/flask-paseto-extended/pull/126>`__
    - Bump pre-commit to 3.5.0. `#113 <https://github.com/dajiaji/flask-paseto-extended/pull/113>`__
    - Bump pre-commit/pre-commit-hooks to 4.5.0. `#110 <https://github.com/dajiaji/flask-paseto-extended/pull/110>`__

Version 0.5.0
-------------

Released 2023-09-17

- Drop support for Python 3.7. `#94 <https://github.com/dajiaji/flask-paseto-extended/pull/94>`__
- Add SECURITY.md. `#89 <https://github.com/dajiaji/flask-paseto-extended/pull/89>`__
- Use allowlist_externals on tox. `#84 <https://github.com/dajiaji/flask-paseto-extended/pull/84>`__
- Update dependencies.
    - Bump Werkzeug to 2.3.7. `#99 <https://github.com/dajiaji/flask-paseto-extended/pull/99>`__
    - Bump Flask to 2.3.3. `#99 <https://github.com/dajiaji/flask-paseto-extended/pull/99>`__
    - Bump Flask-Login to 0.6.2. `#99 <https://github.com/dajiaji/flask-paseto-extended/pull/99>`__
    - Bump pyseto to 1.7.4. `#99 <https://github.com/dajiaji/flask-paseto-extended/pull/99>`__
- Update dev dependencies.
    - Bump pytest to 7.2.0. `#101 <https://github.com/dajiaji/flask-paseto-extended/pull/101>`__
    - Bump pre-commit/flake8 to 6.1.0. `#100 <https://github.com/dajiaji/flask-paseto-extended/pull/100>`__
    - Bump pre-commit/black to 23.9.1. `#100 <https://github.com/dajiaji/flask-paseto-extended/pull/100>`__
    - Bump pre-commit/blacken-docs to 1.16.0. `#100 <https://github.com/dajiaji/flask-paseto-extended/pull/100>`__
    - Bump sphinx to 7.0.1. `#99 <https://github.com/dajiaji/flask-paseto-extended/pull/99>`__
    - Bump requests to 2.31.0. `#97 <https://github.com/dajiaji/flask-paseto-extended/pull/97>`__
    - Bump certifi to 2023.7.22. `#96 <https://github.com/dajiaji/flask-paseto-extended/pull/96>`__
    - Bump pygments to 2.15.0. `#95 <https://github.com/dajiaji/flask-paseto-extended/pull/95>`__
    - Bump pre-commit/isort to 5.11.4. `#86 <https://github.com/dajiaji/flask-paseto-extended/pull/86>`__
    - Bump tox to 3.28.0. `#85 <https://github.com/dajiaji/flask-paseto-extended/pull/85>`__
    - Bump pre-commit/pre-commit-hooks to 4.4.0. `#78 <https://github.com/dajiaji/flask-paseto-extended/pull/78>`__
    - Bump sphinx-rtd-theme to 1.1.1. `#77 <https://github.com/dajiaji/flask-paseto-extended/pull/77>`__
    - Bump pytest-cov to 4.0.0. `#70 <https://github.com/dajiaji/flask-paseto-extended/pull/70>`__

Version 0.4.2
-------------

Released 2022-08-11

- Update dependencies.
    - Bump pyseto to 1.6.10. `#65 <https://github.com/dajiaji/flask-paseto-extended/pull/65>`__
- Update dev dependencies.
    - Bump pre-commit/flake8 to 5.0.4. `#64 <https://github.com/dajiaji/flask-paseto-extended/pull/64>`__
    - Bump sphinx to 5.1.1. `#62 <https://github.com/dajiaji/flask-paseto-extended/pull/62>`__
    - Bump mypy to 0.971. `#60 <https://github.com/dajiaji/flask-paseto-extended/pull/60>`__
    - Bump pre-commit/black to 22.6.0. `#59 <https://github.com/dajiaji/flask-paseto-extended/pull/59>`__
    - Bump tox to 3.25.1. `#58 <https://github.com/dajiaji/flask-paseto-extended/pull/58>`__
    - Bump pre-commit/pre-commit-hooks to 4.3.0. `#54 <https://github.com/dajiaji/flask-paseto-extended/pull/54>`__
- Drop support for Python3.6. `#57 <https://github.com/dajiaji/flask-paseto-extended/pull/57>`__

Version 0.4.1
-------------

Released 2022-04-09

- Refine pyproject, tox.ini and github actions. `#44 <https://github.com/dajiaji/flask-paseto-extended/pull/44>`__
- Update dependencies.
    - Update mypy requirement from ^0.910 to ^0.942. `#43 <https://github.com/dajiaji/flask-paseto-extended/pull/43>`__
    - Update pre-commit-hooks from 4.0.1 to 4.1.0. `#37 <https://github.com/dajiaji/flask-paseto-extended/pull/37>`__
    - Update pytest requirement from ^5.2 to ^6.2. `#36 <https://github.com/dajiaji/flask-paseto-extended/pull/36>`__

Version 0.4.0
-------------

Released 2021-12-11

- Migrate the project to poetry. `#33 <https://github.com/dajiaji/flask-paseto-extended/pull/33>`__
- Add support for kid. `#32 <https://github.com/dajiaji/flask-paseto-extended/pull/32>`__

Version 0.3.3
-------------

Released 2021-11-24

- Refine README and docstring for Read the Docs. `#29 <https://github.com/dajiaji/flask-paseto-extended/pull/29>`__
- Refine example. `#28 <https://github.com/dajiaji/flask-paseto-extended/pull/28>`__

Version 0.3.2
-------------

Released 2021-11-23

- Fix .readthedocs not to use setup.py. `#27 <https://github.com/dajiaji/flask-paseto-extended/pull/27>`__

Version 0.3.1
-------------

Released 2021-11-23

- Introduce flit for publishing. `#25 <https://github.com/dajiaji/flask-paseto-extended/pull/25>`__

Version 0.3.0
-------------

Released 2021-11-23

- Add PasetoIssuer and PasetoVerifier. `#19 <https://github.com/dajiaji/flask-paseto-extended/pull/19>`__

Version 0.2.0
-------------

Released 2021-10-24

- Refine app.config name for PasetoLoginManager. `#16 <https://github.com/dajiaji/flask-paseto-extended/pull/16>`__
- Add tests for PasetoLoginManager. `#16 <https://github.com/dajiaji/flask-paseto-extended/pull/16>`__
- Rename package name from Flask PASETO Extended to flask-paseto-extended. `#15 <https://github.com/dajiaji/flask-paseto-extended/pull/15>`__
- Add tests for PasetoCookieSessionInterface. `#14 <https://github.com/dajiaji/flask-paseto-extended/pull/14>`__

Version 0.1.1
-------------

Released 2021-10-23

- Activate Read the Docs. `#12 <https://github.com/dajiaji/flask-paseto-extended/pull/12>`__

Version 0.1.0
-------------

Released 2021-10-23

- First public release. `#11 <https://github.com/dajiaji/flask-paseto-extended/pull/11>`__
