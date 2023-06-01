from typing import Iterable
import re




class FormulaParser():
    def __init__(self):
        pass


    def outputParsedComponents(self, formulaPair: Iterable[str], obligatoryVariableExponentPairs: dict[str, list[int]]):
        variableDictList = []

        for formula in formulaPair:
            formula = formula.split(": ")[1]
            variableDict = {}

            separatedExpressions = self.splitStringWithOperators(formula)
            
            for expr in separatedExpressions:
                if "*" not in expr:
                    variableDict["yShift**1"] = variableDict.get("yShift**1") or 0
                    variableDict["yShift**1"] = round(variableDict["yShift**1"] + float(expr), 3)
                else:
                    num, var, exp = self.extractNumVarExponentFromExpr(expr)
                    variableDict[f"{var}**{exp}"] = variableDict.get("yShift") or 0
                    variableDict[f"{var}**{exp}"] = round(variableDict[f"{var}**{exp}"] + num, 3)
            
            for var, exps in obligatoryVariableExponentPairs.items():
                for exp in exps:
                    variableDict[f"{var}**{exp}"] = variableDict.get(f"{var}**{exp}") or 0
            variableDictList.append(variableDict)

            for k in list(variableDict):
                if k.endswith("**1"):
                    variableDict[k[:-3]] = variableDict[k]
                    del variableDict[k]

        return variableDictList
    
    def extractNumVarExponentFromExpr(self, expr):
        if "**" in expr:
            numVar, exp = expr.split("**")
        else:
            numVar = expr
            exp = 1

        num, var = numVar.split("*")
        return float(num), var, int(exp)

    def splitStringWithOperators(self, string):
        result = []
        currentExpr = string[0]
        for a in string[1:]:
            if a not in ("+", "-"):
                currentExpr += a
            else:
                result.append(currentExpr)
                currentExpr = a
        result.append(currentExpr)

        return result

if __name__ == "__main__": 
    formula = [
        "+1.712*a-0.202*a**2+1.9+0.102*b+0.063",
        "+0.2-0.541*b+1.286"
    ]

    # s = shift

    fr = FormulaParser()
    output = fr.outputParsedComponents(formula, {"a": [1,2], "b": [1,2], "yShift": [1]})
    print(output)