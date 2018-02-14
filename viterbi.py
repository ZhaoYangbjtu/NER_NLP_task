import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores (words -> labels), as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """

    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    emission = emission_scores.transpose() #made it LXN to suit my trellis table

    trellis = np.zeros(shape=(L, N))  # default to 0s

    par = np.zeros(shape=(L, N))

    for j in range(L):

        # print trellis[j][0]
        wp = emission[j][0]
        x= start_scores[j] + wp
        #max = -np.inf
        # r=0
        #for k in range(L):
            #x = start_scores[k] + wp
            #if (x > max):
                #max = x
                # r=k
        trellis[j][0] = x #max
        # par[j][0] = r
    # print trellis[j][0]

    y = []
    for i in range(1, N):
        best = -1000
        for k in range(L):
            wp = emission[k][i]
            max = -np.inf
            r = 0
            for j in range(L):  # for getting the maximum over all the labels
                x = trellis[j][i - 1] + wp + trans_scores[j][k]
                if (x > max):
                    max = x
                    r = j
            trellis[k][i] = max
            par[k][i] = r

            # if(trellis[k][i]>best):
            #     best = trellis[k][i]

            # y.append(best)

    # for j in range(L):
    #  print trellis[j][3]
    m = -np.inf
    p = 0
    for j in range(L):
        # print trellis[j][0]
        x = trellis[j][N - 1] + end_scores[j]
        if (x > m):
            m = x
            p = j

    #print m
    #print trellis
    # print y

    #print par

    # print p
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

    for i in range(1, N):
        t = y[i - 1]
        c = N - i
        z = int(par[t][c])
        y.append(z)

    # print y
    y.reverse()
    # print y
    # z = []
    # for i in range(N):
    #     z.append(trellis[y[i]][i])
        #print z[i]
    #print (m,z)
    #print trellis
    return (m, y)


    # y = []
    # for i in xrange(N):
    #     # stupid sequence
    #     y.append(i % L)
    # # score set to 0
    # return (0.0, y)
