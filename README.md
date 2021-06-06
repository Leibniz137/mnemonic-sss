Mnemonic-sss is a tool to split a seed phrase into a 2-of-3 Shamir Secret Shares.

The purpose of this tool is to provide safety and redundancy to your seed phrase backup.

Only 2 of the 3 shares are required to reconstruct your seed phrase.

These shares are comprised of 29 or 30 words taken from the official set of english BIP-39 words.
As with a seed phrase, words instead of characters or numbers are to provide the same redundancy and
ease of use that the original seed phrase provides.

Taken individually, each share reveals no information about the seed phrase, however,
it is possibly to reconstruct the seed using any 2 shares.

Note that, in addition to writing down the share words, you'll need to note the order of the share (ie 1st, 2nd, or 3rd)

Keep these shares physically separate locations.

# Install

## Natively
```
pip install -r ./requirements.txt
```

## Docker
```
docker build -t mnemo .

# do not allow any network connections during runtime
docker run --network=none --rm -it mnemo --help
```

# Usage
```
usage: main.py [-h] {restore,generate,split}

positional arguments:
  {restore,generate,split}

optional arguments:
  -h, --help            show this help message and exit
```

## Modes of Operation
### restore
This mode interactively prompts the user to enter their shares and reconstructs the original seed phrase

### generate
This mode generates a seed phrase and displays the 3 shares

### split
This mode prompts the user to enter an existing seed phrase, and splits it into 3 shares.
