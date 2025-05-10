class Vector:
    def __init__(self, arr):
        self.__arr = arr
    
    @property
    def magnitude(self):
        return sum(map(lambda v: v**2, self.__arr))**0.5

class Matrix: # structure holding numbers in rows and columns
    def __init__(self, arr):
        if not isinstance(arr, (list, tuple)):
            raise ValueError("arr must be an iterable")
        
        row_size = len(arr)
        if row_size == 0:
            raise ValueError("arr cannot be empty")
        
        if not isinstance(arr[0], (list, tuple)):
            raise ValueError("arr must be two dimensional")
        
        col_size = len(arr[0])
        for col_index in range(1, row_size):
            col = arr[col_index]
            if not isinstance(col, (list, tuple)):
                raise ValueError("arr must be two dimensional")
            elif col_size != len(col):
                raise ValueError("all columns must be of same length")
            
        self.__shape = (row_size, col_size)
        self.__arr = arr
    
    @property
    def determinant(self):
        if self.__shape[0] != self.__shape[1]:
            raise ValueError("matrix must be square")

        if self.__shape[0] == 1:
            return self._arr[0][0]
        if self.__shape[0] == 2:
            return self.__arr[0][0]*self.__arr[1][1]-self.__arr[0][1]*self.__arr[1][0]

        _sum = 0
        arr = self.__arr
        for col_index in range(self.__shape[0]):
            c = arr[col_index][0]
            c_s = (col_index & 1) and -1 or 1

            sub_matrix_array = []
            for row_index in range(0, self.__shape[0]):
                if row_index != col_index:
                    lhs = arr[row_index][0:col_index]
                    rhs = arr[row_index][col_index+1:self.__shape[0]]

                    sub_matrix_array.append(lhs + rhs)

            _sum += Matrix(sub_matrix_array).determinant * (c * c_s)
        
        return _sum
    
    @property
    def det(self):
        return self.determinant
    
    def scale(self, scalar):
        new_matrix_arr = []

        for row in self.__arr:
            new_matrix_arr.append([entry * scalar for entry in row])
        
        return Matrix(new_matrix_arr)

    def __str__(self):
        m_str = ""
        
        for row in self.__arr:
            col_str = ""
            for col in row:
                col_str += str(col) + " "
            col_str = col_str[:-1] + "\n"
            m_str += col_str
        m_str = m_str[:-1]
        
        return m_str




if __name__ == "__main__":
    m = Matrix([[5, 9], [5, 6]])
    