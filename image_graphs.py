import numpy as np
import scipy.misc as sp
import copy
from min_cut import Graph



def im_to_graph(filename, sig_R, sig_W):
    #First, initialize matrix of the right size
    #im = sp.imread(filename, mode='RGB')

    im = [[[255, 255, 255],[255,255,255],[255,255,255]],
          [[0,0,0],[0,0,0],[255,255,255]],
          [[0,0,0],[0,0,0],[0,0,0]]]

    #Temporary testing setup (for the smiley face)
    # im = [[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [255, 255, 255]],
    #       [[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[255, 255, 255], [0,0,0],[0,0,0],[255, 255, 255], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[255, 255, 255],[255, 255, 255],[0,0,0], [0,0,0], [0,0,0], [0,0,0]]]

    adj_mat = np.zeros(((2 + len(im) * len(im[0])), (2 + len(im) * len(im[0]))))

    # Next add weights

    for i in range(len(im)):
        for j in range(len(im[0])):
            #v is current pixel values, r, g, b
            v = im[i][j]
            #Corresponding position in adj_mat: (i)*len(im[0]) + j (because its number of rows in the image * number of pixels in a row plus number of pixels through the current row)
            loc = (i)*len(im[0]) + j
            #print(v)

            #Assign weights for all adjacent vertices (if not already assigned), so thats from vertex (i,j) to (i+1,j), (i-1,j), (i,j+1), and (i,j-1)
            #Write to adj_mat[loc][loc_v2], adj_mat[loc_v2][loc], where loc_v2 is the same equation as loc but with new vertex values plugged in
            #equation: W_v1,v2 = e^(-((r(v1,v2)/sigma_R))) * e^(-((||w(v1)-w(v2)||^2)/(sigma_W)))

            #This part assigns weights by looking at adjacent pixels
            if i < len(im)-1: # Look one below
                p1 = np.exp(-(1/sig_R))
                p2 = -(np.linalg.norm((np.array(v)-np.array(im[i+1][j])))**2)/(sig_W) #Broken up for debugging, not necessary
                p3 = np.exp(p2)
                W1 = p1*p3

                #Other weight1 stuff
                loc1 = (i+1)*len(im[0]) + j

                if adj_mat[loc][loc1] == 0:
                    adj_mat[loc][loc1] = W1
                    adj_mat[loc1][loc] = W1


            if j < len(im[0]) - 1: #Look one to the right
                W2 = np.exp(-(1/sig_R))*np.exp(-(np.linalg.norm((np.array(v)-np.array(im[i][j+1])))**2)/(sig_W))
                #Other weight2 stuff
                loc3 = (i)*len(im[0]) + j+1

                if adj_mat[loc][loc3] == 0:
                    adj_mat[loc][loc3] = W2
                    adj_mat[loc3][loc] = W2

            #Assign a weight for (v, s) and (v, t), write to adj_mat[loc][-1], adj_mat[-1][loc] and adj_mat[loc][-2], adj_mat[-2][loc]
            #s equation: W_s,v1 = (p(w(v1)|v1 in s))/(p(w(v1|v1 in s))+p(w(v1)|v1 in t))
            #t equation:  W_t,v1 = (p(w(v1)|v1 in t))/(p(w(v1|v1 in s))+p(w(v1)|v1 in t))
            # From paper, p(v|SIGMA, mu) = sum(1/(sqrt(2pi|SIGMA_i|)) * e^(-0.5((v-mu_i)^T)*(SIGMA_i^-1) *(v-mu_i)))
            #For now, might just make s and t weights 0.5, so that cutting them is not incentivized or discouraged


            # Weighting things based on the assumption that things will be black and white

            if sum(v) >= (255*2): # If the pixel = white

                adj_mat[loc][-1] = 10000
                adj_mat[-1][loc] = 10000

                adj_mat[loc][-2] = 0.01
                adj_mat[-2][loc] = 0.01

            elif sum(v) <= (255):  # If the pixel = black

                adj_mat[loc][-1] = 0.01
                adj_mat[-1][loc] = 0.01

                adj_mat[loc][-2] = 10000
                adj_mat[-2][loc] = 10000

            # elif sum(v) <= (255) and sum(v) >= 0: # if the pixel = a color (but this is any color)
            #
            #     adj_mat[loc][-2] = 1000
            #     adj_mat[-2][loc] = 1000



    #Now just initialize the graph
    g = Graph(adj_mat=(adj_mat.tolist()))
    return g


