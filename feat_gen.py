#!/bin/python
import nltk
import codecs
import string
from nltk.corpus import wordnet as wn
# import emoticon

def preprocess_corpus(train_sents):
    """Use the sentences to do whatever preprocessing you think is suitable,
    such as counts, keeping track of rare features/words to remove, matches to lexicons,
    loading files, and so on. Avoid doing any of this in token2features, since
    that will be called on every token of every sentence.

    Of course, this is an optional function.

    Note that you can also call token2features here to aggregate feature counts, etc.
    """
    global first_name
    global last_name
    first_name = set(line.strip() for line in codecs.open('data\lexicon\\firstname.5k','r','utf-8'))
    last_name = set(line.strip() for line in codecs.open('data\lexicon\lastname.5000','r','utf-8'))


    global stop
    stop = set(line.strip() for line in codecs.open('data\lexicon\\english.stop','r','utf-8'))

    global loc
    global loc_country
    global venue

    # loc = set()
    # for line in open('data\lexicon\\location'):
    #     for x in (line.strip().split(" ")):
    #         loc.add(x)
    # for line in open('data\lexicon\\location.country'):
    #     for x in (line.strip().split(" ")):
    #         loc.add(x)
    # for line in open('data\lexicon\\transportation.road'):
    #     for x in (line.strip().split(" ")):
    #         loc.add(x)

    loc = set((line.strip()) for line in codecs.open('data\lexicon\\location','r','utf-8'))
    loc_country = set((line.strip()) for line in codecs.open('data\lexicon\location.country','r','utf-8'))
    venue = set((line.strip()) for line in codecs.open('data\lexicon\\transportation.road','r','utf-8'))


    global tv
    tv_net = set(line.strip() for line in codecs.open('data\lexicon\\tv.tv_network','r','utf-8'))
    tv_show = set(line.strip() for line in codecs.open('data\lexicon\\tv.tv_program','r','utf-8'))
    tv_channel = set(line.strip() for line in codecs.open('data\lexicon\\broadcast.tv_channel','r','utf-8'))
    tv = tv_net|tv_show|tv_channel

    global sports
    sport = set((line.strip()) for line in codecs.open('data\lexicon\\sports.sports_league','r','utf-8'))
    league = set((line.strip()) for line in codecs.open('data\lexicon\\sports.sports_team','r','utf-8'))
    sports = sport|league

    global products
    prod = set((line.strip()) for line in codecs.open('data\lexicon\\product','r','utf-8'))
    auto = set((line.strip()) for line in codecs.open('data\lexicon\\automotive.model','r','utf-8'))
    products = prod|auto

    global music
    music = set((line.strip()) for line in codecs.open('data\lexicon\\music.artists','r','utf-8'))

    pass

def token2features(sent, i, add_neighs = True):
    """Compute the features of a token.

    All the features are boolean, i.e. they appear or they do not. For the token,
    you have to return a set of strings that represent the features that *fire*
    for the token. See the code below.

    The token is at position i, and the rest of the sentence is provided as well.
    Try to make this efficient, since it is called on every token.

    One thing to note is that it is only called once per token, i.e. we do not call
    this function in the inner loops of training. So if your training is slow, it's
    not because of how long it's taking to run this code. That said, if your number
    of features is quite large, that will cause slowdowns for sure.

    add_neighs is a parameter that allows us to use this function itself in order to
    recursively add the same features, as computed for the neighbors. Of course, we do
    not want to recurse on the neighbors again, and then it is set to False (see code).
    """
    ftrs = []
    # bias
    ftrs.append("BIAS")
    # position features
    if i == 0:
        ftrs.append("SENT_BEGIN")
    if i == len(sent)-1:
        ftrs.append("SENT_END")

    # the word itself
    word = unicode(sent[i])
    ftrs.append("WORD=" + word)
    ftrs.append("LCASE=" + word.lower())
    # some features of the word
    if word.isalnum():
        ftrs.append("IS_ALNUM")
    if word.isnumeric():
        ftrs.append("IS_NUMERIC")
    if word.isdigit():
        ftrs.append("IS_DIGIT")
    if word.isupper():
        ftrs.append("IS_UPPER")
    # if word[0].isupper():
    #     ftrs.append("START_UPPER")
    if word.islower():
        ftrs.append("IS_LOWER")

    if word.lower() in stop:
        ftrs.append("IS_STOP")

    # if("Show" in word or "show" in word):
    #     ftrs.append("TV_SHOW")

    if(word[0]=='@' or word[0]=='#'):
        if(len(word)>1):
            word = word[1:]

    if(word in music):
        ftrs.append("MUSIC_ARTIST")

    # for x in word:
    #     if(x in string.punctuation):
    #         ftrs.append("IS_SPECIAL")

    # if(word[:4]=="http"):
    #     ftrs.append("IS_INTERNET")

    if word in first_name:
        ftrs.append("FIRST_NAME")
    elif word in last_name:
        ftrs.append("LAST_NAME")

    if(word in loc or word in loc_country or word in venue or "field" in word):
        ftrs.append("IS_LOC")

    if word in sports:
        ftrs.append("SPORTS")

    if word in products:
        ftrs.append("PROD")

    # if(word.lower() in loc):
    #     ftrs.append("IS_LOC")

    if(word in tv):
        ftrs.append("IS_TV")

    w = nltk.word_tokenize(word)
    l = nltk.pos_tag(w)
    if (len(l)>0):
     ftrs.append(str(l[0][1]))

    s = wn.synsets(word)
    if (len(s) > 0):
        try:
            c = s[0].hypernyms()
            if(len(c)>0):
                g= c[0].name().split('.')[0]
                ftrs.append(g)
        except Exception as inst:
            print(word," ",inst)

    def encode(char):
        if char.isupper():
            return 'X'
        elif char.islower():
            return 'x'
        elif char.isdigit():
            return 'd'
        else:
            return char

    def word_shapes(word):
        ws = ''
        if len(word) <= 4:
            for chr in word:
                if chr.isupper():
                    ws += 'X'
                elif chr.islower():
                    ws += 'x'
                elif chr.isdigit():
                    ws += 'd'
                else:
                    ws += chr
        else:
            for chr in word[:2]:
                if chr.isupper():
                    ws += 'X'
                elif chr.islower():
                    ws += 'x'
                elif chr.isdigit():
                    ws += 'd'
                else:
                    ws += chr
            for chr in word[2:-2]:
                char_encode = encode(chr)
                if char_encode in string.punctuation:
                    ws += char_encode
                elif char_encode != ws[-1]:
                    ws += char_encode
            for chr in word[-2:]:
                if chr.isupper():
                    ws += 'X'
                elif chr.islower():
                    ws += 'x'
                elif chr.isdigit():
                    ws += 'd'
                else:
                    ws += chr
        return ws

    ftrs.append(word_shapes(word))

    # e = emoticon.analyze_tweet(word)
    # if(e !="NA"):
    #     ftrs.append(e)



            # previous/next word feats
    if add_neighs:
        if i > 0:
            for pf in token2features(sent, i-1, add_neighs = False):
                ftrs.append("PREV_" + pf)
        if i < len(sent)-1:
            for pf in token2features(sent, i+1, add_neighs = False):
                ftrs.append("NEXT_" + pf)

    # return it!
    return ftrs

if __name__ == "__main__":
    sents = [
    [ "I", "love", "food" ]
    ]

    preprocess_corpus(sents)

    for sent in sents:
        for i in xrange(len(sent)):
            print sent[i], ":", token2features(sent, i)
