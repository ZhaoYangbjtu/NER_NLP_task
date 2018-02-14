import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import emoticon

N =4
L=5
#print L,N
trellis = np.zeros(shape=(L,N)) #default to 0s

#transpose the given emission matrix because we need labels -> words ,ie, rows = labels
emission = np.array([[0,0.4,0.1,0],[0,0.1,0.9,0],[0.7,0,0,0],[0,0,0,1],[0,0,0,0.1]])
transition = np.array([[0.2,0.4,0.01,0.3,0.04],[0.3,0.05,0.3,0.2,0.1],[0.9,0.01,0.01,0.01,0.07],[0.4,0.05,0.4,0.1,0.05],[0.1,0.5,0.1,0.1,0.1]])

# print emission
# emission = emission.transpose()
# print emission

start=np.array([0.3,0.1,0.3,0.2,0.1])
end = np.array([0.05,0.05,0,0,0.1])

L = start.shape[0] #row
assert end.shape[0] == L
assert transition.shape[0] == L
assert transition.shape[1] == L
assert emission.shape[0] == L
N = emission.shape[1] #column

#print L,N
par = np.zeros(shape=(L,N))

for j in range(L):
 #print trellis[j][0]
 wp = emission[j][0]
 max = -1
 #r=0
 for k in range(L):
     x = start[k]*wp
     if(x>max):
         max =x
         #r=k
 trellis[j][0] = max
 #par[j][0] = r
# print trellis[j][0]

y=[]
for i in range(1,N):
    best =-1
    for k in range(L):
        wp = emission[k][i]
        max = -1
        r=0
        for j in range(L): # for getting the maximum over all the labels
          x = trellis[j][i-1] * wp * transition[j][k]
          if (x > max):
            max = x
            r=j
        trellis[k][i] = max
        par[k][i] = r

        # if(trellis[k][i]>best):
        #     best = trellis[k][i]

    # y.append(best)

# for j in range(L):
#  print trellis[j][3]
m =-1
p=0
for j in range(L):
 #print trellis[j][0]
 x=trellis[j][N-1]*end[j]
 if(x>m):
     m=x
     p=j

print m
print trellis
#print y

print par

#print p
y.append(p)

# z=int(par[p][N-1])
# print z
#
# d = int(par[z][N-2])
# print d
#
#
# o= int(par[d][N-3])
# print o

for i in range(1,N):
    t = y[i-1]
    c = N-i
    z = int(par[t][c])
    y.append(z)

#print y
y.reverse()
#print y
z = []
for i in range(N):
    z.append(trellis[y[i]][i])
    print z[i]

print (m,z)

w = "ab:cd"
if w[0].isupper():
    print "y"

w = "san"
x = set()
x.add("san jose")
x.add("san francisco")
if(w in x):
    print "present"

for k in x:
    if w in k:
        print "yes"

word = "pizza"
s = wn.synsets(word)
print "pizza"
print s
v = ["Synset('pizza.n.01')"]
print s[0].name().split('.')[0]
print str(s[0].hypernyms()[0].name().split('.')[0])

we = ":P"
print emoticon.analyze_tweet(we)

print set("a b".strip())

# word = nltk.word_tokenize(word)
# l=nltk.pos_tag(word)
# print str(l[0][1])

#
# for x in w:
#     if (x == ':'):
#         print "yes"










# print emission
# print emission.transpose()
#print transition
#print start
#print end
#print trellis

