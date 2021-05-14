# python2
from pprint import pprint

from mnemonic import Mnemonic
from secretsharing import (
    points_to_secret_int,
    secret_int_to_points,
    SecretSharer,
)

from six import integer_types


class SeedPhraseToSeedPhraseSecretSharer(SecretSharer):
    mnemo = Mnemonic("english")
    secret_charset = mnemo.wordlist
    share_charset = mnemo.wordlist

    @classmethod
    def split_secret(cls, secret_string, share_threshold, num_shares):
        secret_int = charset_to_int(secret_string, cls.secret_charset)
        points = secret_int_to_points(secret_int, share_threshold, num_shares)
        shares = []
        for point in points:
            shares.append(point_to_share_string(point, cls.share_charset))
        return shares

    @classmethod
    def recover_secret(cls, shares):
        points = []
        for share in shares:
            points.append(share_string_to_point(share, cls.share_charset))
        secret_int = points_to_secret_int(points)
        secret_string = int_to_charset(secret_int, cls.secret_charset)
        return secret_string


def int_to_charset(val, charset):
    """ Turn a non-negative integer into a string.
    """
    if not val >= 0:
        raise ValueError('"val" must be a non-negative integer.')
    if val == 0:
        return charset[0]
    # in original function, this is a emtpy string not empty list
    output = []
    while val > 0:
        val, digit = divmod(val, len(charset))
        output.append(charset[digit])
    # reverse the characters in the output and return
    return output[::-1]


def point_to_share_string(point, charset):
    """ Convert a point (a tuple of two integers) into a share string - that is,
        a representation of the point that uses the charset provided.
    """
    # point should be in the format (1, 4938573982723...)
    if '-' in charset:
        raise ValueError(
            'The character "-" cannot be in the supplied charset.')
    if not (isinstance(point, tuple) and len(point) == 2 and
            isinstance(point[0], integer_types) and
            isinstance(point[1], integer_types)):
        raise ValueError(
            'Point format is invalid. Must be a pair of integers.')
    x, y = point
    # x_list = int_to_charset(x, charset)
    y_list = int_to_charset(y, charset)
    share_list = (x, y_list)
    return share_list


def share_string_to_point(share_tuple, charset):
    """ Convert a share string to a point (a tuple of integers).
    """
    # share should be in the format "(1, ['able', 'daughter', ...])"
    (x, y_list) = share_tuple
    y = charset_to_int(y_list, charset)
    return (x, y)


def charset_to_int(s, charset):
    """ Turn a string into a non-negative integer.
    """
    output = 0
    for char in s:
        output = output * len(charset) + charset.index(char)
    return output


def main():
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate().split(' ')
    pprint(m)
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 2, 3)
    pprint(shares)
    m2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret(shares[0:2])
    pprint(m2)
    assert m == m2


if __name__ == '__main__':
    main()
