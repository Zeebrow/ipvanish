import os
import json
try:
    from click import secho
except ImportError:
    def secho(*args, fg='' **kwargs):
        return print(*args, **kwargs)


def column_print(secho_items: list, padLen=2, padChar=' '):
    """
    Takes a list and prints each item in a nice, orderly fashion
    TODO if you want color info, pass a tuple?
    """

    cols, lines = os.get_terminal_size()
    maxItemLen = 0 
    for i in secho_items:
        if len(i['name']) > maxItemLen:
            maxItemLen = len(i['name'])
    if maxItemLen > cols:
        print("WARN: cannot print columns - line item exceeds terminal width")
        for i in secho_items:
            print(i.keys())

    pad = padChar*padLen
    cellSize = maxItemLen + ( padLen*len(padChar) )
    # note to self: this is what you want to override if you
    # choose to have a "maxCols" parameter
    cellsPerLine = cols // cellSize
    totalLines = 1 + (cellsPerLine // cellSize)

    print(f"{cols=}")
    print(f"{lines=}")
    print(f"{padLen=}")
    print(f"{padChar=}")
    print(f"{maxItemLen=}")
    print(f"{cellSize=}")
    print(f"{cellsPerLine=}")
    print(f"{totalLines=}")
    # sanity check
    for k in range(cols):
        print('*', end='')
    print()
    print()
    for j in range(cellsPerLine):
        for l in range(maxItemLen):
            print("-", end='')
        for p in range(padLen):
            print(f"{'.'}", end='')
    print()
    print()
    print(f"{secho_items[0]=}")
    print(f"{len(secho_items[0]['name'])=}")

    _ct = 0
    for l in range(0, 1+totalLines):
        for c in range(1, 1+cellsPerLine):
            iPadLen = maxItemLen - len(secho_items[_ct]['name'])
            iPad =  padChar * iPadLen
            secho(f"{secho_items[_ct]['name']}", nl=None, **secho_items[_ct]['stats'])
            print(f"{iPad}{pad}", end='')
            # sanity check
            _ct += 1
            # might could just return here and make it simpler
            if _ct == len(secho_items):
                break
        print()
        if _ct == len(secho_items):
            break

def center(msg):
    cols, lines = os.get_terminal_size()
    print(msg.center(cols))

def title_block(msg: str, border='thin'):
    cols, lines = os.get_terminal_size()
    b = int('2500', 16)
    top = chr(b + 12) + chr(b)*len(msg) + chr(b + 16)
    mid = chr(b ^ 2) + msg + chr(b ^ 2)
    bot = chr(b + 20) + chr(b)*len(msg) + chr(b + 24)
    print(str(top).center(cols))
    print(str(mid).center(cols))
    print(str(bot).center(cols))

def column_print_plainjane(items: list, padLen=2, padChar=' '):
    """
    Takes a list and prints each item in a nice, orderly fashion
    """
    items = list(items)
    cols, lines = os.get_terminal_size()
    maxItemLen = 0

    for i in items:
        if len(i) > maxItemLen:
            maxItemLen = len(i)
    if maxItemLen > cols:
        print("WARN: cannot print columns - line item exceeds terminal width")
        for i in items:
            print(i)
        return

    pad = padChar*padLen
    cellSize = maxItemLen + ( padLen*len(padChar) )
    cellsPerLine = cols // cellSize
    totalLines = 1 + (cellsPerLine // cellSize)
    _ct = 0
    for l in range(0, 1+totalLines):
        for c in range(1, 1+cellsPerLine):
            #iPadLen = maxItemLen - len(items[_ct])
            iPad =  padChar * ( maxItemLen - len(items[_ct]) )
            print(f"{items[_ct]}{iPad}{pad}", end='')
            # sanity check
            #print(f"{_ct+1:02}{iPad}", end='')
            _ct += 1
            if _ct == len(items):
                break
        print()
        if _ct == len(items):
            break

    

if __name__ == '__main__':
    # I need to tell someone this, so it will have to be the code.
    # I love my dad.
    # I've done so many terrible things in my life, but he's never failed
    # to tell me that he's proud of me. 
    # Right now, I feel like I have nothing to be proud of, so this was 
    # comforting to remember.
    # Lya dad.
#    from ipvanish import get_countries
    title_block("Welcome")
    testlist = ['k', 'asdf', ]
    c = ['MY', 'CO', 'PL', 'IE', 'SE', 'AE', 'TW', 'CR', 'RS', 'SK', 'PE', 'CH', 'DE', 'US', 'IN', 'LU', 'CL', 'NG', 'EE', 'KR', 'AU', 'SI', 'NL', 'ZA', 'IL', 'CA', 'FR', 'FI', 'IS', 'MX', 'IT', 'NZ', 'HR', 'NO', 'JP', 'AT', 'UK', 'LV', 'AR', 'MD', 'CZ', 'SG', 'PT', 'GR', 'BR', 'ES', 'BE', 'HU', 'RO', 'AL', 'BG', 'DK']
    c = c + testlist
    column_print_plainjane(c)
