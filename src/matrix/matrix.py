class Vector:
    def __init__(self, arr):
        if not isinstance(arr, (list, tuple)):
            raise ValueError("arr must be an iterable")
        
        for elem in arr:
            if not isinstance(elem, (list, tuple)):
                raise ValueError("arr must be one dimensional")
        
        self.__arr = arr
    
    def dot(self, other):
        if len(other.__arr) != len(self.__arr):
            raise ValueError("both vectors must be of same length")
        
        dot_product = 0

        for idx in range(self.__arr):
            dot_product += (self.__arr[idx] * other.__arr[idx])

        return dot_product
    
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

    def __get_submatrix(self, i, j): # returns matrix with row i and column j removed
        row_array = self.__arr[0:i] + self.__arr[i+1:]
        sub_matrix_array = []

        for row in row_array:
            sub_matrix_array.append(row[0:j] + row[j+1:])

        return Matrix(sub_matrix_array)
    
    def cofactor(self, i, j):
        coeff = (i+j) & 1 and -1 or 1
        return coeff * self.__get_submatrix(i, j).determinant
    
    @property
    def determinant(self):
        if not self.issquare:
            raise ValueError("matrix must be square")

        if self.__shape[0] == 1:
            return self.__arr[0][0]
        if self.__shape[0] == 2:
            return self.__arr[0][0]*self.__arr[1][1]-self.__arr[0][1]*self.__arr[1][0]
        
        _sum = 0
        for i in range(self.__shape[0]):
            _sum += self.__arr[i][0] * self.cofactor(0, i)
        
        return _sum
    
    @property
    def inverse(self):
        if not self.issquare:
            raise ValueError("matrix must be nxn")
        
        adj_mat = []
        for row_index in range(self.__shape[0]):
            adj_vector = []
            for col_index in range(self.__shape[0]):
                adj_vector.append(self.cofactor(col_index, row_index))
            adj_mat.append(adj_vector)
        
        return Matrix(adj_mat).scale(1/self.determinant)
    
    def multiply(self, other): # naive matrix multiplication
        if not isinstance(other, Matrix):
            raise ValueError("can only multiply a matrix with another matrix")    
        if self.shape[1] != other.shape[0]:
            raise ValueError("matrix shapes incompatible for matrix multiplication")
        
        result = []
        for i in range(self.shape[0]):
            result_row = []
            for j in range(other.shape[1]):
                entry_sum = 0
                for k in range(self.shape[1]):
                    entry_sum += self.__arr[i][k] * other.__arr[k][j]
                result_row.append(entry_sum)
            result.append(result_row)

        return Matrix(result)

    
    @property
    def det(self): return self.determinant

    @property
    def issquare(self): return self.__shape[0] == self.__shape[1]

    @property
    def shape(self): return (self.__shape[0], self.__shape[1])
    
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
    m = Matrix([[1, 6], [4, 4]])
    print(m.multiply(Matrix([[1, 0], [0, 1]])))