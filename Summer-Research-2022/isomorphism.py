# #! header needs to be updated post-new-step-5
# collection of functions used in checking isomorphism and processing matrices in order to check isomorphism
#
# to check, lattices are turned into their associated polygon vertex incidence matrix (pvim) and then manipulated and compared
# if they are equal, the lattices are isomorphic and we can get rid of one
# otherwise, the lattices are different figures and we should keep both
#
# these functions were moved out of lattice_generator.py to make things easier to read
#
# functions:
#   - isomorphism in list
#   - check isomorphism (for two individual pvims)
#   - process all matrices
#   - process matrix
#   - sort rows
#   - sort cols
#   - get row vector
#   - break row ties
#   - get col vector
#   - break col ties
#   - get groups
#   - get next group
#   - get max length
#   - sort group
#   - compare vectors
#   - both tied break
#   - get tied area
#   - find next leftmost true
#   - get col index as close as possible to leftmost true
#   - get row index vector
#   - check row index vectors

import collections

#local imports
from column_vector                      import ColumnVector
from polygon_vertex_incidence_matrix    import PolygonVertexIncidenceMatrix

class Isomorphism():

    #@------------------------------------@#
    #@----- Checking for isomorphism -----@#
    #@------------------------------------@#

    # checks to see if the target lattice is isomorphic to any lattice in a list of lattices
    # iterates through the list and checks the pvim resulting from that lattice against the target pvim
    #
    # lattices - a list of Lattices
    # target - a Lattice to be checked against the list of Lattices
    #
    # returns True if target is isomorphic to any lattice in lattices
    # returns False if no lattice in lattices is isomorphic to target
    @staticmethod
    def isomorph_in_list(lattices, target):
        #moved out of if statement in loop to save space
        target_pvim = PolygonVertexIncidenceMatrix(target._nodes_list)

        for item in lattices:
            if Isomorphism._check_isomorphism(PolygonVertexIncidenceMatrix(item._nodes_list), 
                                              target_pvim):
                return True

        return False

    # checks to see if two pvims are isomorphic (equaivalent after processing)
    # first checks to be sure the dimensions are the same, then processes each pvim and compares for equality
    #
    # pvim1 - a PolygonVertexIncidenceMatrix to be compared
    # pvim2 - a PolygonVertexIncidenceMatrix to be compared
    #
    # returns False if pvim1 and pvim2 are not the same size or not equivalent after processing
    # returns True if the matrices are the same after processing (represent the same figure)
    @staticmethod
    def _check_isomorphism(pvim1, pvim2):
        #check dimensions, no need to waste time processing if they aren't even the same size        
        if pvim1.dimensions() != pvim2.dimensions():
            return False
        
        #process pvim1
        pvim1 = Isomorphism._process_matrix(pvim1)

        #process pvim2
        pvim2 = Isomorphism._process_matrix(pvim2)

        #if equiv, return true
        if pvim1._matrix == pvim2._matrix:
            return True

        # otherwise, return False
        return False    

    #@-----------------------------@#
    #@----- Matrix Processing -----@#
    #@-----------------------------@#
    
    # takes a list of candidate pvims, processes each one and appends the processed pvim to a list
    # 
    # candidates - a list of PolygonVertexIncidenceMatrix objects
    #
    # returns a list of processed pvims.
    # if candidates is empty, returns an empty list
    @staticmethod
    def process_all_matrices(candidates):
        matrices = []

        for candidate in candidates:
            matrix = PolygonVertexIncidenceMatrix(candidate._nodes_list)
            matrix = Isomorphism._process_matrix(matrix)

            matrices.append(matrix)

        return matrices

    # processes a pvim in six steps, summarized below:
    #    1. sort rows in descending order of their row-sums
    #    2. sort cols in descending order of their col-sums
    #    3. break ties in the row-sum sort by sorting by row vectors, which contain the col-sum of every col for which the row is True 
    #        - can also be described as "a vector of the size of each polygon in which the vertex for that row is involved"
    #    4. break ties in the col-sum sort by sorting by col vectors, which contain the row-sum of every row the col is True
    #        - can also be described as " a vector of the number of shapes each vertex in the shape for this column is involved in"
    #    5. 
    #
    #    The step 5
    #    goal is to do a final col sort by similarity - a measure of how many shared True rows two cols have
    # 
    #     algorithm: changing :/
    #
    #    6. sort the rows once more by ascending row index vectors, which contain the col-index of each True in the row
    #        - can also be described as "a vector of the index of each shape the vertex for that row is involved in"
    #
    # it is important that all six steps happen
    # For order, 1 and 2 can be swapped but must happen before 3 and 4, which can be swapped,
    #            but must happen before 5 and 6, which cannot be swapped
    # If done out of order, the pvims for the same figure may appear different and you will retain redundant lattices
    #
    # pvim - a PolygonVertexIncidenceMatrix to be processed
    #
    # returns the processed pvim
    @staticmethod
    def _process_matrix(pvim):
        #print("Before Step 1 / Initial State")
        #print(pvim)

        # step 1: sort rows
        pvim = Isomorphism._sort_rows(pvim)

        #print("Post Step 1")
        #print(pvim)

        # step 2: sort cols
        pvim = Isomorphism._sort_cols(pvim)

        #print("Post Step 2")
        #print(pvim)

        # step 3: row tie-breaking
        # swap rows to be in order within their row vector length groups
        pvim = Isomorphism._break_row_ties(pvim)

        #print("Post Step 3")
        #print(pvim)

        # step 4: col tie-breaking
        # swap cols to be in order within their vertex_vector length groups
        pvim = Isomorphism._break_col_ties(pvim)

        #print("Post Step 4")
        #print(pvim)

        #step 5: 
        pvim = Isomorphism._similarity_col_sort(pvim)

        #print("Post Step 5")
        #print(pvim)

        #step 6: final fix of row order after columns have been set to final spots in step 5
        pvim = Isomorphism._check_row_index_vectors(pvim)

        #print("Post Step 6 / Final State")
        #print(pvim)

        return pvim

    #@------------------@#
    #@----- Step 1 -----@#
    #@------------------@#

    #step 1: sort rows by row sum, descending
    # uses built-in Python sorted()
    #
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the post-step-1 pvim
    @staticmethod
    def _sort_rows(pvim):
        # sorted is a built-in Python function
        pvim._matrix = sorted(pvim._matrix, key=sum, reverse=True)

        return pvim               

    #@------------------@#
    #@----- Step 2 -----@#
    #@------------------@#

    #step 2: sort cols in descending col_sum order
    # uses bubble sort. actual swaps done using col_swap function
    #
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the post-step-2 pvim
    @staticmethod
    def _sort_cols(pvim):
        # bubble sort
        n = len(pvim._matrix[0])

        # traverse the array from 0 to n-i-1,
        for i in range(n):
            for j in range(0, n-i-1):
                # swap adjacent elements if they are in decreasing order
                if pvim.col_sum(j) < pvim.col_sum(j+1):
                    pvim.col_swap(j, j+1)
        
        return pvim       
        
    #@------------------@#
    #@----- Step 3 -----@#
    #@------------------@#

    # get the row vector so we can use it when breaking row-sum ties in step 3
    # a row vector is a vector containing the sizes of each polygon that the row is a part of
    #
    # row - a list (a row) from the pvim matrix
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the vector associated with this row
    @staticmethod
    def _get_row_vector(row, pvim):
        poly_vector = []
        # go along the row and
        for i in range(len(row)):
            # if it is True,
            if row[i] is True:
                # add the size of the polygon (the col_sum) to the vector
                poly_vector.append(pvim.col_sum(i))

        return poly_vector

    # step 3: row tie-breaking
    # take the row vectors of each row and sort them (and their rows) in descending order
    # a row vector is a vector containing the sizes of each polygon that the row is a part of
    # 
    # Algorithm: Gather the vectors and their respective matrices into two lists.
    #            Loop through and isolate each group of vectors with the same size.
    #            Then, sort the vectors in descending order of their size, while sorting the matrices in parallel.
    # 
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the post-step-3 pvim
    #
    # this is ruining me (negative) but i think i need to add indices limits?
    # so when it swaps the things it does it in the middle if needed and not the beginning all the time
    # aaaaaa
    @staticmethod
    def _break_row_ties(pvim):
        #get row vectors
        row_vectors = []
        # while I'm getting row vectors, I'm also tying them to the rows
        # they match with for sorting after this loop
        pairs = []
        for row in pvim._matrix:
            single_row_vector = Isomorphism._get_row_vector(row, pvim)
            row_vectors.append(single_row_vector)
            pairs.append([single_row_vector, row])
        
        #print(row_vectors)
        #print(pairs)


        #pairs = sorted(sorted(pairs, key = lambda pair: len(pair[0]), reverse = True), key = lambda pair: pair[0], reverse = True) 
        # sort by length of row vectors and by values
        # sort is stable, which is why this works
        # i fucking cried over this and all i had to do was reverse the sort order 
        # yay coding
        pairs.sort(key = lambda pair: pair[0], reverse = True)
        pairs.sort(key = lambda pair: len(pair[0]), reverse = True)
        #print(pairs)

        # sort by values in row vectors
        #pairs.sort(key = lambda pair: pair[0], reverse = True)
        #print(pairs)

        # extract the now-sorted rows
        rows = []
        for pair in pairs:
            rows.append(pair[1])
        #print(rows)
        
        pvim._matrix = rows

        return pvim

    #@------------------@#
    #@----- Step 4 -----@#
    #@------------------@#
    
    # get the column vectors so we can break col sum ties in step 4
    # a column vector is the row sums of the rows that contain a True in that column
    #
    # col_index - int index of the column you want the vector for
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns a ColumnVector that has the row sums of the rows that are True for the col at col_index
    @staticmethod
    def _get_col_vector(col_index, pvim):
        vector = ColumnVector([], col_index)
        
        # for each row, if the cell at col_index is True, add the row sum to the vector
        for i in range(len(pvim._matrix)):
            if pvim._matrix[i][col_index] is True:
                vector._vector.append(pvim.row_sum(i))
        
        return vector

    # step 4: col tie-breaking
    # this means that we take the column vectors of each column and sort them in descending order
    # a column vector is the row sums of the rows that contain a True in that column
    #
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the post-step-4 pvim
    @staticmethod
    def _break_col_ties(pvim):
        # get the column vectors in a list of ColumnVector objects
        column_vectors = []
        for i in range(len(pvim._matrix[0])):
            column_vectors.append(Isomorphism._get_col_vector(i, pvim))

        # get groups, then sort each group lexicographically with sort_group
        groups = Isomorphism._get_groups(column_vectors)
        for group in groups:
            Isomorphism._sort_group(group, pvim)

        return pvim

    
    # get groups of col vectors
    # to be a group, the vectors must all have the same length
    #
    # column_vectors - a list of ColumnVector objects
    #
    # returns a list of groups, each group being a list of ColumnVector objects
    # [ [CV,CV,CV] , [CV,CV] , [CV,CV,CV] ] 
    @staticmethod
    def _get_groups(column_vectors):
        groups = []
        # go through column_vectors
        while column_vectors:
            # find the length of the largest vector
            max_length = Isomorphism._get_max_length(column_vectors)

            # get the group of vectors with the max length and add to groups
            group = Isomorphism._get_next_group(column_vectors, max_length)
            groups.append(group)
            
            # reset column_vectors to no longer include CVs already in a group
            column_vectors = [x for x in column_vectors if x not in group]

        return groups
    
    # get the group of ColumnVectors with the specific length (max_length)
    # we don't need to check if the max length does not exist in the list because
    # we will already have gotten the right max_length in _get_groups()
    #
    # column_vectors - a list of ColumnVector objects to look in for the group we want
    # max_length - int, the length of the group we are looking for.
    #
    # returns the list of ColumnVectors that have length max_length
    @staticmethod
    def _get_next_group(column_vectors, max_length):
        
        group = []
        for vector in column_vectors:
            # collect all the ColumnVectors with length max_length
            if len(vector._vector) == max_length:
                group.append(vector)

        return group   
        
    # Finds the length of the longest vector in the list passed in
    #
    # column_vectors - a list of ColumnVector objects
    #
    # returns the length of the longest vector
    @staticmethod
    def _get_max_length(column_vectors):
        # set max_length to a length -> length of the first vector in the list
        max_length = len(column_vectors[0]._vector)

        # go through the list
        for i in range(1, len(column_vectors)):
            # if the length of the current vector is longer than the max_length, set max_length to that length
            if len(column_vectors[i]._vector) > max_length:
                max_length = len(column_vectors[i]._vector)

        return max_length

    # Bubble sort the individual vectors in the group, descending by value
    # vectors get sorted in length groups by comparing the first entries' value
    # if it is a tie, continue to the next entry in each until tie is resolved or you reach end of vector
    #
    # group - list of ColumnVector objects
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the newly sorted pvim (keep in mind only one group has been sorted)
    @staticmethod
    def _sort_group(group, pvim):
        n = len(group)
        # for each vector in the group
        for i in range(n): 
            # range excludes already traversed elements and the last element
            for j in range(0, n-i-1): 
                # compare next and this
                if Isomorphism._compare_vectors(group[j+1], group[j]):
                    vector_index_0 = group[j]._index
                    vector_index_1 = group[j+1]._index

                    group[j], group[j+1] = group[j+1], group[j]
                    pvim.col_swap(vector_index_0, vector_index_1)

                    # swap vector object indices
                    group[j]._index, group[j+1]._index = group[j+1]._index, group[j]._index

        return pvim

    # returns true if vector_u is greater than vector_v
    # vectors get sorted by comparing the first entry values
    # if it is a tie, continue to the next entry in each until tie is resolved or you reach end of vector
    #
    # vector_u - a ColumnVector object to be compared
    # vector_v - a ColumnVector object to be compared
    #
    # returns True if vector_u is greater than vector_v
    # returns False if vector_v is greater than vector_u
    #
    # throws exception if vector_u is not a ColumnVector object
    # throws exception if vector_v is not a ColumnVector object
    # throws exception if vector_u and vector_v are not the same length (meaning they are not in the same group)
    @staticmethod
    def _compare_vectors(vector_u, vector_v):

        if not isinstance(vector_u, ColumnVector):
            raise TypeError("vector_u must be a ColumnVector object")

        if not isinstance(vector_v, ColumnVector):
            raise TypeError("vector_v must be a ColumnVector object")

        if not len(vector_u._vector) == len(vector_v._vector):
            raise ValueError("vector_u and vector_v must be the same length")

        # if greater doesn't change, then the vectors are the same
        for i in range(len(vector_u._vector)):
            # leave as soon as you decide one is greater, don't keep looking at the other entries
            if vector_u._vector[i] > vector_v._vector[i]:
                return True
            elif vector_u._vector[i] < vector_v._vector[i]:
                break

        return False

    #@------------------@#
    #@----- Step 5 -----@#
    #@------------------@#

    # The step 5
    # goal is to do a final col sort by similarity - a measure of how many shared True rows two cols have
    # 
    # algorithm:
    #    begin at third-to-last col, the furthest right col that may require movement of right-from-there cols
    #    get the similarity vector, which contains similarity values for every column to the right of the active column
    #    sort the sim vector in descending order, dragging the associated columns along in that sort
    #       uses bubble sort
    #    move active col one cal to the left and repeat
    #
    #
    # 1/12 step five updates
    #    move back to left-right processing
    #    restrict consideration to columns that are both tied by shape size (col sum)
    #        and tied by column vector (vector of the number of shapes each vertex involved in this shape is a member of)
    #        (vector of the row-sums for which this column has a True)
    #    similarity vector stuff remains the same
    #
    # 
    # pvim - PolygonVertexIncidenceMatrix object to be sorted
    #
    # returns sorted PolygonVertexIncidenceMatrix


    # needs to be tested
    # takes a pvim, calculates the column sums for every column,
    # then calls out to helpers to get the indices (inclusive) of ties
    #
    # returns groups, a list of lists, each of length 2 and containing the start and end (inclusive) indices for ties
    @staticmethod
    def _get_col_sum_ties(pvim):

        # id tied areas - needs to be tied by col sum and column vector
        # get col sums
        col_sums = []
        for i in range(0, pvim.dimensions()[1]):
            col_sums.append(pvim.col_sum(i))
            
        # id groups of tied col sums
        return Isomorphism._col_sum_get_groups(col_sums)

    # needs to be tested
    # need to take in pvim also to get column vectors
    # looks in each group of tied by col sum to check if it contains a tie by col vector
    # no need to check if the tie is less than three columns because that would not result in any movement
    # get the col vector for every col in the col-sum-tie, then get the tied groups of those
    # collect the indices (inclusive) of those groups into a list of lists and return that
    #
    # returns groups, a list of lists, each of length 2 and containing the start and end (inclusive)
    # indices where the matrix is tied by col vector
    @staticmethod
    def _get_col_vector_ties(col_sum_groups, pvim):
        ties = []
        #looking for tied col vectors within the tied col sum areas
        for group in col_sum_groups:
            # if group covers more than 2 columns (otherwise no need to move things)
            if group[1] - group[0] >= 2:
                column_vectors = []
                for i in range(group[0], group[1] + 1):
                    column_vectors.append(Isomorphism._get_col_vector(i, pvim))
                column_vector_groups = Isomorphism._get_groups(column_vectors)
                for col_vector_group in column_vector_groups:
                    # get the index of the first column in group and the index of the last index in group
                    ties.append([col_vector_group[0].get_index(), col_vector_group[len(col_vector_group) - 1].get_index()])
        return ties

    # # needs to be tested
    # @staticmethod
    # def _similarity_col_sort_manager(pvim):
    #     # print("welcome to sim col sort manager")
    #     col_sum_groups = Isomorphism._get_col_sum_ties(pvim)
    #     # print(col_sum_groups)
    #     ties = Isomorphism._get_col_vector_ties(col_sum_groups, pvim)
    #     # print(ties)
    #     # ties is a list of lists of length 2 containing the
    #     # start and end indices (inclusive) to consider for step 5 movement
    #     # call out to step 5 movement if ties are large enough
    #     for iSet in ties:
    #         # print(iSet)
    #         # print("leaving to sim col sort")
    #         pvim = Isomorphism._similarity_col_sort(iSet[0], iSet[1], pvim)
    #     return pvim

    # needs to be tested
    @staticmethod
    def _similarity_col_sort(pvim):

        # get groups
        col_sum_groups = Isomorphism._get_col_sum_ties(pvim)
        tied_groups = Isomorphism._get_col_vector_ties(col_sum_groups, pvim)
        # put all indices not included in a tied group in s
        s = []
        #TODO: id and add the columns not in a group
        
        # continue until either 1) all columns are in S or 2) no more changes produced
        moved_in_last = True # for tracking if changes occured. needs to start as True so loop starts
        while len(s) != pvim.dimensions[1] and moved_in_last==True:
            # by group,
            for group in tied_groups:
                sim_vectors = []
                colI = group[0]
                while colI <= group[1]:
                    sim_vectors.append(Isomorphism._get_similarity_vector(colI, pvim, s))
                # do the sort
                s.extend(Isomorphism._step_5_sort(group[0], pvim, sim_vectors))
        return pvim

    # returns list of indices to add to s
    @staticmethod    
    def _step_5_sort(start_i, pvim, sim_vectors):
        sorted_is = []
        # now a list of tuples, the pvim index and the sim_vector
        sims_e = enumerate(sim_vectors, start = start_i)

        # sort cols in group by sim vector
        # selection sort
        # i need all this crazy +start_i and -start_i because i'm working in
        # the middle of the matrix but the beginning of the sim_vector list
        # prob a better way to do it though
        # over the indexes of the group,
        for i in range(start_i, start_i + len(sims_e) - 1):   
            max_idx = i
            for j in range(i+1-start_i, len(sims_e)):
                if sims_e[j][1] > sims_e[max_idx - start_i][1]:
                    max_idx = j + start_i
            sims_e[i-start_i], sims_e[max_idx-start_i] = sims_e[max_idx-start_i], sims_e[i-start_i]
            pvim.col_swap(i, max_idx)

            # TODO: this would add all of the indexes i think but i only want the ones in their final place
            # TODO: force cols to be in s in their final place
            # move whatever has been sorted to s
            # until told otherwise, i will add the index of the larger column first
            sorted_is.append(max_idx)

        # set?
        return sorted_is

        # # start with the third-to-last column as a default
        # # no need to handle the last or penult. because no order change necessary
        # active_col = start_index #0 #pvim.dimensions()[1] - 1 - 2

        # # tracks sim vector and index
        # sim_vectors = []

        # # while the col you are looking at is not beyond the current col,
        # while active_col <= end_index: #pvim.dimensions()[1] - 1 - 2: # 0:

        #     # get the similarity vector
        #     sim_vectors.append([Isomorphism._get_similarity_vector(active_col, end_index, pvim), active_col])
        #     # print("before:")
        #     # print(sim_vector)
        #     # print(pvim)

        #     # sort the remaining columns and the similarity vector in parallel
        #     # (basically, step 2 again but with a different vector)
        #     # bubble sort the values in the similarity vector descending, and
        #     # do the matching swaps to the columns
        #     # bubble sort (Copilot code, thanks copilot)
        #     # n = len(sim_vector)
        #     # for i in range(n):
        #     #     for j in range(0, n-i-1):
        #     #         if sim_vector[j+1] > sim_vector[j]:
        #     #             sim_vector[j], sim_vector[j + 1] = sim_vector[j + 1], sim_vector[j]
        #     #             pvim.col_swap(active_col + 1 + j, active_col + 1 + j + 1)
        #     # print("after:")
        #     # print(sim_vector)
        #     # print(pvim)
        #     #repeat for every column remaining to the right
        #     active_col = active_col + 1
        
        # # sort sim_vectors?

        # # move cols by sim vectors
        # n = len(sim_vectors)
        # for i in range(n):
        #     for j in range(0, n-i-1):
        #         if sim_vectors[j+1][0] > sim_vectors[j][0]:
        #             sim_vectors[j], sim_vectors[j + 1] = sim_vectors[j + 1], sim_vectors[j]
        #             pvim.col_swap(sim_vectors[j][1], sim_vectors[j+1][1])
        #             #pvim.col_swap(active_col + 1 + j, active_col + 1 + j + 1)

        # return pvim

    # passed
    # helper for restricting step 5 working area
    # identifies groups of col-sum ties
    # modeled closely off of step 4 get_groups
    #
    # returns groups, a list of lists, each of length 2 and containing the start and end (inclusive) indices for ties
    @staticmethod
    def _col_sum_get_groups(col_sums):
        groups = []
        start_index = 0

        while start_index < len(col_sums):
            end_index = Isomorphism._col_sum_get_next_group(start_index, col_sums)
            groups.append([start_index, end_index])
            start_index = end_index + 1

        return groups

    # passed
    # helper for _col_sum_get_groups
    # given an index, get the group of col_sums that match the value at that index
    # identifies a group of tied col sums by index
    # modeled closely after step 4 get_next_group
    #
    # returns end index of group inclusive
    @staticmethod
    def _col_sum_get_next_group(index, col_sums):
        # value to form group of
        value = col_sums[index]

        # move through col sums
        while index < len(col_sums):
            # if sum no longer matches value, you have left the group
            # return previous index
            if col_sums[index] != value: return index - 1

            #increment
            index = index + 1

        # end is reached, this group extends to the end of the list
        return len(col_sums) - 1

    # get the similarity vector of one column as compared to the columns in set S
    #
    # a similarity vector is how many of the column's rows are both true
    # ex.    True  True    the first col has a similarity vector of [2] because the cols share two True rows
    #        True  True    
    #        False True
    #        True  False
    #
    # ex. comparing col 1 to 2 and 3
    #        True, True, False        first col has [2, 1] because both are true on the first and second rows in cols 1 and 2                                                      
    #        True, True, False                             and cols 1 and 3 are only both true on row 2
    #        True, False, True
    #        False, True, False
    #        False, False, True
    #        False, False, True
    #
    # process: get the col_index_vector for col (the row indices where this column is True)        
    #          for each column in S,
    #                  get the col_index_vector
    #                  sum how many of the same values the two vectors have and append that to the similarity vector
    #
    # col - the column index to get the similarity vector for
    # pvim - a PolygonVertexIncidenceMatrix
    # s - set of the indicies of the sorted columns
    #
    # returns a list of similarity values (ints)
    # returns [] if no similarities or no remaining columns to be similar to
    @staticmethod                  # thats inclusive of group
    def _get_similarity_vector(col, pvim, s):
        sim_vector = []

        # get the row-indices of each true for this column
        col_indices = Isomorphism._get_col_index_vector(col, pvim)

        # for every column in S,
        for index in s:
            sum = 0
            # add up how many of the Trues in the two columns are on the same row
            # you can probably improve the efficiency of this with set cast
            # (get the indexes of each True in that col, 
            other_col_indices = Isomorphism._get_col_index_vector(index, pvim)
            for item in col_indices:
                # check each and add one to a sum if they match,
                if item in other_col_indices:
                    sum = sum + 1
            # add the sum to the sim vector)
            sim_vector.append(sum)
            index = index - 1 #+ 1    

        return sim_vector

    # # get the col index vector for the column at col
    # # a col index vector is a list of the row indices where the column is True
    # #
    # # col - the column index to get the col index vector for
    # # pvim - a PolygonVertexIncidenceMatrix
    # #
    # # returns a list of row indices where the column is True
    # @staticmethod
    # def _get_col_index_vector(col, pvim): #@ passed
    #     col_index_vector = []

    #     for i in range(0, len(pvim._matrix)):
    #         # for every True in the column, add the index to the col_index_vector
    #         if pvim._matrix[i][col]:
    #             col_index_vector.append(i)

    #     return col_index_vector

    # # get the groups of the same values in a similarity vector
    # # we need the groups so we can identify where we need to break ties in sort_sim_group
    # # expects a sorted sim_vector
    # # same code as in step 4
    
    # # sim_vector - a list of similarity values you want the groups from, sorted
    
    # # returns a list of groups, each group being a list of indexes where the values are the same in the sim_vector
    # @staticmethod
    # def _get_sim_groups(sim_vector):   #@ passed
    #     groups = []
    #     start_index = 0

    #     while start_index < len(sim_vector):
    #         group = Isomorphism._get_next_sim_group(start_index, sim_vector, sim_vector[start_index])
    #         groups.append(group)

    #         start_index = group[-1] + 1

    #     return groups

    # # helper for get sim group
    # # gets the next group to be added to the list of groups in get sim groups
    # # a group has the same values in the sim_vector
    # # expects a sorted sim_vector
    # # same code as in step 4
    # #
    # # start - the index to start from in the sim_vector (so we exclude what is already part of a group)
    # # sim_vector - the list of similarity values to be grouped, sorted
    # # target - int, the value to identify this group by
    # #
    # # returns the sim_vector indexes of the grouped elements
    # # if at end of sim vector, returns []
    # @staticmethod
    # def _get_next_sim_group(start, sim_vector, target): #@ passed
    #     group = []
    #     for i in range(start, len(sim_vector)):
    #         if sim_vector[i] == target:
    #             group.append(i)
    #     return group

    # # break ties by the most-top-most True
    # # in groups where the similarity vector values are the same,
    # # the group gets sorted by which col has the top-most True
    # # same code as in step 4
    # #
    # # start_to_sort - the index to start from in the matrix (the one next to the col whose sim vector you are looking at)
    # # pvim - a PolygonVertexIncidenceMatrix
    # # group - a list of indexes where the values are the same in the sim_vector
    # #
    # # returns the pvim after ONE group has been sorted
    # @staticmethod
    # def _sort_sim_group(start_to_sort, pvim, group):
    #     # bubble sort
    #     #print("length of group")
    #     n = len(group)
    #     #print(n)
    #     for i in range(n):
    #         for j in range(0, n-i-1):
    #             if Isomorphism._get_col_index_vector(start_to_sort + group[j], pvim) > Isomorphism._get_col_index_vector(start_to_sort + group[j + 1], pvim):
    #                 group[j], group[j + 1] = group[j + 1], group[j]
    #                 pvim.col_swap(start_to_sort + group[j], start_to_sort + group[j + 1])
       
    #     return pvim

    #@------------------@#
    #@----- Step 6 -----@#
    #@------------------@#
    
    # get new step 6 row index vectors containing the indices where this row is True
    # (not the old row vectors where it was the col sums!)
    # a row index vector is a list of the indices of the True cols in this row
    #
    # row - a list of booleans representing one row from a PolygonVertexIncidenceMatrix
    #
    # returns a row index vector
    @staticmethod
    def _get_row_index_vector(row):
        index_vector = []                                             
        for i in range(len(row)):
            # for every True in this row, append the index to the index_vector
            if row[i]:
                index_vector.append(i)     

        return index_vector
    
    # step 6: sort the rows once more by ascending row index vectors, which contain the col-index of each True in the row
    #                 - can also be described as "a vector of the index of each shape the vertex for that row is involved in"
    #
    # uses the same logic as step 3: 
    #     Gather the row index vectors and their matrices into two lists.
    #     Loop through and isolate each group of vectors with the same size.
    #     Then, sort the vectors in descending order of their size, while sorting the matrices in parallel.
    #
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns the post-step-six pvim
    @staticmethod
    def _check_row_index_vectors(pvim):
        #get row vectors
        row_index_vectors = []
        # while I'm getting row vectors, I'm also tying them to the rows
        # they match with for sorting after this loop
        pairs = []
        for row in pvim._matrix:
            single_row_vector = Isomorphism._get_row_index_vector(row)
            row_index_vectors.append(single_row_vector)
            pairs.append([single_row_vector, row])

        #print(row_index_vectors)
        #print(pairs)
        
        # sort by length of row vectors and value
        pairs.sort(key = lambda pair: pair[0], reverse = True)
        pairs.sort(key = lambda pair: len(pair[0]), reverse = True)
        #print(pairs)

        # sort by values in row vectors
        
        #print(pairs)

        # extract the now-sorted rows
        rows = []
        for pair in pairs:
            rows.append(pair[1])
        #print(rows)
        
        pvim._matrix = rows

        return pvim