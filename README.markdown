
# Installation

Checkout repository, no dependencies required other than Python 3,
just setup a virtualenv and go at it.

    git clone whatever-github-tells-you-path-is
    cd accounting
    python3 -mvenv env
    . ./env/bin/activate
    
Run the tests:

    python -munittest tests/test_ledger.py

Run the output generating script:

    python test.py

That's pretty much it!