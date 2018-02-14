import re,sys
mycompile = lambda pat: re.compile(pat, re.UNICODE)
# SMILEY = mycompile(r'[:=].{0,1}[\)dpD]')
# MULTITOK_SMILEY = mycompile(r' : [\)dp]')

NormalEyes = r'[:=]'
Wink = r'[;]'

NoseArea = r'(|o|O|-)'  ## rather tight precision, \S might be reasonable...

HappyMouths = r'[D\)\]]'
SadMouths = r'[\(\[]'
Tongue = r'[pP]'
OtherMouths = r'[doO/\\]'  # remove forward slash if http://'s aren't cleaned

Happy_RE = mycompile('(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')')
Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)

Wink_RE = mycompile(Wink + NoseArea + HappyMouths)
Tongue_RE = mycompile(NormalEyes + NoseArea + Tongue)
Other_RE = mycompile('(' + NormalEyes + '|' + Wink + ')' + NoseArea + OtherMouths)

Emoticon = (
    "(" + NormalEyes + "|" + Wink + ")" +
    NoseArea +
    "(" + Tongue + "|" + OtherMouths + "|" + SadMouths + "|" + HappyMouths + ")"
)
Emoticon_RE = mycompile(Emoticon)


def analyze_tweet(text):
    h = Happy_RE.search(text)
    s = Sad_RE.search(text)
    w = Wink_RE.search(text)
    t = Tongue_RE.search(text)
    o= Other_RE.search(text)
    if h and s: return "BOTH_HS"
    if h: return "HAPPY"
    if s: return "SAD"
    if w: return "WINK"
    if t: return "TONGUE"
    if o: return "OTHER"
    return "NA"
