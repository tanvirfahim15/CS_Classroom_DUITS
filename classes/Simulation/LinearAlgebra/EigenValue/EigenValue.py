import numpy as np
from pattern.SimulationStrategy.Strategy import SimulationStrategy


class EigenValue(SimulationStrategy):
    mat = [[1, 2], [3, 4]]

    def __init__(self, _mat):
        self.mat = _mat

    def get_data(self):
        det_array=[]
        for i in range(self.mat.__len__()):
            row = []
            for j in range(self.mat.__len__()):
                col=''
                if i != j:
                    col += str(self.mat[i][j])
                else:
                    col += str(self.mat[i][j])+'-λ'
                row.append(col)
            det_array.append(row)
        equations = []
        equation = '(' + det_array[0][0] + ')' + ' * ' + '('+det_array[1][1]+') - (' + det_array[0][1]+') * ('\
                   + det_array[1][0]+') = 0'
        equations.append(equation)
        b = self.mat[0][0]+self.mat[1][1]
        c = self.mat[0][0]*self.mat[1][1]-self.mat[1][0]*self.mat[0][1]
        equation = 'λ^2 '
        if b >= 0:
            equation += "-"
        equation += str(b) + 'λ '
        if c >= 0:
            equation += "+"
        equation += str(c) + ' = 0'

        equations.append(equation)
        coeff = [1, -(self.mat[0][0]+self.mat[1][1]), self.mat[0][0]*self.mat[1][1]-self.mat[1][0]*self.mat[0][1]]
        roots = np.roots(coeff)

        equation = 'λ^2 '
        if round(roots[0], 3)<0:
            equation+="+"
        equation += str(round(roots[0], 3)*-1)
        equation += "λ"
        if round(roots[1], 3)<0:
            equation+="+"
        equation += str(round(roots[1], 3)*-1)
        equation += "λ"
        if c >= 0:
            equation += "+"
        equation += str(c) + ' = 0'
        equations.append(equation)

        equation="λ"
        equation+="(λ"
        if roots[0]<0:
            equation+="+"
        equation+=str(round(roots[0], 3)*-1)+")"
        if roots[1]<0:
            equation+="+"
        equation+=str(round(roots[1], 3)*-1)
        equation += "(λ"
        if roots[0] < 0:
            equation += "+"
        equation += str(round(roots[0], 3) * -1) + ") = 0"
        equations.append(equation)

        equation = "(λ"
        if roots[0] < 0:
            equation += "+"
        equation += str(round(roots[0], 3) * -1) + ")"

        equation += "(λ"
        if roots[1] < 0:
            equation += "+"
        equation += str(round(roots[1], 3) * -1) + ") = 0"

        equations.append(equation)

        equation = 'Eigen Values(λ) = [ '
        for root in roots:
            equation += str(round(root, 3))+' '
        equation += " ]"
        equations.append(equation)

        output = dict()
        output['det_array'] = det_array
        output['equations'] = equations
        return output


