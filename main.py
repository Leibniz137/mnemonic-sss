from pprint import pprint

from mnemonic import Mnemonic
from secretsharing import (
    points_to_secret_int,
    secret_int_to_points,
    SecretSharer,
)

from six import integer_types

# generate a seed phrase on the spot
GENERATE = 'generate'

# take 2 of the 3 shares and restore the original seed phrase
RESTORE = 'restore'

# take an existing seed phrase and split it into pieces
SPLIT = 'split'


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
        secret_list = int_to_charset(secret_int, cls.secret_charset)
        if len(secret_list) in (11, 23):
            # we need to add a leading zero
            return [cls.mnemo.wordlist[0]] + secret_list
        return secret_list


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


def read_words():
    words = []
    i = 1
    word = input('Enter word {}: '.format(i))
    while word:
        if word not in SeedPhraseToSeedPhraseSecretSharer.mnemo.wordlist:
            print("Error, word is not in official wordlist, reenter word")  # noqa: E501
        else:
            words.append(word)
            i += 1
        word = input('Enter word {}: '.format(i))
    return words


def generate(strength=256):
    m = SeedPhraseToSeedPhraseSecretSharer.mnemo.generate(strength=strength).split(' ')   # noqa: E501
    pprint(m)
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(m, 2, 3)

    # make sure that the split worked successfully!
    reconsituted_seed1 = SeedPhraseToSeedPhraseSecretSharer.recover_secret(shares[0:2])   # noqa: E501
    assert m == reconsituted_seed1
    reconsituted_seed2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret(shares[1:3])   # noqa: E501
    assert m == reconsituted_seed2

    for i, share in enumerate(shares):
        pprint(share)
        input("Did you write down the share? Include it's order! (ie 1st, 2nd, or 3rd) ")   # noqa: E501
    input("Did you know that you need to include the share order to successfully restore the seed? ")   # noqa: E501

    test_user_entries(shares)


def restore():
    ith = input("Which share do you want to input? (enter '1', '2', or '3') ")
    i = int(ith)
    print(
        'Enter share {}, press enter twice to mark share as complete'
        .format(ith))
    share_i = read_words()

    jth = input("Which share do you want to input? (enter '1', '2', or '3') ")
    j = int(jth)
    if i == j:
        raise ValueError("Must input a different share.")
    print(
        'Enter share {}, press enter twice to mark share as complete'
        .format(jth))
    share_j = read_words()

    seed = SeedPhraseToSeedPhraseSecretSharer.recover_secret([
        (i, share_i),
        (j, share_j)
    ])
    input('Press Enter to view restored restored seed:')
    print(seed)


def split():
    print('Enter seed phrase, press enter twice to mark seed as complete')
    seed = read_words()
    shares = SeedPhraseToSeedPhraseSecretSharer.split_secret(seed, 2, 3)

    # make sure that the split worked successfully!
    reconsituted_seed1 = SeedPhraseToSeedPhraseSecretSharer.recover_secret(shares[0:2])   # noqa: E501
    assert seed == reconsituted_seed1
    reconsituted_seed2 = SeedPhraseToSeedPhraseSecretSharer.recover_secret(shares[1:3])   # noqa: E501
    assert seed == reconsituted_seed2
    for i, share in enumerate(shares):
        pprint(share)
        input("Did you write down the share? Include it's order! (ie 1st, 2nd, or 3rd) ")   # noqa: E501
    input("Did you know that you need to include the share order to successfully restore the seed? ")   # noqa: E501
    test_user_entries(shares)


def test_user_entries(shares):
    """
    interactively test the user to make sure
    that they wrote the shares down correctly
    """
    fifteenth_entry_1st_share = input("What's the 15th entry in the 1st share? ")   # noqa: E501
    if fifteenth_entry_1st_share != shares[0][1][14]:
        raise ValueError("Mismatch! {} != {} Try Again!!!".format(fifteenth_entry_1st_share, shares[0][1][14]))   # noqa: E501

    fouth_entry_2nd_share = input("What's the 4th entry in the 2nd share? ")
    if fouth_entry_2nd_share != shares[1][1][3]:
        raise ValueError("Mismatch! {} != {} Try Again!!!".format(fouth_entry_2nd_share, shares[1][1][3]))   # noqa: E501

    seventeenth_entry_3rd_share = input("What's the 17th entry in the 3rd share? ")   # noqa: E501
    if seventeenth_entry_3rd_share != shares[2][1][16]:
        raise ValueError("Mismatch! {} != {} Try Again!!!".format(seventeenth_entry_3rd_share, shares[2][1][16]))   # noqa: E501
    print('Looks Good!')


def main(args):
    if args.action == GENERATE:
        generate()
    elif args.action == RESTORE:
        restore()
    elif args.action == SPLIT:
        split()
    else:
        raise ValueError("Unknown action {}".format(args.action))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[RESTORE, GENERATE, SPLIT])
    args = parser.parse_args()
    main(args)
