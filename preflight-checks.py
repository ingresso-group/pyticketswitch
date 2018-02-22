import docs.conf
import pyticketswitch
import re

if __name__ == '__main__':

    # check all the version numbers are consistent.
    print('pyticketswitch/init.py:', pyticketswitch.__version__)
    print('docs/conf.py (version): ', docs.conf.version)
    print('docs/conf.py (release): ', docs.conf.release)

    setup = None
    with open('setup.py', 'r') as fh:
        match = re.search(r"\s*version\s*=\s*'([^']+)'", fh.read())
        if match:
            setup = match.group(1)
            print('setup.py: ', setup)
        else:
            print('version info missing from setup.py')

    all_match = all(
        version == pyticketswitch.__version__
        for version in [docs.conf.version, docs.conf.release, setup]
    )
    assert all_match
