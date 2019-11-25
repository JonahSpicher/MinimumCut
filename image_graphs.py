import numpy as np
import scipy.misc as sp
import copy



def im_to_graph(filename):
    #First, initialize matrix of the right size
    im = sp.imread(filename, mode='RGB')
    adj_mat = np.zeros(((2 + len(im) * len(im[0])), (2 + len(im) * len(im[0]))))
    print(len(adj_mat), len(adj_mat[0]))
    print(adj_mat)

    # Ne

im_to_graph("test.jpg")
