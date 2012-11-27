#!/usr/bin/env python

from random import randrange, seed, choice
from itertools import ifilter, izip
import itertools

#This problem is like a mastermind,
# except with less choice (6 instead of 8)
# except with more slot (6 intead of 4)
# except without the "good but bad place" result, only good or bad



###############################
# Utils
###############################


def combinaison_with_doublon_and_order(choice, size):
  choiceLen = len(choice)
  sizeModulo = [ choiceLen ** n for n in range(size) ]

  for i in range(choiceLen ** size):
    yield [ choice[(i / n) % choiceLen] for n in sizeModulo ]


def nbDiff(l1, l2):
  return len(list(ifilter(lambda x: x[0] == x[1] , izip(l1, l2))))



class ProblemDefinition:
  def __init__(self, nbPlaces, nbElements, nbTries, names = None):
    self.nbPlaces = nbPlaces
    self.nbElements = nbElements
    self.nbTries = nbTries

    if names == None:
      names = [str(i) for i in range(nbElements)]

    self.names = names

  def getCombi(self): return self.nbPlaces ** self.nbElements

  def toHumain(self, e, msg = "Elements"):
    return msg + " : " + ' '.join([str(self.names[i]) for i in e])




class ProbWithResolv:

  @staticmethod
  def medianOn(size, problem, resolver, probDef):
    res = []
    for i in range(size):
      p = ProbWithResolv(problem, resolver, probDef)
      cur = p.tryBeforeWin()
      if cur == None: cur = probDef.getCombi() * 2
      res.append(cur)
    print(sum(res))
    return sum(res) / size


  def __init__(self, problem, resolver, probDef):
    self.probDef = probDef
    self.problem = problem()
    self.resolver = resolver()

  def step(self):
    tryContent = self.resolver.getNextTrie()
    tryResult = self.problem.tryMe(tryContent)
    if tryResult == self.probDef.nbPlaces:
      return self.problem.getNbTry()
    self.resolver.setTrieResult(tryContent, tryResult)
    return None


  def step_with_print(self):
    print self.probDef.toHumain(self.problem.getSolution(), "Solution")
    tryContent = self.resolver.getNextTrie()
    print self.probDef.toHumain(tryContent, "Try     ")
    tryResult = self.problem.tryMe(tryContent)
    print "TryResult : %s" % tryResult
    if tryResult == self.probDef.nbPlaces:
      return self.problem.getNbTry()
    self.resolver.setTrieResult(tryContent, tryResult)
    return None

  def tryBeforeWin(self, maxTries = None):
    for i in range(maxTries or self.probDef.getCombi()):
      #r = self.step_with_print()
      r = self.step()
      if r != None: break
    return r
      

###############################
# Problem map
###############################



class Problem:
  def __init__(self, prob):
    self.solution = prob
    self.nbTries = 0

  def tryMe(self, tryContent):
    self.nbTries += 1
    return nbDiff(self.solution, tryContent)

  def getNbTry(self): return self.nbTries
  def getSolution(self): return self.solution

  def __call__(self): return Problem(self.prob)



class FixedProblem(Problem):
  def __call__(self): return FixedProblem(self.solution)


class RandomProblem(FixedProblem):

  def __init__(self, probDef):
    self.probDef = probDef
    FixedProblem.__init__(self, [randrange(probDef.nbElements) for e in range(probDef.nbPlaces)])

  def __call__(self): return RandomProblem(self.probDef)


class HumainProblem(Problem):
  def __init__(self, probDef):
    self.probDef = probDef
    self.nbTries = 0

  def __call__(self): return HumainProblem(self.probDef)

  def tryMe(self, tryContent):
    self.nbTries += 1
    print self.probDef.toHumain(tryContent, "Step %s, try this solution :" % self.nbTries)
    nb = int(raw_input("How many elements are good ? : "))
    return nb



###############################
# Problem resolver
###############################

class Resolver:
  def getNextTrie(self): return None
  def setTrieResult(self, tryContent, number): pass
  def __call__(self): return Resolver()


class FixedResolver(Resolver): #50.000
  def __init__(self, res): self.res = res

  def getNextTrie(self): return self.res
  def __call__(self): return FixedResolver(self.res)



class RandomResolver(Resolver): #50.000
  
  def __init__(self, probDef):
    self.probDef = probDef
    self.nbPlaces = probDef.nbPlaces
    self.nbElements = probDef.nbElements

  def getNextTrie(self):
    return [randrange(self.nbElements) for e in range(self.nbPlaces)]

  def __call__(self): return RamdomResolver(self.probDef)



class SeqencialResolver(Resolver): #20.000

   def __init__(self, probDef, listAll = None):
     self.probDef = probDef
     self.listAll = listAll or list( combinaison_with_doublon_and_order( list(range(probDef.nbElements)), probDef.nbPlaces) )
     self.curId = -1

   def getNextTrie(self):
     self.curId += 1	
     return self.listAll[self.curId]
   
   def __call__(self): return SeqencialResolver(self.probDef, self.listAll)



class FilterResolver(Resolver): #8

   def __init__(self, probDef, listAll = None):
     self.probDef = probDef
     self.listAll = listAll or list( combinaison_with_doublon_and_order( list(range(probDef.nbElements)), probDef.nbPlaces) )
     self.curList = self.listAll
     print len(self.listAll)

   def __call__(self): return FilterResolver(self.probDef, self.listAll)

   def getNextTrie(self):
     return choice(self.curList)

   def setTrieResult(self, tryContent, number):
     self.curList = [e for e in self.curList if nbDiff(tryContent, e) == number]


#I could have done an algorythme to split the self.listAll by 6*6*6*6*6*6 part equals
#But the FilterResolver is good








if __name__ == "__main__":

  #d = ProblemDefinition(6, 6, 10)
  #d = ProblemDefinition(6, 6, 10, ['Tree','Butterfly','Turtle','Moon','Fire','Square'])
  d = ProblemDefinition(4, 8, 10, ['Red', 'Green', 'Blue', 'Yellow', 'Marron', 'Orange', 'Black', 'White']) #mastermind

  #prob = FixedProblem([5, 1, 0, 5, 0, 5])
  #prob = RandomProblem(d)
  prob = HumainProblem(d)
  
  #reso = RandomResolver(d)
  #reso = FixedResolver([5, 1, 0, 5, 0, 5])
  #reso = SeqencialResolver(d)
  reso = FilterResolver(d)

  res = ProbWithResolv.medianOn(20, prob, reso, d)
  print "%s / %s" % (res, d.getCombi())

  print "__EOF__"



#__EOF__
