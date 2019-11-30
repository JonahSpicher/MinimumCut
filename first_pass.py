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
                        self.W.append(0)                  # Add a 0 to W as a placeholder for the edge weight

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

    # In our interpretation self is the graph (G), a is the initial a value,
    # and w is the weights W


    # The goal of Stoer-Wagner: do all the cuts, when new_cut is less than best_cut, reset best_cut
        #return best_cut

    def minimumCutPhase(self, g):
    ## TODO: # Might have to look at the behavior for the first time step. It seems like from the paper that regardless of starting point,
    #          it winds up going to the tightest connected vertex immediately.

    # First let's initialize a new version of the adjacency matrix so we don't overwrite what we previously
    #established

        c = copy.deepcopy(g) # Commented out because I think this belongs in StoerWagner
        """ah, sort of. Stoer Wagner does this too, but this modifies the graph StoerWagner is using, so it needs to do it too."""

        # Initialize V (the number of vertices we're dealing with)
        # I also decided that this belonged in StoerWagner
        """Actually, this also belongs here, because there are two different relevant V's, the number of vertices in the full
        graph and the number currently being looked at"""

        # V = []
        # for i in range(0, len(c.adj_mat), 1):
        #     V.append(i)
        """We don't need this because you only use it to get its length, which we know already"""

        # Initialize A to a random vertex (or just to 0)

        #a = 0

        #A = [random.choice(V)]
        A = [0]

        #print('Edges Before', c.E)

        # Stoer Wagner runs as long as the number of values in A (length of A - 1, think spaces between sticks with sticks being the commas in the array)
        # and the number of values in V (V - 1 for the same reason) as well as when the length of the adjacency matrix is greater than or equal to three

        # Interestingly the length of the adjacency matrix being = to three is representative of there being only two vertices due to the way we set up
        # the adjacency matrix
        """Umm this is not true, if len(adj_mat) = 3 there are 3 vertices """


        """
        while (len(A) - 1) < (len(V) - 1) and len(c.adj_mat) >= 3: You dont need the >=3, thats a separate thing,
        and we actually want to stop when we have two vertices because its easier to check things then,
        so this should be:
        """
        while len(A) < len(g.adj_mat) - 1:


            # We set the current vertex to be the last value in A by putting the number of values in A in as the index

            currentVertex = A[len(A)- 1]

            # We then set up dummy variables that will later be used in the calculation

            intersectVertex = 0      # Represents a single value that will be the result of adding every value in the row
            largestIntersect = 0     # The largest value summed row value in the adjacency matrix
            tightestWithCurrent = 0  # Represents the vertex most tightly connected to the current vertex

            # We find the vertex most tightly connected with the current using the following for loop with if statements

            """I don't think this for loop does this, it gets whichever vertex is most tightly connected
            to the vertex added most recently to A (I think), but we want the one most tightly connected
            to any vertex in A. Probably the best way to do this is to contract an edge of C every time
            so that every vertex of g in A is just one vertex in c, but it gets hard (but not impossible)
            to keep track of vertices because they get renumbered."""
            for i in range(len(c.adj_mat)):                       # We index through all of the rows
                if i != currentVertex:                            # We skipping the row that represents the current vertex

                    intersectVertex = c.adj_mat[i][currentVertex] # We record the intersection between the currentVertex and all others as the value of each row
                                                                  # in the current vertex's column except the row that represents the current vertex

                if intersectVertex > largestIntersect:            # We see if the value representing the intersection with current vertex is larger than the previous
                    largestIntersect = intersectVertex            # If the value is larger we replace the current largest value with it
                    tightestWithCurrent = i                       # We record the index for the vertex most tightly connected as the current vertex

            # The next most tightly connected (to current) vertex will be the largest value in the current vertex column that isn't representative of the vertex itself

            # We add the most tightly connected vertex to the list A

            A.append(tightestWithCurrent)
            print('Next Tightest Vertex', tightestWithCurrent)
            print('Current A', A)

            # We set the index of the last value in A (-1 because it indexes from 0)

            currentIndex = len(A) - 1
            """In python you can do A[-1] to get the last element"""

            # We set the edge to be the edge between the current vertex and the one most tightly connected to the current vertex
            # The vertex most tightly connected to the current will be the last value of A and the current vertex will be the one before it

            edge = (A[currentIndex-1], A[currentIndex])
            """So this is equivalent to edge = (A[-2], A[-1]), which would also work, just so you know.
            But also, this is the wrong edge to contract. You want to contract the A vertex (which is 0),
            because you initialized A as [0] with the most recent one. So you should write
            edge = (A[0], A[-1])"""
            print("Edge", edge)

            # We contract the edge associated with the current vertex and the one most tightly connected to it
            currentContraction = c.contract(edge)

            print(len(c.adj_mat))
            print('adj_mat', c.adj_mat)
            print('New Edges', c.E)

        # We initialize the sum of the edges cut (the cut itself)

        sum = 0

        # Once all possible edges have been contracted, we index through the value, skipping the contracted edges and making a sum = to the cut

        # for i in range(len(c.E)):
        #     if c.E[i] == (-1, -1):
        #         pass
        #     else:
        #         cutOfPhase += 1
                #print(c.E[i])
                #print(sum)
        """There aren't any (-1,-1)'s here, because nothing has been cut. Things have been
        contracted though, so at this point, c has a 2x2 adjacency matrix, so all you have to do is this:"""
        cutOfPhase = c.adj_mat[0][1]
        """We want to return A becuase we need to know what partition this cutOfPhase corresponds to,
        the last two values of A are s and t, where t tells us what vertex (or vertices) we cut off
        and s and t together tell us what to contract in g."""
        return cutOfPhase, A


    def StoerWagner(self, cutOfPhase):

        # Set current minimum cut to something absurdly large so that the cutOfPhase results can replace it

        currentMinimumCut = 100
        best_partition = 0 """Need to find a way to describe partitions, see note below"""

        # Create a copy of the adjacency matrix so that we don't change the original
        """There is a hierarchy here where we dont touch self, we just try to find its minimum cut,
        g is the graph we contract as shown in the paper, and c is the graph we contract as shown in
        my notebook. That way they all stay safe, but we can make the edits we need to in order to
        learn things"""
        g = copy.deepcopy(self)

        # Re-creating the vertex array using method from minimumCutPhase

        # V = []
        # for i in range(0, len(c.adj_mat), 1):
        #     V.append(i)
        """Actually dont need this, we just need to count the vertices,
        don't have to keep track of them in any order or anything"""

        while len(g.adj_mat) > 1:
            cutOfPhase, final_A = self.minimumCutPhase(g)
            """I changed this a little to get the values minimumCutPhase returns"""

            if cutOfPhase < currentMinimumCut:
                currentMinimumCut = cutOfPhase
                best_partition = final_A[-1]
                """Need some logic here to figure out what partition in self
                this vertex of g corresponds to, like what it shows in the paper."""

            """Then we contract and go again on the smaller graph."""
            g.contract((final_A[-1], final_A[-2]))

        """Finally, just return the best value and what partition of self we got it from"""
        return currentMinimumCut, best_partition




    def KargerStein(self):
        # Make copies to avoid changing original
        j = copy.deepcopy(self)
        k = copy.deepcopy(self)
        # Define n
        n_j = len(j.adj_mat)
        n_k = len(k.adj_mat)
        # Now contract edges
        while len(j.adj_mat) >= math.ceil((n_j/math.sqrt(2))):
            edge_j = (-1,-1)
            while edge_j == (-1,-1):
                edge_j = (random.choice(j.E))
            j.contract(edge_j)
        while len(k.adj_mat) >= math.ceil((n_k/math.sqrt(2))):
            edge_k = (-1,-1)
            while edge_k == (-1,-1):
                edge_k = (random.choice(k.E))
            k.contract(edge_k)
        # Initialize sums
        j_sum = 0
        k_sum = 0
        # Either count sum, or call Karger Stein recursively
        if len(j.adj_mat) == 2:
            for i in range(len(j.E)):
                if j.E[i] == (-1,-1):
                    pass
                else:
                    j_sum += 1
        elif 2 < len(j.adj_mat) < math.ceil((n_j/math.sqrt(2))+1):
            p = copy.deepcopy(j)
            j_sum = p.KargerStein()
        else:
            pass
        if len(k.adj_mat) == 2:
            for i in range(len(k.E)):
                if k.E[i] == (-1,-1):
                    pass
                else:
                    k_sum += 1

        elif 2 < len(k.adj_mat) < math.ceil((n_j/math.sqrt(2))+1):
            q = copy.deepcopy(k)
            k_sum = q.KargerStein()
        else:
            pass
        # Return the smallest number of cuts
        if j_sum < k_sum:
            return j_sum
        else:
            return k_sum


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
    print(g.StoerWagner())
    #print(g.KargerStein())
    # print(g.adj_mat)
    # print(g.E)

    # h = Graph(VE=VE_test)
    # print(h.adj_mat)