def graph_to_im(graph, cut, image, file_extension=''):
    new_im_f = copy.deepcopy(image)
    new_im_b = copy.deepcopy(image)
    for i in range(len(cut[1])):
        if cut[1][i] == (-1, -1):
            pass
        else:
            edge = g.E[i]
            g.adj_mat[edge[0]][edge[1]] = 0
            g.adj_mat[edge[1]][edge[0]] = 0
    foreground = np.array(copy.deepcopy(g.adj_mat))
    background = np.array(copy.deepcopy(g.adj_mat))
    for i in range(len(foreground) - 2):
        if foreground[i][-2] == 0:
            foreground[i,:] = 0
            foreground[:,i] = 0
        if background[i][-1] == 0:
            background[i,:] = 0
            background[:,i] = 0

        x = i % len(im[0])
        y = i // len(im[0])
        if sum(foreground[i]) == 0:
            #print("Yeah!")
            new_im_f[y][x] = (255,0,0)

        if sum(background[i]) == 0:
            # print("Some red")
            new_im_b[y][x] = (255,0,0)

    sp.imsave('foreground' + file_extension + '.png', new_im_f)
    sp.imsave('background' + file_extension + '.png', new_im_b)

    # sp.imshow(foreground)
    # sp.imshow(background)


if __name__ == "__main__":
    # Create results file
    results_file = open("image_graph_test1.txt","w")
    #im = sp.imread(filename, mode='RGB')

    im = [[[255, 255, 255],[255,255,255],[255,255,255]],
          [[0,0,0],[0,0,0],[255,255,255]],
          [[0,0,0],[0,0,0],[0,0,0]]]
    g = im_to_graph(im, 10, 1000000)
    # im = [[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [0,0,0], [255, 255, 255]],
    #       [[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [0,0,0], [255, 255, 255], [0,0,0]],
    #       [[0,0,0],[0,0,0],[255, 255, 255],[0,0,0],[0,0,0],[0,0,0],[0,0,0], [255, 255, 255], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[255, 255, 255], [0,0,0],[0,0,0],[255, 255, 255], [0,0,0], [0,0,0], [0,0,0]],
    #       [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[255, 255, 255],[255, 255, 255],[0,0,0], [0,0,0], [0,0,0], [0,0,0]]]
    np.save("test_adj_mat.npy", np.array(g.adj_mat))

    print("Testing Karger Cut Algorithm.")
    for i in range(2):

        print("Graph initialized, iteration %s." % i)
        print(np.array(g.adj_mat))
        min_cut = g.Karger_cut()
        #min_cut = g.KargerStein()
        print(min_cut)
        results_file.write(str(min_cut) + "\n")
        graph_to_im(g, min_cut, im, str(i))

        #Use pre-saved graph (saves time, though...) for next iteration
        loaded_adj_mat = np.load("test_adj_mat.npy")
        g = Graph(adj_mat=loaded_adj_mat.tolist())


    # print("Testing Karger-Stein Cut Algorithm.")
    # for i in range(10):
    #     print("Graph initialized, iteration %s." % i)
    #
    #     print("Graph initialized.")
    #     print(np.array(g.adj_mat))
    #     #min_cut = g.Karger_cut()
    #     min_cut = g.KargerStein()
    #     print(min_cut)
    #     results_file.write(str(min_cut) + "\n")
    #
    #     #Re initatialize for the next iteration
    #     loaded_adj_mat = np.load("test_adj_mat.npy")
    #     g = Graph(adj_mat=loaded_adj_mat.tolist())

    results_file.close()
