# erc20-contract-testing-experiment

Messing about with [web3.py](https://web3py.readthedocs.io/en/stable/) to run unit tests on the latest hot coin: XYZ token.

The `builds/` directory is currently checked-in to facilitate testing.

To test (in Bash):
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest -v
```

Tested with Python 3.9.7 built via pyenv on Linux Mint 19.3.
