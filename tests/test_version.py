import docs.conf
import pyticketswitch
import re


def test_versions():
    # check all the version numbers are consistent.
    print('pyticketswitch/init.py: {}'.format(pyticketswitch.__version__))
    print('docs/conf.py (version): {}'.format(docs.conf.version))
    print('docs/conf.py (release): {}'.format(docs.conf.release))

    setup = None
    with open('setup.py', 'r') as fh:
        match = re.search(r"\s*version\s*=\s*'([^']+)'", fh.read())
        if match:
            setup = match.group(1)
            print('setup.py: {}'.format(setup))
        else:
            print('setup.py: MISSING!')

    all_match = all(
        version == pyticketswitch.__version__
        for version in [docs.conf.version, docs.conf.release, setup]
    )
    assert all_match, 'Version numbers do not match pyticketswitch.__version__'

    # check that the change log has an entry for this version
    with open('CHANGELOG.md', 'r') as fh:
        match = re.search(
            "## \[{}\]".format(pyticketswitch.__version__), fh.read())
        assert match, 'no entry in CHANGELOG.md for current version {}'.format(
            pyticketswitch.__version__
        )
        print("CHANGELOG.md: {}".format(
            pyticketswitch.__version__
        ))
