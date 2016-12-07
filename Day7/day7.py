import re


# regular expression used to segment addresses into parts
split_alpha_sequence_re = re.compile('\W')


def search_for_abba_sequence(s):
    """
    Determine whether there is an 'ABBA' (e.g. 'xyyz', 'foof') sequences within a string.

    :param s: string to search in
    :return: boolean depending on whether an abba sequence was found
    """

    # pythons RE support doesn't appear to correctly support group-matches :|
    # so instead of just using the re: '(.)(.)\2\1' to match abba sequences, do something dumber that works :|

    for d,e,f,g in zip(s,s[1:],s[2:],s[3:]):
        if d==g and e==f and d!=e:
            return True

    return False

def split_address(address):
    """
    Split an address into a list of parts.

    :param address: string containing the address to process
    :return: list of address parts, even-indexed parts are 'outside' brackets, odd-indexed parts 'inside'
    """
    addrparts = split_alpha_sequence_re.split(address)

    # there should be an odd number of parts, addresses should start and end with unbracketed parts, e.g. 'a[b]c[d]e'
    assert ((len(addrparts) % 2) == 1)

    return addrparts


def does_address_support_tls(address):
    """
    Determine if an address supports TLS.

    :param address: string containing the address
    :return: boolean
    """
    # split the address such that the even parts are outside delimeters, and odd parts are inside delimiters
    addrparts = split_address(address)

    # this address is valid if the first part that contains an 'abba' sequence is even and NO PART THAT ODD does
    valid_even_part = False
    for i, part in enumerate(addrparts):
        if search_for_abba_sequence(part):
            if (i % 2) == 0:
                # this is an even part, the address MIGHT support TLS
                valid_even_part = True
            else:
                # this is an odd part, the address definitely does not support TLS
                return False

    return valid_even_part


def count_tls_capable_addresses(addresses):
    """
    :param addresses: list of strings containing addresses
    :return: integer count
    """
    tls_capable_addresses = [addr for addr in addresses if does_address_support_tls(addr)]
    return len(tls_capable_addresses)


def find_aba_and_bab_sequences(address_parts):
    """
    Determine the 'ab' for 'aba' sequences (for even/outside bracket parts) and 'bab' sequences (for odd/inside bracket parts).

    Example: given parts ['abba','piip','saas'] then the aba set will be [('a','b'),('s','a')] and the bab set [('i','p')]

    :param address_parts: list of parts
    :return: a tuple of (aba, bab), where both are sets containing tuples of characters (a,b). See example above.
    """
    aba = set()
    bab = set()

    for i, part in enumerate(address_parts):
        for d, e, f in zip(part, part[1:], part[2:]):
            if d == f and d != e:
                if (i % 2) == 0:
                    # aba sequences in even parts go in the aba set
                    aba.add((d,e))
                else:
                    # bab sequences in the odd parts go in the bab set
                    bab.add((e,d))

    return aba, bab


def does_address_support_ssl(address):
    """
    Determine if an address supports SSL.

    :param address: string containing the address
    :return: boolean
    """
    # split the address such that the even parts are outside delimeters, and odd parts are inside delimiters
    addrparts = split_address(address)

    # get the aba and bab sequence sets
    aba_set, bab_set = find_aba_and_bab_sequences(addrparts)

    # if there is a matching aba entry to any bab entry, then this address supports ssl
    return len(aba_set.intersection(bab_set)) != 0


def count_ssl_capable_addresses(addresses):
    """
    :param addresses: list of strings containing addresses
    :return: integer count
    """
    ssl_capable_addresses = [addr for addr in addresses if does_address_support_ssl(addr)]
    return len(ssl_capable_addresses)


if __name__ == '__main__':
    with(open('input_7a.txt', 'r')) as infile:
        addresses = infile.read().splitlines()

    print(count_tls_capable_addresses(addresses))
    print(count_ssl_capable_addresses(addresses))




