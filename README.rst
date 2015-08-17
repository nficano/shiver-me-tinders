=================
Shiver me Tinders
=================
A lightweight wrapper around the Tinder undocumented API.

Requirements
============

- Python 2.6+ (2.7 or 3.4 recommended)
- PIP (for some installation methods)
- GIT (for some installation methods)

Installation
============

If you are on Mac OS X or Linux, chances are that one of the following two commands will work for you:

Installation
============

Using PIP via PyPI

.. code:: bash

    pip install shiver_me_tinders

Using PIP via Github

.. code:: bash

    pip install git+git://github.com/NFicano/shiver-me-tinders.git#egg=shiver_me_tinders

Adding to your ``requirements.txt`` file (run ``pip install -r requirements.txt`` afterwards)

.. code:: bash

    git+ssh://github.com/NFicano/shiver-me-tinders.git#egg=shiver_me_tinders

Manually via GIT

.. code:: bash

    git clone git://github.com/NFicano/shiver-me-tinders.git shiver-me-tinders
    cd shiver-me-tinders
    python setup.py install


Usage Example
=============

.. code:: python

    from shiver_me_tinder import Tinder
    tinder = Tinder(fb_token='xxx', fb_id=1001, lat=40.0, lon=-70.0)

    # Or initialize it with a yaml file (see included config.yaml.sample).
    tinder = Tinder.config_from_file('/path/to/file/config.yaml')

    matches = Tinder.get_matches()
    for match in matches:
        # Show users' name + photos.
        print match.name, match.photos

        # Now tip your hat at them...
        tinder.like(match)
