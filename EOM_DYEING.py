import itertools
text = "INSERT TEXT TO BE FORMATTED HERE"

def alternating(text, c1, c2):
    textf = list(text)
    p2 = textf[1::2]
    p1 = textf[::2]
    p1c = []
    p2c = []
    for i in p1:
        if i == " ":
            p1c.append(i)
        else:
            p1c.append(c1 + i)
    for i in p2:
        if i == " ":
            p2c.append(i)
        else:
            p2c.append(c2 + i)
    form = []
    for f,b in itertools.zip_longest(p1c, p2c):
        if f:
            form.append(f)
        if b:
            form.append(b)
    return "".join(form)

def triplealternate(text, c1, c2, c3):
    textf = list(text)
    p4 = textf[3::4]
    p3 = textf[2::4]
    p2 = textf[1::4]
    p1 = textf[::4]
    p4c = []
    p3c = []
    p2c = []
    p1c = []
    for i in p1:
        if i == " ":
            p1c.append(i)
        else:
            p1c.append(c1 + i)
    for i in p2:
        if i == " ":
            p2c.append(i)
        else:
            p2c.append(c2 + i)
    for i in p3:
        if i == " ":
            p3c.append(i)
        else:
            p3c.append(c3 + i)
    for i in p4:
        if i == " ":
            p4c.append(i)
        else:
            p4c.append(c2 + i)

    form = []
    for a,b,c,d, in itertools.zip_longest(p1c, p2c, p3c, p4c):
        if a:
            form.append(a)
        if b:
            form.append(b)
        if c:
            form.append(c)
        if d:
            form.append(d)

    return "".join(form)
    
#The colour codes go here into the function
print(alternating(text, "~L7", "~G2"))
#print(triplealternate(text, "~W9", "~W8", "~W7"))
