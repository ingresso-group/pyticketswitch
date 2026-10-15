import re

import docs.conf
import pyticketswitch


def test_versions():
    # the package version is the single source of truth (pyproject.toml reads
    # it dynamically), so just check the docs follow it.
    print(f"pyticketswitch/__init__.py: {pyticketswitch.__version__}")
    print(f"docs/conf.py (version): {docs.conf.version}")
    print(f"docs/conf.py (release): {docs.conf.release}")

    assert docs.conf.version == pyticketswitch.__version__
    assert docs.conf.release == pyticketswitch.__version__

    # check that the change log has an entry for this version
    with open("CHANGELOG.md") as fh:
        match = re.search(rf"## \[{pyticketswitch.__version__}\]", fh.read())
        assert match, (
            f"no entry in CHANGELOG.md for current version {pyticketswitch.__version__}"
        )
        print(f"CHANGELOG.md: {pyticketswitch.__version__}")
