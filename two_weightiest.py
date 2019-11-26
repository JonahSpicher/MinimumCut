
# Substitute in for Stoer Wagner if appropriate

# TODO: Reesolve possible issue with the contracting process. I don't know if it's an error or just taking a
# long time to run.

def combineHighest(self):

   #best_cut = 10000

    #do all the cuts, when new_cut is less than best_cut, reset best_cut
    #return best_cut

    m = Graph(adj_mat = self.adj_mat)

    while len(m.adj_mat) > 2:    # While we haven't reached the condition of having two vertices
        edge = (-1,-1)           # Initialize edge to contracted edge condition

        #print(m.adj_mat)
        #Initialize variables

        summedRow = 0       # Represents a single value that will be the result of adding every value in the row
        comparedRow = 0     # The largest value summed row value in the adjacency matrix

        # Sum a row and compare it to a variable that stores the previous largest value

        for i in range(len(m.adj_mat)):                  # Index through all rows in self
            for j in range(len(m.adj_mat)):              # Index through all columns
                summedRow = summedRow + m.adj_mat[i][j]  # Summed row = each column value added to the previous
            if summedRow > comparedRow:                  # If the value for the whole row is larger than the previous value
                  comparedRow = summedRow                # It replaces the current largest value
                  comparedRow = i                        # Creating an index for the tightest row.
                  summedRow = 0                          # And we reset the variable that stores the summed row value.

        #Save the output of the previous for loop as the tightest vertex

        tightestVertex = comparedRow

        # A list that will contain all of the values except those associated with the tightest add_vertex

        notTightest = []

        for i in range(len(m.adj_mat)):                  # Index through all rows in self
            for j in range(len(m.adj_mat)):              # Index through all columns
                if i != comparedRow:                     # If the value is not associated with the tightest vertex row
                    notTightest.append(m.adj_mat[i][j])  # Add the value to the notTightest array
                else:
                    notTightest.append(0) # If it is the largest row, set it to 0 to preserve indexing


        # Set the side length to be the length of the graph matrix

        sideLength = len(m.adj_mat)

        # Rearrange the notTightest matrix to be the same structure as the adjacency matrix

        notFirstTightest = [notTightest[i:i+sideLength] for i in range(0, len(notTightest), sideLength)]
        #print(notFirstTightest)
        # Initialize variables

        summedRow2 = 0    # Represents a single value that will be the result of adding every value in the row
        comparedRow2 = 0  # The second largest summed row value in the adjacency matrix (because we removed the largest value row already)

        # Go through the same process as above, but for the adjacency matrix without the row representing the tightest add_vertex
        # Goal: find the second tightest vertex

        for i in range(len(notFirstTightest)):
            for j in range(len(notFirstTightest)):
                summedRow2 = summedRow2 + notFirstTightest[i][j]
            if summedRow2 > comparedRow2:
                  comparedRow2 = summedRow2
                  comparedRow2 = i
                  summedRow2 = 0

        # Save the output of the previous for loop as the second tightest vertex

        secondTightest = comparedRow2

        # Find the edge between the first and second tightest vertices

        edge = (tightestVertex, secondTightest)

        #print("Contracting edge:", edge)

        #contract the edge corresponding to the two tightest vertices in the adjacency matrices

        m.contract(edge)

    # Display the final cut as before
    sum = 0
    #print("Edges to cut:")
    for i in range(len(m.E)):
        if m.E[i] == (-1, -1):
            pass
        else:
            sum += 1
            #print(self.E[i])
    #print("For a total of %s edges" % sum)

    pass
