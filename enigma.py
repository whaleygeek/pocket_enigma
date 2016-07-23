# enigma.py  23/07/2016  D.J.Whale
#
# A simple simulation of the pocket enigma machine bought from Bletchley Park
#
# As reviewed and commented on by it's original author here:
#   http://www.savory.de/pocket_enigma.htm

# Note, this simulator does not use the 'code the key as the first character'
# protocol. So if you want to cipher text given to you by such an algorithm,
# first cipher the single letter given to you as the ciphered key, and use the
# plaintext version that comes back as the key to this program.
#
# This was done just to keep the operation of this program as simple and generic
# as possible.

import sys

WHEEL0 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WHEEL1 = "ZEXKBHJFMGDRIONVTLUQSPYCWA"
WHEEL2 = "CDABWIPMFKJNHLQGOZUVSTEYXR"
wheels = [WHEEL0, WHEEL1, WHEEL2]


def usage():
    """Show user instructions"""

    print("usage: python enigma.py <wheel_no> <start_letter> <step> <message>")
    print("e.g. python enigma.py 2 J -2 hello world")


def cipher(wheel, offset, ch):
    """cipher a single letter using a wheel with a given offset"""

    # how far round from 'A' is the user letter?
    user_index = ord(ch) - ord('A')
    # how far round the wheel is user_index, accounting for offset
    u2 = (user_index - offset) % 26
    # look this up to see where it jumps to
    d = ord(wheel[u2]) - ord('A')
    # work out what this distance is
    diff = (d - u2) % 26
    # add the distance on to the input character
    ch = chr(((user_index + diff) % 26) + ord('A'))
    return ch


def process(wheel, start, step, message):
    """Process a whole message with given wheel settings"""

    result = ""
    offset = ord(start[0].upper()) - ord('A') # to an offset 0..25

    for ch in message:
        if ch == ' ': continue # skip any spurious spaces
        if not ch.isalpha():
            raise ValueError("only letters are allowed")
        ch = ch.upper()

        ch2 = cipher(wheel, offset, ch)
        result += ch2
        offset = (offset + step) % 26 # turn the wheel

    return result


def group5(message):
    """Turn a message into spaced groups of 5 characters"""

    result = ""
    for i in range(len(message)):
        ch = message[i]
        result += ch
        if (i+1) % 5 == 0 and i != len(message):
            result += ' '
    return result


def main():
    """Process command line arguments and process a whole message"""

    wheel_no = int(sys.argv[1])
    wheel = wheels[wheel_no]
    start = sys.argv[2]
    step = int(sys.argv[3])

    message = ""
    for m in sys.argv[4:]:
        message += m

    result = process(wheel, start, step, message)
    result = group5(result)
    print(result)


if __name__ == "__main__":
    """This code is called if you run this as the main program.
        You can 'import enigma' instead and then call the functions yourself"""

    try:
        main()
    except Exception as e:
        usage()
        print("error: %s" % e)
        print("")

# END

