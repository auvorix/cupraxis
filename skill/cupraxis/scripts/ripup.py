import sys, io
board = sys.argv[1]
t = io.open(board, encoding="utf-8").read()

def strip_items(text, tokens):
    out = []
    i = 0
    n = len(text)
    removed = {tok:0 for tok in tokens}
    while i < n:
        # detect top-level item start: newline + single tab + '(' + token
        matched = None
        if text.startswith("\n\t(", i):
            for tok in tokens:
                if text.startswith("\n\t(%s" % tok, i):
                    # ensure next char after token is space or newline or '(' (whole token)
                    j = i + 3 + len(tok)
                    if j <= n and (text[j] in " \n("):
                        matched = tok
                        break
        if matched:
            # find balanced close starting at the '(' which is at i+1 (after \n)
            start_paren = i + 1  # position of '\t'? no; '(' is at i+2
            p = text.index("(", i)
            depth = 0
            k = p
            instr = False
            while k < n:
                c = text[k]
                if c == '"':
                    instr = not instr
                elif not instr:
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                        if depth == 0:
                            k += 1
                            break
                k += 1
            removed[matched] += 1
            # skip the leading \n and the item (drop it entirely, including preceding \n)
            i = k
            continue
        out.append(text[i])
        i += 1
    return "".join(out), removed

newt, removed = strip_items(t, ["segment", "via", "arc"])
io.open(board, "w", encoding="utf-8", newline="").write(newt)
print("removed:", removed)
print("delta chars:", len(newt) - len(t))
