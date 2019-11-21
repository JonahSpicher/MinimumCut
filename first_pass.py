import random
# TODO: Stoer Wagner

class Graph: #Undirected, but can be a multigraph
    def __init__(self, VEW=None, adj_mat=None):
        #Format for VE initialization: V is number of vertices, E is list of edges: (v_i, v_j) connects v_i to v_j
        #So for example K_4 would be written (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
        if VEW == None and adj_mat == None:
            #empty graph
            self.adj_mat = [[0]]
            self.E = []
            self.W = []

        elif VEW == None:
            #initialize from an adjacency matrix, usually use this one
            self.adj_mat = adj_mat
            self.E = []
            self.W = []
            for i in range(len(self.adj_mat)):
                for j in range(i, len(self.adj_mat[i])):
                    if self.adj_mat[i][j] != 0:
                        self.E.append((i, j))
                        self.W.append(0)
                        for k in range(self.adj_mat[i][j]):
                            self.W[-1] += 1

        elif adj_mat == None:
            #initialize from a tuple of vertices and edges, maybe easier sometimes (its faster, if nothing else)
            self.E = VEW[1]
            self.W = VEW[2]
            self.adj_mat = []
            for i in range(VEW[0]):
                self.adj_mat.append([0]*VEW[0])
            print(self.adj_mat)
            for i in range(len(self.E)):
                #print("current edge:", self.E[i][0], self.E[i][1])
                self.adj_mat[self.E[i][0]][self.E[i][1]] += self.W[i]
                self.adj_mat[self.E[i][1]][self.E[i][0]] += self.W[i]
        else:
            #initialize from one, check with the other. If wrong, throw error
            self.adj_mat = adj_mat
            self.E = VEW[1]
            self.W = VEW[2]
            test_adj_mat = []
            for i in range(VEW[0]):
                test_adj_mat.append([0]*VEW[0])
            print(self.adj_mat)
            for i in range(len(self.E)):
                #print("current edge:", self.E[i][0], self.E[i][1])
                test_adj_mat[self.E[i][0]][self.E[i][1]] += self.W[i]
                test_adj_mat[self.E[i][1]][self.E[i][0]] += self.W[i]
            if test_adj_mat == self.adj_mat:
                print("Inputs matched, graph initialized.")
            else:
                print("Inputs mismatched, failed to initialize.")
                self.E = []
                self.adj_mat = [[0]]

    def add_lone_vertex(self):
        self.adj_mat.append([0]*(len(self.adj_mat) - 1))
        for row in self.adj_mat:
            row.append(0)

    def add_edge(self, v1, v2, num=1):
        self.adj_mat[v1][v2] += num
        self.adj_mat[v2][v1] += num
        for i in range(num):
            self.E.append((v1, v2))

    def add_vertex(self, vs, nums=None):
        #nums should be a list of the same length as vs, corresponding to number of edges
        if nums == None:
            nums = [1]*len(vs)
        self.add_lone_vertex()
        for i in range(len(vs)):
            self.add_edge(self.V[-1], vs[i], nums[i])

    def contract(self, edge):
        #edge is a tuple of the two connected vertices
        #Remembers edges using index in self.E
        if edge[0] < edge[1]:
            v1 = edge[0]
            v2 = edge[1]
        else:
            v1 = edge[1]
            v2 = edge[0]

        if (v1, v2) in self.E or (v2, v1) in self.E:
            temp = self.adj_mat.pop(v2)
            self.adj_mat[v1] = [sum(x) for x in zip(self.adj_mat[v1], temp)]
            for row in self.adj_mat:
                row_temp = row.pop(v2)
                row[v1] = row[v1] + row_temp
            self.adj_mat[v1][v1] = 0

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

    def Karger_cut(self):
        #First make a copy so the original isnt disturbed
        h = Graph(adj_mat=self.adj_mat)
        #Now do the cut
        while len(h.adj_mat) > 2:
            edge = (-1,-1)
            while edge == (-1, -1):
                edge = (random.choice(h.E))
            print("Contracting edge:", edge)
            h.contract(edge)

        #Display stuff
        sum = 0
        print("Edges to cut:")
        for i in range(len(h.E)):
            if h.E[i] == (-1, -1):
                pass
            else:
                sum += 1
                print(self.E[i])
        print("For a total of %s edges" % sum)
        return sum

    def StoerWagner(self):
        best_cut = 10000
        #do all the cuts, when new_cut is less than best_cut, reset best_cut
        #return best_cut
        h = Graph(adj_mat = self.adj_mat)

        summedRow = 0
        comparedRow = 0


        # Finding the biggest vertex

        ## Working on this: not quite normal code yet
        for i in range(len(self.adj_mat[0]))
            for j in range(len(self.adj_mat[0])):
                summedRow = summedRow + j
                if j == len(self.adj.append(j)_mat[0])
                   if summedRow > comparedRow
                      comparedRow = summedRow
                      summedRow = 0


        #####
        while len(h.adj_mat) > 2:
            edge = (-1,-1)
            while edge == (-1, -1):
                edge = (random.choice(h.E))
            print("Contracting edge:", edge)
            h.contract(edge)

        sum = 0
        print("Edges to cut:")
        for i in range(len(h.E)):
            if h.E[i] == (-1, -1):
                pass
            else:
                sum += 1
                print(self.E[i])
        print("For a total of %s edges" % sum)

        pass



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
    g.Karger_cut()
    # print(g.adj_mat)
    # print(g.E)

    # h = Graph(VE=VE_test)
    # print(h.adj_mat)
