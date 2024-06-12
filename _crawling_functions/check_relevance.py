import re


def contains_post_digits(url, pattern):
    """
    Check if a string contains a pattern of digits.
    It checks for a slash followed by 5 or more digits.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string contains the pattern, False otherwise.
    """

    return bool(re.search(pattern, url))


def set_elements_startwith(set_, start_arr):
    new_set = {
        element for element in set_ if any(
            element.startswith(begin) for begin in start_arr
        )
    }
    return new_set


def set_elements_contains(set_, includes_arr):
    new_set = {
        url for url in set_ if any(inc in url for inc in includes_arr)
    }
    return new_set


def set_elements_notcontains(set_, excludes_arr):
    new_set = {
        url for url in set_ if not any(exc in url for exc in excludes_arr)
    }
    return new_set


def set_elements_startwith_regex(set_, pattern):
    new_set = {
        element for element in set_ if re.match(pattern, element)
    }
    return new_set


def set_elements_notstartwith_regex(set_, pattern):
    new_set = {
        element for element in set_ if not re.match(pattern, element)
    }
    return new_set


def set_elements_contain_regex(set_, pattern):
    new_set = {
        element for element in set_ if re.search(pattern, element)
    }
    return new_set


def set_elements_notcontain_regex(set_, pattern):
    new_set = {
        element for element in set_ if not re.search(pattern, element)
    }
    return new_set


def relevant_set_regex(
    set_,
    starts_pattern=None, notstart_pattern=None,
    includes_pattern=None, excludes_pattern=None
):
    if starts_pattern:
        set_ = set_elements_startwith_regex(set_, starts_pattern)
    if notstart_pattern:
        set_ = set_elements_notstartwith_regex(set_, notstart_pattern)
    if includes_pattern:
        set_ = set_elements_contain_regex(set_, includes_pattern)
    if excludes_pattern:
        set_ = set_elements_notcontain_regex(set_, excludes_pattern)
    return set_


def relevant_set(
    set_,
    start_arr=None, includes_arr=None, excludes_arr=None
):

    if start_arr:
        set_ = set_elements_startwith(set_, start_arr)
    if includes_arr:
        set_ = set_elements_contains(set_, includes_arr)
    if excludes_arr:
        set_ = set_elements_notcontains(set_, excludes_arr)
    return set_


def remove_subset(bigset, subset):
    """
    Remove all elements of a subset from a larger set.

    The function creates a new set from the elements of 'bigset' that are not
    in 'subset'.

    Args:
        bigset (set): The larger set to remove elements from.
        subset (set): The set of elements to remove from 'bigset'.

    Returns:
        set: The resulting set after removing the elements of 'subset'
            from 'bigset'.
    """
    return {element for element in bigset if element not in subset}
