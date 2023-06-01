from typing import Callable, Iterable
import ast
import numpy as np

def loadFormula(formulaStr):
    formulaAst = ast.parse(formulaStr, mode='eval')
    return eval(compile(formulaAst, filename='<string>', mode='eval'))

class FormulaGenerator():
    """
    works with numpy arrays as output of generators
    """

    def __init__(self, dim: int, maxDegree: int, constantsGenerator: Callable, degreeBoolGenerator: Callable): 
        # operatorGenerator could be implemented here
        self.dim = dim
        self.maxDegree = maxDegree
        self.constantsGenerator = constantsGenerator
        self.degreeBoolGenerator = degreeBoolGenerator

    def generate(self, num: int) -> list[list[tuple[Callable, str]]]:
        """returns a list of formulaPairs: 
        formulaPairs are a list of tuples, one tuple for each variable.
        the tuple contains the lambda and the string version of the respective formula"""

        genSize = (self.dim, self.dim, self.maxDegree)
        return [
            self.generateSingleFormulaPair(self.constantsGenerator(genSize), self.degreeBoolGenerator(genSize)) for _ in range(num)
        ]

    def generateSingleFormulaPair(self, constants, degreeBools) -> list[tuple[Callable, str]]:
        """returns one formulaPair: 
        formulaPairs are a list of tuples, one tuple for each variable.
        the tuple contains the lambda and the string version of the respective formula
        """
        varnames = generateVarNamesLikeExcel(self.dim)
        formulas = []
        for i, varname in enumerate(varnames):
            formulaStr = "lambda " + ",".join(varnames) + ": "
            for i2, varname in enumerate(varnames):
                for j in range(1, self.maxDegree+1):
                    if degreeBools[i, i2, j-1]:
                        c = str(constants[i, i2, j-1])
                        if not c.startswith("-"):
                            c = "+" + c

                        # random.choice(["", "-"]) +
                        # this breaks things with a typeerror: unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'
                        formulaStr += c + "*" + varname + ("**" + str(j) if j != 1 else "")
                
                c = str(self.constantsGenerator(1)[0])
                if not c.startswith("-"):
                    c = "+" + c

                formulaStr += c

            if formulaStr.endswith(": "):
                formulaStr += "1" # default if lambda is empty - 1 instead of 0 to continue producing values
            
            formulas.append((loadFormula(formulaStr), formulaStr))

        return formulas
    

def duplicateElemsWithIndex(elems: list, start: int, end: int):
    return [elem + str(num) for elem in elems for num in range(start, end)]

def generateVarNamesLikeExcel(count):
    variable_names = []
    current_letter = ord('a')

    for _ in range(count):
        variable_name = ''
        quotient, remainder = divmod(current_letter - ord('a'), 26)

        while quotient > 0:
            variable_name += chr(ord('a') + quotient - 1)
            quotient, remainder = divmod(remainder, 26)

        variable_name += chr(ord('a') + remainder)
        variable_names.append(variable_name)
        current_letter += 1

    return variable_names


if __name__ == "__main__":
    # test the module here

    degreeBoolGenerator = lambda degrees: np.random.choice([True, False], size=degrees)
    constantsGenerator = lambda size: np.round(np.random.normal(0, 1, size), 3)

    dims = 2
    maxdegree = 3

    fg = FormulaGenerator(dims, maxdegree, constantsGenerator, degreeBoolGenerator)
    for formulaPair in fg.generate(10):
        print(formulaPair)
        print(formulaPair[0][0](*[69]*2))
        print(formulaPair[1][0](*[69]*2))

