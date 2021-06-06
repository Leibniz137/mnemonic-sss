from itertools import permutations

import pytest

from main import SeedPhraseToSeedPhraseSecretSharer


@pytest.mark.parametrize('i, j', permutations(range(0, 2), r=2))
def test_reconstruction(i, j):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate().split(' ')
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 2, 3)
    share_i = shares[i]
    share_j = shares[j]
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret([share_i, share_j])
    assert m == m2


@pytest.mark.parametrize('i, j, k', permutations(range(0, 5), r=3))
def test_reconstruction_3_of_5(i, j, k):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate().split(' ')
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 3, 5)
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret([
        shares[i],
        shares[j],
        shares[k]
    ])
    assert m == m2


@pytest.mark.parametrize('i, j', permutations(range(0, 2), r=2))
def test_reconstruction_256(i, j):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate(strength=256).split(' ')   # noqa: E501
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 2, 3)
    share_i = shares[i]
    share_j = shares[j]
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret([share_i, share_j])
    assert m == m2


@pytest.mark.parametrize('i, j, k', permutations(range(0, 5), r=3))
def test_reconstruction_3_of_5_256(i, j, k):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate(strength=256).split(' ')   # noqa: E501
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 3, 5)
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret([
        shares[i],
        shares[j],
        shares[k]
    ])
    assert m == m2
