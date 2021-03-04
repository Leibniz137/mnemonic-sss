import pytest

from main import SeedPhraseToSeedPhraseSecretSharer


@pytest.mark.parametrize('i, j', [
    (0, 1),
    (0, 2),
    (1, 2),
])
def test_reconstruction(i, j):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate().split(' ')
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 2, 3)
    share_i = shares[i]
    share_j = shares[j]
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret([share_i, share_j])
    assert m == m2
