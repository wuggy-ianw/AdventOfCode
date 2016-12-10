import re

# match input text that starts with zero or more content characters followed by a single
# duplication directive e.g. '(4x2)'. Group 1 is the non-directive prefix, group 2 and 3
# are the values in the directive (number of characters to repeat, number of repeats).
match_text_then_duplicate_directive_re = re.compile('([^(]*)\(([0-9]+)x([0-9]+)\)')

def decompress(compressed):
    pos = 0
    output=''

    while(pos<len(compressed)):
        # find the first match after pos
        match = match_text_then_duplicate_directive_re.match(compressed,pos=pos)
        if match:
            prefix, numchars, numrepeats = match.group(1,2,3)
            pos = match.end()

            output = output + prefix + (compressed[pos:pos+int(numchars)]*int(numrepeats))
            pos += int(numchars)
        else:
            # if there was no match, then the remainder of input includes no directives
            output = output + compressed[pos:]
            pos = len(compressed)

    return output

def decompressed_length(compressed, v2=False):
    # assuming we don't have 'split' directives, then we can apply this recursively
    pos = 0
    outputlen = 0

    while (pos < len(compressed)):
        # find the first match after pos
        match = match_text_then_duplicate_directive_re.match(compressed, pos=pos)
        if match:
            prefix, numchars, numrepeats = match.group(1, 2, 3)
            pos = match.end()

            outputlen += len(prefix)

            # get the sequence from performing this directive, and then try and decompress it
            decompseq = compressed[pos:pos + int(numchars)]
            if v2:
                outputlen += decompressed_length(decompseq, v2) * int(numrepeats)
            else:
                outputlen += len(decompseq) * int(numrepeats)

            pos += int(numchars)
        else:
            # if there was no match, then the remainder of input includes no directives
            outputlen += len(compressed[pos:])
            pos = len(compressed)

    return outputlen

if __name__ == '__main__':
    with(open('input_9a.txt', 'r')) as infile:
        compressedlines = infile.read().splitlines()

    # should only be one line!
    assert(len(compressedlines)==1)

    print(decompressed_length(compressedlines[0], v2=False))
    print(decompressed_length(compressedlines[0], v2=True))



