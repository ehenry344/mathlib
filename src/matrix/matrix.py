import random
import time

class Vector:
    def __init__(self, arr):
        if not isinstance(arr, (list, tuple)):
            raise ValueError("arr must be an iterable")
        
        for elem in arr:
            if isinstance(elem, (list, tuple)):
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
    
    @property
    def arr(self):
        return self.__arr
    
    @property
    def size(self):
        return len(self.__arr)
    
    def __add__(self, other):
        if isinstance(other, Vector):
            if self.size == other.size:
                sum_arr = []
                for i in range(self.size):
                    sum_arr.append(self.__arr[i] + other.__arr[i])
                return Vector(sum_arr)
            else:
                raise ValueError("invalid size")
        else:
            raise ValueError("type of other not supported")
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            product_arr = []
            for i in range(self.size):
                product_arr.append(self.__arr[i] * other)
            return Vector(product_arr)
    
    def __str__(self):
        vec_str = "["
        for idx in range(self.size):
            if idx == self.size - 1:
                vec_str += str(self.__arr[idx])
            else:
                vec_str += str(self.__arr[idx]) + " "
        vec_str += "]"
        return vec_str

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
        submatrix = self.__get_submatrix(i, j)
        submatrix_det = submatrix.determinant
        return coeff * submatrix_det
        
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
    def determinant(self):
        copy_arr = self.copy().__arr
        num_rows = self.shape[1]

        if not self.issquare:
            raise ValueError("matrix must be nxn to compute determinant")
        
        det = self.arr[0][0]

        num_swaps = 0
        if num_rows > 1:
            pos = 0
            while pos < num_rows - 1:
                curr_pivot = copy_arr[pos][pos]
                if curr_pivot == 0: # need to row swap
                    num_swaps += 1
                    row_offset = 1
                    while copy_arr[pos][pos] == 0:
                        temp_row = copy_arr[pos]
                        copy_arr[pos] = copy_arr[pos+row_offset]
                        copy_arr[pos+row_offset] = temp_row
                        row_offset = row_offset + 1
                    continue
                else:
                    pivot_vector = Vector(copy_arr[pos])
                    for row_idx in range(pos + 1, num_rows):
                        row_vector = Vector(copy_arr[row_idx])
                        scale_factor = -copy_arr[row_idx][pos] / curr_pivot
                        row_vector = row_vector + pivot_vector * scale_factor
                        copy_arr[row_idx] = row_vector.arr # replace
                    pos += 1
            # now just multiply diagonals
            for idx in range(1, num_rows):
                det *= copy_arr[idx][idx]
        
        swap_sign = num_swaps & 1 and -1 or 1
        return det * swap_sign


    
    def copy(self):
        copy_arr = []
        for row in self.__arr:
            row_vector = []
            for entry in row:
                row_vector.append(entry)
            copy_arr.append(row_vector)
        return Matrix(copy_arr)


    @property
    def det(self): return self.determinant

    @property
    def issquare(self): return self.__shape[0] == self.__shape[1]

    @property
    def shape(self): return (self.__shape[0], self.__shape[1])

    @property
    def arr(self): return self.__arr
    
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
    
def generate_randint_matrix(nrows=1, ncols=1, _min=0, _max=1000):
    vector_arr = []
    for i in range(nrows):
        row_vector = []
        for j in range(ncols):
            row_vector.append(random.randint(_min, _max))
        vector_arr.append(row_vector)
    return Matrix(vector_arr)

    
if __name__ == "__main__":
    test_arr = [
        [1, 2, 3],
        [7, -9, 4],
        [3, 2, 1]
    ]
    test_mat = Matrix(test_arr)
    
    rand_matrix = generate_randint_matrix(15, 15, 0, 1)

    print(rand_matrix.determinant)
