import copy
class Atom:
    def __init__(self, name):
        self.name = name

    def equals(self, atom):
        if type(atom)==Atom:
            return self.name == atom.getName()
        else:
            return False

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Functor:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def getArguments(self):
        return self.arguments

    def getArity(self):
        return len(self.arguments)

    def getName(self):
        return self.name
    def __str__(self):
        return self.name+'('+''.join([str(i) for i in self.arguments])+')'
    def equals(self, functor):
        if type(functor)==Functor:
            return self.name == functor.getName() and self.arguments==functor.getArguments()
        else:
            return False

class Rule:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

class Query:
    def __init__(self,functor):
        self.functor=functor
    def getFunctor(self):
        return self.functor

class Fact:
    def __init__(self,functor):
        self.functor = functor
    def getFunctor(self):
        return self.functor

class Variable:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def equals(self,term):
        if type(term)== Variable:
            return term.getName()==self.getName()
        else:
            return False
    def __str__(self):
        return self.name


class Unification:
    def __init__(self, substitutions):
        self.substitutions = substitutions
        self.__str__()

    def get_substitutions(self):
        return self.substitutions

    def canCombine(self, unification):
        new_substitutions = unification.get_substitutions()
        for term in new_substitutions:
            if term in copy.deepcopy(self.substitutions):
                if not copy.deepcopy(self.substitutions[term]).equals(new_substitutions[term]):
                    return False
        return True

    def combine(self, unification):
        unification_copy=copy.deepcopy(self.substitutions)
        new_substitutions = unification.get_substitutions()
        for term in new_substitutions:
            unification_copy[term] = new_substitutions[term]
        return Unification(unification_copy)

    def __str__(self):
        self.output = "{"
        for key in self.substitutions:
            self.output += "[" + key + "=" + str(self.substitutions[key]) + "]"
        self.output += "}"
        return self.output


def unify(term1, term2):
    if type(term1) == Atom and type(term2) == Atom:
        if term1.equals(term2):
            return Unification({})
        else:
            return False
    if type(term1) == Variable:
        return Unification({term1.getName(): term2})
    if type(term2) == Variable:
        return Unification({term2.getName(): term1})
    if type(term1) == Functor and type(term2) == Functor:
        if term1.getArity() == term2.getArity() and term1.getName() == term2.getName():
            substitutions = Unification({})
            term1Arguments = term1.getArguments()
            term2Arguments = term2.getArguments()
            for i in range(len(term1Arguments)):
                new_unification = unify(term1Arguments[i], term2Arguments[i])
                new_unification
                if new_unification and substitutions.canCombine(new_unification):
                    substitutions=substitutions.combine(new_unification)
                else:
                    return False
            return substitutions
    return False



class KnowledgeBase:
    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts

    def get_rules(self):
        return self.rules

    def get_facts(self):
        return self.facts

    def solve(self,query):
        solutions=[]
        for fact in self.facts:
            unification=unify(query.getFunctor(),fact.getFunctor())
            unification
            if unification:
                solutions.append(unification)
            solutions
        for rule in self.rules:
            unification=unify(query.getFunctor(),rule.getHead())
            if unification:
                current_solutions=[unification]
                for tailCondition in rule.getTail():
                    new_solutions=[]
                    for current_solution in current_solutions:
                        generated_solutions=self.solve(Query(copy.deepcopy(tailCondition)))
                        for generated_solution in generated_solutions:
                            if current_solution.canCombine(generated_solution):
                                new_solutions.append(copy.deepcopy(current_solution.combine(generated_solution)))
                    current_solutions=copy.deepcopy(new_solutions)
                solutions+=current_solutions
        return solutions

Beth=Atom("Beth")
Jan=Atom("Jan")
Cherie=Atom("Cherie")
Dad=Atom("Vince")
Dan=Atom("Dan")
DansMum=Fact(Functor("IsMum",[Cherie,Dan]))
MumsMum=Fact(Functor("IsMum",[Jan,Cherie]))
DansDad=Fact(Functor("IsDad",[Dad,Dan]))
DadsMum=Fact(Functor("IsMum",[Beth,Dad]))

A=Variable('A')
B=Variable('B')

X=Variable('X')
Y=Variable('Y')
Z=Variable('Z')
#If X and Y are related and Y and Z are related, X and Z are related
RelationRule=Rule(Functor("IsNan",[Z,X]),[Functor("IsMum",[Z,Y]),Functor("IsMum",[Y,X])])
RelationRule2=Rule(Functor("IsNan",[Z,X]),[Functor("IsMum",[Z,Y]),Functor("IsDad",[Y,X])])

#Who's Joel Related to?
my_query=Query(Functor("IsNan",[A,B]))
kb=KnowledgeBase([RelationRule,RelationRule2],[DansMum,MumsMum,DansDad,DadsMum])
print([str(u) for u in kb.solve(my_query)])