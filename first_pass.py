import random
import math
import copy
import numpy as np
# TODO: Stoer Wagner

class Graph: #Undirected, but can be a multigraph

    def __init__(self, VEW=None, adj_mat=[]):

        #Format for VE initialization: V is number of vertices, E is list of edges: (v_i, v_j) connects v_i to v_j
        #So for example K_4 would be written (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])

        if VEW == None and adj_mat == []: #If both the VEW matrix and adjacency matrix are empty
                                            #create an empty adjacency array, edge array, and weight array

           # Initialize the adjacency array as a blank array
            self.adj_mat = [[0]]

            # Initialize the edge and weight arrays as empty fields of class self
            self.E = []
            self.W = []

        elif VEW == None:
            # The following is if we initialize from an adjacency matrix (we'll usually use this one)
            # If only VEW is empty, accept the adjacency matrix

            self.adj_mat = adj_mat # Set the given adjacency matrix to be the adjacency matrix

            # Initialize the edge and weight arrays as fields of class

            self.E = []
            self.W = []

            # Index through every value in the adjacency matrix.

            for i in range(len(self.adj_mat)):            # Index through rows
                for j in range(i, len(self.adj_mat[i])):  # Index through columns

                    if self.adj_mat[i][j] != 0:           # If both i and j are not 0
                                                          # I and j represent end cap vertices of a particular edge

                        self.E.append((i, j))             # Add the vertex ends of the edge as a unit ot the E class
                        self.W.append(self.adj_mat[i][j])                  # Add a 0 to W as a placeholder for the edge weight



        elif adj_mat == None:

            # Alternate way to initialize: If you already have vertices and edges

            # If we have no adjacency matrix initialize from a tuple of vertices and edges,
            # maybe easier sometimes (its faster, if nothing else)

            self.E = VEW[1]    # Edges are second value in tuple (indexes from 0)
            self.W = VEW[2]    # Weights are 3rd value in tuple (indexes from 0)
            self.adj_mat = []  # Initialize blank adjacency array

            # Reminder: The 0th value in the tuple would be the number of vertices

            for i in range(VEW[0]):
                self.adj_mat.append([0]*VEW[0]) # Add a 0 for each vertex (placeholder)
            #print(self.adj_mat)

            # Index through the edges by indexing through the end cap vertices related
            # to the edge and using them to create edge weights

            for i in range(len(self.E)):
                #print("current edge:", self.E[i][0], self.E[i][1])
                self.adj_mat[self.E[i][0]][self.E[i][1]] += self.W[i]
                self.adj_mat[self.E[i][1]][self.E[i][0]] += self.W[i]

        else:

            # Saves given adjacency matrix as adjacency matrix.

            self.adj_mat = adj_mat

            # Generates a test matrix using the method described above.

            self.E = VEW[1]
            self.W = VEW[2]
            test_adj_mat = []
            for i in range(VEW[0]):
                test_adj_mat.append([0]*VEW[0])
            #print(self.adj_mat)
            for i in range(len(self.E)):
                #print("current edge:", self.E[i][0], self.E[i][1])

                # There are two of these because for every edge in the adjacency matrix,
                # there will be two relevant vertices.

                # For example: the edge made by vertex 1 and vertex 2 will be represented
                # by 2,1 and 1,2

                test_adj_mat[self.E[i][0]][self.E[i][1]] += self.W[i]
                test_adj_mat[self.E[i][1]][self.E[i][0]] += self.W[i]

            # Compares the two. If wrong, throws error.

            if test_adj_mat == self.adj_mat:
                print("Inputs matched, graph initialized.")
            else:
                print("Inputs mismatched, failed to initialize.")

                # Re-initialize edges and adjacency matrix in response to failed test
                self.E = []
                self.adj_mat = [[0]]


    def add_lone_vertex(self):
           # Add an additional row. Then add an additional 0 to each row.
           # Essentially it increases the column # and row # by 1.

        self.adj_mat.append([0]*(len(self.adj_mat) - 1)) ## Will this add an additional row?
        for row in self.adj_mat:
            row.append(0)


    def add_edge(self, v1, v2, num=1):
        # Index to the intersection between two vertices in the matrix and add
        # num to each place where the intersection occurs

        # Note: this is also accounting for the fact that there will be two places
        # in the adjacency matrix that represent a single edge.

        #Example: The edge that connects vertex 1 and vertex 2 is represented by (2,1) and (1,2)

        self.adj_mat[v1][v2] += num
        self.adj_mat[v2][v1] += num

        # Append the new vertex to the edge matrix

        for i in range(num):
            self.E.append((v1, v2))

    def add_vertex(self, vs, nums=None):
        # Adds vertices and corresponding connections to an existing adjacency matrix

        if nums == None:
            nums = [1]*len(vs)   # Make nums the same length as vs (which is the edge #)
        self.add_lone_vertex()   # Add a vertex
        for i in range(len(vs)): # Add edges that correspond with the vertex
            self.add_edge(self.V[-1], vs[i], nums[i])

    def contract(self, edge):
        # Edge is a tuple of the two connected vertices
        # Remembers edges using index in self.

        # Compare the vertices in the tuple (edge[0] and edge[1]). Assign the smaller to be
        # v1 and the larger to be v2
        # Edge is a tuple of the two connected vertices
        # Remembers edges using index in self.

        # Compare the vertices in the tuple (edge[0] and edge[1]). Assign the smaller to be
        # v1 and the larger to be v2

        if edge[0] < edge[1]:
            v1 = edge[0]
            v2 = edge[1]
        else:
            v1 = edge[1]
            v2 = edge[0]

        # If we are referring to either intersection between the two vertices within
        # the adjacency matrix

        if (v1, v2) in self.E or (v2, v1) in self.E:

            # Make a version of the matrix with v2 removed
            temp = self.adj_mat.pop(v2)

            # Create a matrix that is the sum of each value in v1 with each value in temp
            self.adj_mat[v1] = [sum(x) for x in zip(self.adj_mat[v1], temp)]

            # Index through matrix rows
            for row in self.adj_mat:
                row_temp = row.pop(v2) # Make something that represents a row in temp by removing v2 from each row
                row[v1] = row[v1] + row_temp # Add the v1 row to the row_Temp

            self.adj_mat[v1][v1] = 0  # Make the index (v1, v1) = 0

            for i in range(len(self.E)):
                #print("testing edge:")
                #print(self.E[i])
                if self.E[i] == (v1, v2) or self.E[i] == (v2, v1):
                    #print("Found contracted edge")
                    self.E[i] = (-1, -1)
                elif self.E[i][0] == v2:
                    #print("Found moved edge 0")
                    self.E[i] = (v1, self.E[i][1])
                elif self.E[i][1] == v2:
                    #print("Found moved edge 1")
                    self.E[i] = (self.E[i][0], v1)
                if self.E[i][0] > v2:
                    #print("Found renumbered edge 0")
                    self.E[i] = (self.E[i][0]-1, self.E[i][1])
                if self.E[i][1] > v2:
                    #print("Found renumbered edge 1")
                    self.E[i] = (self.E[i][0], self.E[i][1]-1)

        else:
            print("Edge not contained in graph.")

            pass

    def Karger_cut(self):
        #First make a copy so the original isnt disturbed
        h = copy.deepcopy(self)
        #Now do the cut
        while len(h.adj_mat) > 2:    # While we haven't reached the condition of having two vertices
            edge = (-1,-1)           # Initialize edge to contracted edge condition
            while edge == (-1, -1):  # While contracted edge condition
                w = np.array(h.W)
                w_norm = []
                for i in range(len(w)):
                    w_norm.append(float(float(w[i])/np.sum(w)))
                choice = (np.random.choice(len(h.E),p=w_norm))  # Choose a random edge
                edge = h.E[choice]
            #print("Contracting edge:", edge)
            h.contract(edge)                 # Contract it


        #Display stuff
        sum = 0
        #print("Edges to cut:")

        # Index through matrix. If the edge is contracted, skip it. If it's not, add to printed stuff
        # and display it.

        for i in range(len(h.E)):
            if h.E[i] == (-1, -1):
                pass
            else:
                sum += 1
                print(self.E[i])
        print("For a total of %s edges" % sum)
        return sum, h.E

    # The Stoer Wagner algorithm is based on the original paper on the subject
    # (link here: https://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf )

    # In our interpretation self is the graph (G), a is the initial a value,
    # and w is the weights W


    # The goal of Stoer-Wagner: do all the cuts, when new_cut is less than best_cut, reset best_cut
        #return best_cut

    def minimumCutPhase(self, g, V):

            # Make a copy of the g graph

            c = copy.deepcopy(g)

            # Initialize a blank array that will hold the contracted vertex at each step

            A = [0]

            # As the program looks for most itghtly connected vertex values,
            # it will store the output of each step here

            possible_A = 0

            # Stores where the contracted vertex is in the adjacency matrix

            contractedIndex = 0

            # While we've contracted everything except 1 vertex

            while len(A) < len(g.adj_mat) - 1: # The # of vertices = the length of the g adjacency matrix

                # Looks through all of the rows in the column associated with the contracted vertex A
                # in the adjacency matrix and finds the largest one (the one most tightly connected with the contracted vertex A)
                # and saves the vertex (which is represented by the row index i) as a possible represented of the vertex most tightly connected to A

                ## Note: Just to make sure that it does this correctly, we make sure that it skips the row representing the current A

                largestIntersect = [0]

                for i in range(0, (len(c.adj_mat))):
                    currentWeight = c.adj_mat[i][contractedIndex]
                    if i != contractedIndex and currentWeight > largestIntersect[-1]:
                        largestIntersect.append(currentWeight)
                        possible_A = i;

                # Add the possible_A that we get at the end of the loop (which should represent the most tightly connected vertex and therefore the next A)
                # But we do this after we go through a process of finding out where the new A is in an adjacency matrix where the contraction is represented

                A.append(vertexOrder.index(possible_A))

                # We use the vertexOrder array representing how the vertices are organized in the adjacency matrix as contractions occurs
                # First we set all of the indexs vertices that are higher in the order than the new A to be one less than their current value
                # Then we set the index in the vertex order that is = to the current A value to be the new contracted vertex, which is at vertexOrder column 0

                for i in range(0, (len(vertexOrder))):
                    if i > A[-1] and vertexOrder[i] != 0:
                        vertexOrder[i] -= 1
                    if i == A[-1]:
                        vertexOrder[i] = 0

                # The edge that is being contracted will always be between the contracted vertex (0) and the output for the most tightly connected vertex (possible A)
                edge = (0, possible_A)

                # Contract the edge that connects the contracted vertex and vertex that is most tightly connected to the contracted vertex
                c.contract(edge)

            # The final cut of phase will be between the two vertices that remain after everything but one vertex has been contracted
            cutOfPhase = c.adj_mat[0][1]

            # Append the remaining vertex in vertex order (which will be the single un-contracted vertex after everything else has been contracted) to A
            A.append(vertexOrder.index(1))

            # Output the cut of phase and A array
            return cutOfPhase, A


    def StoerWagner(self, cutOfPhase):

        # Set current minimum cut to something absurdly large so that the cutOfPhase results can replace it

        currentMinimumCut = 100

        # Create a copy of the adjacency matrix so that we don't change the original

        g = copy.deepcopy(self)

        # Re-creating the vertex array using method from minimumCutPhase

        V = []
        iterateV = [vertexOrder.append(i) for i in range(0, len(c.adj_mat), 1)]

        while len(g.adj_mat) > 1:
            cutOfPhase, final_A = self.minimumCutPhase(g)
            if cutOfPhase < currentMinimumCut:
                currentMinimumCut = cutOfPhase

            g.contract((final_A[-1], final_A[-2]))

        return currentMinimumCut




    # The Karger Stein algorithm is a recursive version of the Karger algorithm
    # with increased accuracy
    # Run the Karger algorithm until there are ceil((n/sqrt(2))+1) vertices remaining.
    # This gives a 50% chance that the contracted edges will lead to the minimum
    # cut, so we do this twice. Then, we run Karger again on the two partially
    # contracted graphs and continue doing this recursively until only two
    # vertices remain.
    def KargerStein(self):

        # Make copies to avoid changing original
        j = copy.deepcopy(self)
        k = copy.deepcopy(self)

        # Define n
        n_j = len(j.adj_mat)
        n_k = len(k.adj_mat)

        # When n <= 6, ceil((n/sqrt(2))+1) = n. So, if n <= 6, the limit will be
        # ceil((n/sqrt(2))) instead

        # Set j limit
        if n_j > 6:
            limit_j = math.ceil((n_j/math.sqrt(2))+1)
        else:
            limit_j = math.ceil((n_j/math.sqrt(2)))
        # Set k limit
        if n_k > 6:
            limit_k = math.ceil((n_k/math.sqrt(2))+1)
        else:
            limit_k = math.ceil((n_k/math.sqrt(2)))

        # Now contract edges until n < limit
        # J
        while len(j.adj_mat) >= limit_j:
            edge_j = (-1,-1)
            while edge_j == (-1,-1):
                w = np.array(j.W)
                w_norm = []
                for i in range(len(w)):
                    w_norm.append(float(float(w[i])/sum(w)))
                choice_j = (np.random.choice(len(j.E),p=w_norm))
                edge_j = j.E[choice_j]
            j.contract(edge_j)
        # K
        while len(k.adj_mat) >= limit_k:
            edge_k = (-1,-1)
            while edge_k == (-1,-1):
                w = np.array(k.W)
                w_norm = []
                for i in range(len(w)):
                    w_norm.append(float(float(w[i])/sum(w)))
                choice_k = (np.random.choice(len(k.E),p=w_norm))
                edge_k = k.E[choice_k]
            k.contract(edge_k)

        # Initialize sums
        j_sum = 0
        k_sum = 0

        # List where we will store the sum followed by self.E for each possible
        # minimum cut. At the end, the index of the smallest sum in this list
        # will be found, and the list self.E immediately following will be
        # returned along with the sume
        edge_list = []

        # If there are 2 vertices remaining, count sum and append sum and self.E
        # to edge_list.
        # if 2 < n < limit, make another copy of the graph, and call Karger Stein
        # on it
        # J
        if len(j.adj_mat) == 2:
            for i in range(len(j.E)):
                if j.E[i] == (-1,-1):
                    pass
                else:
                    j_sum += 1
            edge_list.append(j_sum)
            edge_list.append(j.E)
        elif 2 < len(j.adj_mat) < limit_j:
            p = copy.deepcopy(j)
            j_res = p.KargerStein()
            j_sum = j_res[0]
            j_E = j_res[1]
            edge_list.append(j_sum)
            edge_list.append(j_E)
        else:
            pass
        # K
        if len(k.adj_mat) == 2:
            for i in range(len(k.E)):
                if k.E[i] == (-1,-1):
                    pass
                else:
                    k_sum += 1
            edge_list.append(k_sum)
            edge_list.append(k.E)
        elif 2 < len(k.adj_mat) < limit_k:
            q = copy.deepcopy(k)
            k_res = q.KargerStein()
            k_sum = k_res[0]
            k_E = k_res[1]
            edge_list.append(k_sum)
            edge_list.append(k_E)
        else:
            pass

        # Return the smallest number of cuts and self.E
        if j_sum < k_sum:
            r = edge_list.index(j_sum)
            return j_sum, edge_list[r+1]
        else:
            s = edge_list.index(k_sum)
            return k_sum, edge_list[s+1]



if __name__ == "__main__":
    test_mat = [[0, 1, 1, 1, 1],
                [1, 0, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 0, 1],
                [1, 0, 1, 1, 0]]
    # test_mat = [[0, 2, 1],
    #             [2, 0, 0],
    #             [1, 0, 0]]
    # V = 9
    # E = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 7), (1, 2), (1, 4), (1, 8), (2, 4), (2, 5), (5, 4), (5, 8), (8, 4), (8, 7), (7, 4), ()]
    # V = 3
    # E = [(0, 1), (0, 2)]
    # W = [2, 1]
    g = Graph(adj_mat=test_mat)
    # print(g.E)
    # print(g.W)
    # print(g.adj_mat)
    # print(g.adj_mat)

    #print(g.adj_mat)
    #print(g.E)

    #g.contract((0,2))
    #g.Karger_cut()
    print(g.Karger_cut())
    #print(g.KargerStein())
    # print(g.adj_mat)
    # print(g.E)

    # h = Graph(VE=VE_test)
    # print(h.adj_mat)
