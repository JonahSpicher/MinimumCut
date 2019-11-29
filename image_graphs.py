import numpy as np
import scipy.misc as sp
import copy
from first_pass import Graph



def im_to_graph(filename, sig_R, sig_W):
    #First, initialize matrix of the right size
    #im = sp.imread(filename, mode='RGB')

    #Temporary testing setup
    im = [[[0,0,0],[0,0,0],[0,0,0]],
         [[255,255,255],[0,0,0],[255,0,0]],
         [[255,255,255],[255,0,0],[255,0,0]]]
    adj_mat = np.zeros(((2 + len(im) * len(im[0])), (2 + len(im) * len(im[0]))))
    #print(len(adj_mat), len(adj_mat[0]))
    #print(adj_mat)

    # Next add weights I guess

    for i in range(len(im)):
        for j in range(len(im[0])):
            #v is current pixel values, r, g, b
            v = im[i][j]
            #Corresponding position in adj_mat: (i)*len(im[0]) + j (because its number of rows in the image * number of pixels in a row plus number of pixels through the current row)
            loc = (i)*len(im[0]) + j




            #Assign weights for all adjacent vertices (if not already assigned), so thats from vertex (i,j) to (i+1,j), (i-1,j), (i,j+1), and (i,j-1)
            #Write to adj_mat[loc][loc_v2], adj_mat[loc_v2][loc], where loc_v2 is the same equation as loc but with new vertex values plugged in
            #equation: W_v1,v2 = e^(-((r(v1,v2)/sigma_R))) * e^(-((||w(v1)-w(v2)||^2)/(sigma_W)))

            #This part assigns weights by looking at adjacent pixels
            if i < len(im)-1:
                W1 = np.exp(-(1/sig_R))*np.exp(-(np.linalg.norm((np.array(v)-np.array(im[i+1][j])))**2)/(sig_W))
                #Other weight1 stuff
                loc1 = (i+1)*len(im[0]) + j
                if adj_mat[loc][loc1] == 0:
                    adj_mat[loc][loc1] = W1
                    adj_mat[loc1][loc] = W1
            if i > 0:
                W2 = np.exp(-(1/sig_R))*np.exp(-(np.linalg.norm((np.array(v)-np.array(im[i-1][j])))**2)/(sig_W))
                #Other weight2 stuff
                loc2 = (i-1)*len(im[0]) + j
                if adj_mat[loc][loc2] == 0:
                    adj_mat[loc][loc2] = W2
                    adj_mat[loc2][loc] = W2
            if j < len(im[0]) - 1:
                W3 = np.exp(-(1/sig_R))*np.exp(-(np.linalg.norm((np.array(v)-np.array(im[i][j+1])))**2)/(sig_W))
                #Other weight3 stuff
                loc3 = (i)*len(im[0]) + j+1
                if adj_mat[loc][loc3] == 0:
                    adj_mat[loc][loc3] = W3
                    adj_mat[loc3][loc] = W3
            if j > 0:
                W4 = np.exp(-(1/sig_R))*np.exp(-(np.linalg.norm((np.array(v)-np.array(im[i][j-1])))**2)/(sig_W))
                #Other weight4 stuff
                loc4 = (i)*len(im[0]) + j-1
                if adj_mat[loc][loc4] == 0:
                    adj_mat[loc][loc4] = W4
                    adj_mat[loc4][loc] = W4

            #Assign a weight for (v, s) and (v, t), write to adj_mat[loc][-1], adj_mat[-1][loc] and adj_mat[loc][-2], adj_mat[-2][loc]
            #s equation: W_s,v1 = (p(w(v1)|v1 in s))/(p(w(v1|v1 in s))+p(w(v1)|v1 in t))
            #t equation:  W_t,v1 = (p(w(v1)|v1 in t))/(p(w(v1|v1 in s))+p(w(v1)|v1 in t))
            # From paper, p(v|SIGMA, mu) = sum(1/(sqrt(2pi|SIGMA_i|)) * e^(-0.5((v-mu_i)^T)*(SIGMA_i^-1) *(v-mu_i)))
            #For now, might just make s and t weights 0.5, so that cutting them is not incentivized or discouraged
            adj_mat[loc][-1] = 0.5
            adj_mat[-1][loc] = 0.5
            adj_mat[loc][-2] = 0.5
            adj_mat[-2][loc] = 0.5


    #Now just initialize the graph
    g = Graph(adj_mat=(adj_mat.tolist()))
    return g

if __name__ == "__main__":

    #Generate new graph
    g = im_to_graph("test.png", 1, 1)
    np.save("test_adj_mat.npy", np.array(g.adj_mat))

    #Use pre-saved graph (saves time, though...)
    # loaded_adj_mat = np.load("test_adj_mat.npy")
    # g = Graph(adj_mat=loaded_adj_mat.tolist())

    print("Graph initialized.")
    print(np.array(g.adj_mat))
    min_cut = g.Karger_cut()
    #min_cut = g.KargerStein()
    print(min_cut)
