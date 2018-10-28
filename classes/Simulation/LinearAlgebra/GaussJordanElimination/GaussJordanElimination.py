import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class GaussJordanElimination(SimulationStrategy):
    records = ["Initial Matrix"]
    matrices = []
    mat = np.array([[0.0, 1.0, 1.0, -2.0, -3.0],
                    [1.0, 2.0, -1.0, 0.0, 2.0],
                    [2.0, 4.0, 1.0, -3.0, -2.0],
                    [1.0, -4.0, -7.0, -1.0, -19.0]]);

    def __init__(self, _mat):
        self.records = ["Initial Matrix"]
        self.matrices = []
        self.mat = _mat

    def eliminate(self, row, column):
        if row == self.mat.__len__() or column == self.mat[0].__len__():
            return
        row_temp = row
        while self.mat[row_temp][column] == 0 and row_temp < self.mat.__len__()-1:
            row_temp += 1
        if self.mat[row_temp][column] == 0:
            return self.eliminate(row, column + 1)
        if row_temp != row:
            self.records.append("Swap rows: " + str(row+1) + " and " + str(row_temp+1))
            self.matrices.append(self.mat.tolist())
            self.mat[row], self.mat[row_temp] = self.mat[row_temp], self.mat[row].copy()
        if self.mat[row][column] != 1:
            self.records.append("row(" + str(row + 1) + ") = " + "row(" + str(row + 1) + ") / "
                                + str(format(self.mat[row][column], '.3f')))
            self.matrices.append(self.mat.tolist())
            self.mat[row] /= self.mat[row][column]
        for i in range(row+1, self.mat.__len__()):
            if self.mat[i][column] != 0:
                self.records.append("row(" + str(i + 1) + ") = " + "row(" + str(i + 1) + ") - " +
                                    "row(" + str(row + 1) + ") * " + str(format(self.mat[i][column], '.3f')))
                self.matrices.append(self.mat.tolist())
                self.mat[i] -= self.mat[row] * self.mat[i][column]
        self.eliminate(row+1, column+1)

    def reverse_eliminate(self, row, column):
        op_row = row - 1
        while op_row >= 0:
            if self.mat[op_row][column] == 0:
                op_row -= 1
                continue
            self.records.append("row(" + str(op_row + 1) + ") = " + "row(" + str(op_row + 1) + ") - " +
                                "row(" + str(row + 1) + ") * " + str(format(self.mat[op_row][column], '.3f')))
            self.matrices.append(self.mat.tolist())
            self.mat[op_row] -= self.mat[row] * self.mat[op_row][column]
            op_row -= 1

    def jordan(self, row, column):
        if row == self.mat.__len__() or column == self.mat[0].__len__():
            return
        if self.mat[row][column] == 0:
            return self.jordan(row, column + 1)
        self.reverse_eliminate(row, column)
        return self.jordan(row+1, column+1)

    def get_data(self):
        self.eliminate(0, 0)
        self.jordan(1, 1)
        self.matrices.append(self.mat.tolist())
        data = {}
        data["records"] = self.records
        data["matrices"] = self.matrices
        return data