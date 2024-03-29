import random
import math
import copy
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
                        self.W.append(0)

                        # Index through every edge using end cap vertices
                        self.W[-1] = self.adj_mat[i][j]
                        # for k in range(self.adj_mat[i][j]):
                        #     self.W[-1] += 1 # Adding 1 to every previous weight to make current


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
        h = Graph(adj_mat=self.adj_mat)
        #Now do the cut
        while len(h.adj_mat) > 2:    # While we haven't reached the condition of having two vertices
            edge = (-1,-1)           # Initialize edge to contracted edge condition
            while edge == (-1, -1):  # While contracted edge condition
                edge = (random.choice(h.E))  # Choose a random edge
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

    def StoerWagner(self):

        c = copy.deepcopy(self)

        vertexOrder = []
        iterateV = [vertexOrder.append(i) for i in range(0, len(c.adj_mat), 1)]

        contractedIndex = []
        A = [0]
        possible_A = 0
        accumulatePoint = 0

        contractedVertex = 0


        while len(A) < len(self.adj_mat) - 1:

            #First find most tightly connected
            largestIntersect = [0]
            for i in range(0, (len(c.adj_mat))):
                currentWeight = c.adj_mat[i][contractedVertex]
                if i != contractedVertex and currentWeight > largestIntersect[-1]:
                    largestIntersect.append(currentWeight)
                    possible_A = i;
            A.append(vertexOrder.index(possible_A))


            for i in range(0, (len(vertexOrder))):
                if i > A[-1] and vertexOrder[i] != 0:
                    vertexOrder[i] -= 1
                if i == A[-1]:
                    vertexOrder[i] = 0

            #Contract the edge
            print(A)
            edge = (0, possible_A)
            c.contract(edge)

        cutOfPhase = c.adj_mat[0][1]
        A.append(vertexOrder.index(1))
        return cutOfPhase, A






            ##
                # accumulatePoint = v1
                # contractedIndex.append(vertexOrder[v1])
                # contractedIndex.append(vertexOrder[v2])
                # vertexOrder.pop(v2)

            ##
                # contractedIndex.append(vertexOrder[v2])
                # vertexOrder.pop(v2)


    # def KargerStein(self):
    #    # Make copies to avoid changing original
    #    j = copy.deepcopy(self)
    #    k = copy.deepcopy(self)
    #    # Define n
    #    n_j = len(j.adj_mat)
    #    n_k = len(k.adj_mat)
    #    # Now contract edges
    #    while len(j.adj_mat) >= math.ceil((n_j/math.sqrt(2))):
    #        edge_j = (-1,-1)
    #        while edge_j == (-1,-1):
    #            edge_j = (random.choice(j.E))
    #        j.contract(edge_j)
    #    while len(k.adj_mat) >= math.ceil((n_k/math.sqrt(2))):
    #        edge_k = (-1,-1)
    #        while edge_k == (-1,-1)
    #            edge_k = (random.choice(k.E))
    #        k.contract(edge_k)
    #    # Initialize sums
    #    j_sum = 0
    #    k_sum = 0
    #    # Either count sum, or call Karger Stein recursively
    #    if len(j.adj_mat) == 2:
    #        for i in range(len(j.E)):
    #            if j.E[i] == (-1,-1):
    #                pass
    #            else:
    #                j_sum += 1
    #    elif 2 < len(j.adj_mat) < math.ceil((n_j/math.sqrt(2))+1):
    #        p = copy.deepcopy(j)
    #        j_sum = p.KargerStein()
    #    else:
    #        pass
    #    if len(k.adj_mat) == 2:
    #        for i in range(len(k.E)):
    #            if k.E[i] == (-1,-1):
    #                pass
    #            else:
    #                k_sum += 1
    #
    #    elif 2 < len(k.adj_mat) < math.ceil((n_j/math.sqrt(2))+1):
    #        q = copy.deepcopy(k)
    #        k_sum = q.KargerStein()
    #    else:
    #        pass
    #    # Return the smallest number of cuts
    #    if j_sum < k_sum:
    #        return j_sum
    #    else:
    #        return k_sum
    #

if __name__ == "__main__":
   test_mat = [[0, 3, 1, 5, 2],
               [3, 0, 0, 0, 4],
               [1, 0, 0, 4, 2],
               [5, 0, 4, 0, 2],
               [2, 4, 2, 2, 0]]
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
   print(g.StoerWagner())
   #print(g.KargerStein())
   # print(g.adj_mat)
   # print(g.E)

   # h = Graph(VE=VE_test)
   # print(h.adj_mat)
