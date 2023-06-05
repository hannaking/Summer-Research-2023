# Used to represent a column from a list of lists. it makes it easier to access column information (avoid nested for loops)
#
# functions:
#   - get_vector
#   - get_index

class ColumnVector():
    # takes a list and an int index
    # list becomes the vector. Defaults to []
    # index tells you where on whatever this comes from you are. Defaults to 0
    def __init__(self, vector=[], index=0):
        self._vector    = vector
        self._index     = index

    # returns the list _vector
    def get_vector(self):
        return self._vector

    # returns the int _index
    def get_index(self):
        return self._index
    
    def __str__(self):
        string = ""
        for value in self._vector:
            string += str(value)
        string += ", " + str(self._index)
        return string