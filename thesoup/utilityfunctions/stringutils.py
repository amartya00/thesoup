from thesoup.utilityclasses.sets import CountSet


def is_anagram(s1: str, s2: str) -> bool:
    """
    This function takes 2 strings as input and tells if they are anagrams of each other. 2 strings are anagrams if they
    can be constructed by rearranging the other word.

    :param s1: The first string
    :param s2: The second string
    """
    counts1 = CountSet(s1)
    counts2 = CountSet(s2)
    return counts1 == counts2
