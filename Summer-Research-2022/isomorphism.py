# collection of functions used in checking isomorphism and processing matrices in order to check isomorphism
#
# to check, lattices are turned into their associated polygon vertex incidence matrix (pvim) and then manipulated and compared
# if they are equal, the lattices are isomorphic and we can get rid of one
# otherwise, the lattices are different figures and we should keep both
#
# these functions were moved out of lattice_generator.py to make things easier to read
#
# future improvements: replace the concept of a column vector with enumerate to save space?
#                      move compare_vectors functionality to ColumnVectors class
#
# functions:
# management
#   - isomorph in list
#   - check isomorphism (for two individual pvims)
#   - process matrix
# step 1
#   - sort rows
# step 2
#   - sort cols
# step 3
#   - get row vector
#   - break row ties
# step 4
#   - get col vector
#   - break col ties
#   - get groups
#   - get next group
#   - get max length
#   - sort group
#   - compare vectors
# step 5
#   - similarity col sort
#   - get col sum ties
#   - get col vector ties
#   - update group
#   - step 5 sort
#   - col sum get groups
#   - col sum get next group
#   - get similarity vector
#   - get col index vector
# step 6
#   - get row index vector
#   - check row index vectors

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
            if Isomorphism._check_isomorphism(PolygonVertexIncidenceMatrix(item._nodes_list), target_pvim):
                return True

        return False

    # checks to see if two pvims are isomorphic (equaivalent after processing)
    # first checks to be sure the dimensions are the same, then processes each pvim and compares for equality
    #
    # pvim1 - a PolygonVertexIncidenceMatrix to be compared
    # pvim2 - a PolygonVertexIncidenceMatrix to be compared
    #
    # returns False if pvim1 and pvim2 are not the same size or are not equivalent after processing
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
    
    # processes a pvim in six steps, summarized below:
    #    1. sort rows in descending order of their row-sums
    #    2. sort cols in descending order of their col-sums
    #    3. break ties in the row-sum sort by sorting by row vectors, which contain the col-sum of every col for which the row is True 
    #        - can also be described as "a vector of the size of each polygon in which the vertex for that row is involved"
    #    4. break ties in the col-sum sort by sorting by col vectors, which contain the row-sum of every row the col is True
    #        - can also be described as " a vector of the number of shapes each vertex in the shape for this column is involved in"
    #    5. do a final col sort by similarity - a measure of how many shared True rows two cols have
    #        - see method section for more detailed explanation
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
        # step 1: sort rows
        pvim = Isomorphism._sort_rows(pvim)

        # step 2: sort cols
        pvim = Isomorphism._sort_cols(pvim)

        # step 3: row tie-breaking
        # swap rows to be in order within their row vector length groups
        pvim = Isomorphism._break_row_ties(pvim)

        # step 4: col tie-breaking
        # swap cols to be in order within their vertex_vector length groups
        pvim = Isomorphism._break_col_ties(pvim)

        #step 5: put columns in final position by similarity
        pvim = Isomorphism._similarity_col_sort(pvim)

        #step 6: final fix of row order after columns have been set to final spots in step 5
        pvim = Isomorphism._check_row_index_vectors(pvim)

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
        pvim._matrix.sort(key=sum, reverse=True)

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
        for i in range(n):
            for j in range(0, n-i-1):
                # swap adjacent elements if they are in decreasing order
                if pvim.col_sum(j) < pvim.col_sum(j+1): pvim.col_swap(j, j+1)
        
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
        polygon_vector = []
        # go along the row and
        for i in range(len(row)):
            # if it is True,
            if row[i] is True:
                # add the size of the polygon (the col_sum) to the vector
                polygon_vector.append(pvim.col_sum(i))

        return polygon_vector

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

        # sort by length of row vectors and by values
        # sort is stable, which is why this works
        pairs.sort(key = lambda pair: pair[0], reverse = True)
        pairs.sort(key = lambda pair: len(pair[0]), reverse = True)

        # extract the now-sorted rows
        rows = []
        for pair in pairs:
            rows.append(pair[1])
        
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
        while len(column_vectors) != 0:
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
    # cols must remain in their post-step-5 order forever afterward
    # 
    # algorithm:
    #       identify all columns that remain tied after steps 2 and 4 (tied by both col sum and column vector)
    #       all columns not part of a tie are added to set S (S for sorted, aka in final position)
    #       while not all columns are in S,
    #           while the last iteration did add a column to S (meaning we are still making progress with the standard step 5 sorting)
    #               for every tied group you identified above,
    #                   get the similarity vectors with every column in S
    #                   sort the similarity vectors and pvim columns simultaneously by descending sim vector
    #                   add all columns in the group to S moving, left to right until you hit a tie (don't add the tie)
    #                       so you are only adding columns before a tie, if there is one
    #                   and update the limits of the group to exclude the column(s) you just added to S
    #           # choosing is how we tie-break columns with tied sim vectors
    #           # it must be after the normal step 5 sort has done as much as it can
    #           if not all cols are in S, choose the first column in the left-most remaining group to become "sorted"
    #       done!
    #
    # pvim - PolygonVertexIncidenceMatrix object to be sorted
    #
    # returns sorted PolygonVertexIncidenceMatrix
    @staticmethod
    def _similarity_col_sort(pvim):
        # get groups
        tied_groups = Isomorphism._get_col_vector_ties(Isomorphism._get_col_sum_ties(pvim), pvim)
        # remove single column groups
        tied_groups = [group for group in tied_groups if group[0] != group[1]]

        # put all indices not included in a tied group in s
        # by putting all indices in S and then removing those in a group
        s = list(range(0, pvim.dimensions()[1]))
        for group in tied_groups:
            s = [i for i in s if i not in range(group[0], group[1] + 1)]
        s = list(set(s))

        # for tracking if changes occured. needs to start as True so inner while starts
        added_to_s = True
        # while not all columns are in S
        while len(s) != pvim.dimensions()[1]:
            # while the last iteration produced a change
            while added_to_s == True:
                added_to_s = False
                for i in range(0, len(tied_groups)):
                    # can't remove tied groups during the loop or it messes up the iteration,
                    # so I make them None and remove after the for loop
                    # a None tie is actually a removed tie, it just hasn't actually been removed yet
                    # no need to look at it
                    if tied_groups[i] is None: continue

                    # get sim vectors
                    sim_vectors = []
                    colI = tied_groups[i][0]
                    while colI <= tied_groups[i][1]:
                        sim_vectors.append(Isomorphism._get_similarity_vector(colI, pvim, s))
                        colI = colI + 1

                    # do the sort
                    pvim, sim_vectors = Isomorphism._step_5_sort(tied_groups[i], pvim, sim_vectors)

                    # move columns in final position to S
                    for j in range(1, len(sim_vectors)):
                        if sim_vectors[j - 1][1] == sim_vectors[j][1]:
                            break
                        s.append(tied_groups[i][0] + j - 1)
                        added_to_s = True
                    
                    # and update the group
                    # group reduces to nothing
                    if Isomorphism._update_group(tied_groups[i], s) is None:
                        tied_groups[i] = None
                    # group reduces to one column
                    elif Isomorphism._update_group(tied_groups[i], s)[0] == Isomorphism._update_group(tied_groups[i], s)[1]:
                        s.append(tied_groups[i][1])
                        added_to_s = True
                        tied_groups[i] = None
                    # normal operations (>1 col remaining in group)
                    else:
                        tied_groups[i] = Isomorphism._update_group(tied_groups[i], s)
                    # force the order to match matrix
                    s.sort()
                # fine to remove from the list because I'm outside of the iterator
                tied_groups = [group for group in tied_groups if group is not None]
            # choosing
            if len(s) != pvim.dimensions()[1]:
                # choose first from left-most group, add it to s
                s.append(tied_groups[0][0])
                added_to_s = True
                # force the order
                s.sort()
                # and update the group
                # group reduces to nothing
                if Isomorphism._update_group(tied_groups[0], s) is None:
                    # fine to remove from the tied_groups list because I'm outside of the iterator
                    tied_groups.remove(tied_groups[0])
                # group reduces to one column
                elif Isomorphism._update_group(tied_groups[0], s)[0] == Isomorphism._update_group(tied_groups[0], s)[1]:
                    s.append(tied_groups[0][1])
                    added_to_s = True
                    # fine to remove from the tied_groups list because I'm outside of the iterator
                    tied_groups.remove(tied_groups[0])
                # normal operations (>1 col remaining in group)
                else:
                    tied_groups[0] = Isomorphism._update_group(tied_groups[0], s)
        return pvim


    # used in identifying tied columns for step 5 similarity col sort
    #
    # takes a pvim, calculates the column sums for every column,
    # then calls out to helpers to get the indices (inclusive, inclusive) of ties
    #
    # returns groups, a list of lists, each of length 2 and containing the start and end (inclusive) indices for ties
    #
    # I'm not sure this is the best way to handle no tied, but right now it gives a list of lists of length 2,
    # each with the same index repeated. ex. [[0,0], [1,1], [2,2], [3,3]]. so one "tied group" for every single column
    @staticmethod
    def _get_col_sum_ties(pvim):
        # get col sums
        col_sums = []
        for i in range(0, pvim.dimensions()[1]):
            col_sums.append(pvim.col_sum(i))
            
        # id groups of tied col sums from the list
        return Isomorphism._col_sum_get_groups(col_sums)

    # used in identifying tied columns for step 5 similarity col sort
    #
    # need to take in pvim also to get column vectors
    # looks in each group of tied by col sum to check if it contains a tie by col vector
    # no need to check if the tie is less than two columns because that would not result in any movement
    # get the col vector for every col in the col-sum-tie, then get the tied groups of those col vectors
    # collect the indices (inclusive) of those tied groups into a list of lists and return that
    #
    # returns groups, a list of lists, each of length 2 and containing the start and end (inclusive)
    # indices where the matrix is tied by col vector
    @staticmethod
    def _get_col_vector_ties(col_sum_groups, pvim):
        ties = []
        #looking for tied col vectors within the tied col sum areas
        for group in col_sum_groups:
            # if group covers only 1 column, no need to move things so don't bother considering it
            if group[1] == group[0]:
                continue
            # get col vectors
            column_vectors = []
            # + 1 because group[1] inclusive
            for i in range(group[0], group[1] + 1):
                # list of CV objects
                column_vectors.append(Isomorphism._get_col_vector(i, pvim))

            # split into groups
            while len(column_vectors) > 0:
                # temp = one possible tie in this group
                temp = [column_vectors[0]]
                # move left to right through all remaining in the group to consider
                for i in range(1, len(column_vectors)):
                    # compare vectors
                    # if not the same, stop looking at this tie (break)
                    if column_vectors[i-1].get_vector() != column_vectors[i].get_vector(): break
                    # add to this tie if they are the same
                    temp.append(column_vectors[i])
                # we only care about ties of 2 of more columns
                if len(temp) > 1:
                    ties.append([temp[0].get_index(), temp[-1].get_index()])
                # reset the vectors under consideration
                # this is why i track a list, not just a start and end index
                column_vectors = [x for x in column_vectors if x not in temp] 

        return ties
    
    # shrinks a group by eliminating columns which have been sorted into S
    # 
    # group - a list of length 2, containing the start and end (inclusive) indices of the group to shrink
    # s - the list of indices of fixed columns
    # 
    # returns group, a list of length 2, containing the start and end (inclusive) indices of the group
    #         or None, if the group has shrunk to nothing (start > end) or was None in the first place
    @staticmethod
    def _update_group(group, s):
        # need that for [4,4]
        if group is None or group[0] == group[1]: return None
        group = list(range(group[0], group[1] + 1))
        group = [x for x in group if x not in s]
        # need that for group cleared
        if len(group) == 0: return None
        return [group[0], group[-1]]
 
    # the actual sorting for step 5
    # sorts the columns in a group by descending similarity vectors
    # selection sort
    #
    # returns the sorted pvim and the enumerated, sorted sim vectors (i need that for update_group)
    @staticmethod    
    def _step_5_sort(group, pvim, sim_vectors):

        start_i = group[0]
        # now a list of tuples, the pvim index and the sim_vector for the column at that index
        sims_e = [tuple(pair) for pair in enumerate(sim_vectors, start = start_i)]

        # if only one col, it's already in sorted order
        if group[0] == group[1]: return pvim, sims_e        

        # sort cols in group by sim vector
        # i need all this crazy +start_i and -start_i because i'm working in
        # the middle of the matrix but the beginning of the sim_vector list
        #
        # selection sort
        # i feel like i need to justify myself? I chose selection sort because I need the cols in the group to be fully sorted
        # (otherwise i would just get the max and swap it with the first index) so I can id if there is a tie at the front or not.
        # pvim only provides swap for columns, so it needed to be swap based.
        max_idx = 0
        for i in range(start_i, start_i + len(sims_e) - 1):   
            max_idx = i
            for j in range(i+1-start_i, len(sims_e)):
                if sims_e[j][1] > sims_e[max_idx - start_i][1]:
                    max_idx = j + start_i
            sims_e[i-start_i], sims_e[max_idx-start_i] = sims_e[max_idx-start_i], sims_e[i-start_i]
            pvim.col_swap(i, max_idx)

        return pvim, sims_e

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
    # a similarity vector is how many of the columns' rows are both true
    # ex.    True  True    the first col has a similarity vector of [2] because the cols share two True rows
    #        True  True    
    #        False True    s = [1]
    #        True  False   
    #
    # ex. comparing col 1 to 2 and 3
    #        True, True, False        first col has [2, 1] because both are true on the first and second rows in cols 1 and 2                                                      
    #        True, True, False                             and cols 1 and 3 are only both true on row 2
    #        True, False, True
    #        False, True, False       s = [1, 2]
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
    # s - set of the pvim indices of the sorted columns
    #
    # returns the similarity vector, a list of similarity values (ints)
    # returns [] if no similarities or no columns to be similar to (s is empty)
    @staticmethod
    def _get_similarity_vector(col, pvim, s):
        if col < 0 or col >= pvim.dimensions()[1]: raise ValueError("col index out of bounds")
        if len(s) == 0: return []
        if len(s) == 1 and s[0] == col: return []

        sim_vector = []

        # get the row-indices of each true for this column
        col_indices = Isomorphism._get_col_index_vector(col, pvim)

        # for every column in S,
        for index in s:
            sum = 0
            # add up how many of the Trues in the two columns are on the same row
            # get the indexes of each True in that col, 
            other_col_indices = Isomorphism._get_col_index_vector(index, pvim)
            for item in col_indices:
                # check each and add one to a sum if they match,
                if item in other_col_indices:
                    sum = sum + 1
            # add the sum to the sim vector
            sim_vector.append(sum)

        return sim_vector
    
    # helper for get_similarity_vector
    # get the row indices where this column is True
    #
    # col - the column index to build the index vector for
    # pvim - a PolygonVertexIncidenceMatrix
    #
    # returns a list of the row indices where this column is True (the column index vector)
    @staticmethod
    def _get_col_index_vector(col, pvim):
        if col < 0 or col >= pvim.dimensions()[1]: raise ValueError("col index out of bounds")
        index_vector = []
        for i in range(len(pvim._matrix)):
            # for every True in this col, append the index to the index_vector
            if pvim._matrix[i][col] == True:
                index_vector.append(i)     

        return index_vector

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
    #     Then, sort the vectors in ascending order of their size, while sorting the matrices in parallel.
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
        
        # ik it seems out of order but this is how it's meant to be
        # sort by values in row vectors and value
        pairs.sort(key = lambda pair: pair[0], reverse = False)
        # sort by len of row vectors
        pairs.sort(key = lambda pair: len(pair[0]), reverse = True)

        # extract the now-sorted rows
        rows = []
        for pair in pairs:
            rows.append(pair[1])
        
        pvim._matrix = rows

        return pvim