#!/usr/bin/env python

#The goal to 

levels = { #line lenght, map, num touch
  '96': (5, "XX X X XXX  XXX  X    XX ", 14),
  '92': (5, "  XXX     X    XXXX  X   ", 14),
  '82': (5, "XX X   XXXX XXX XX XX  X ", 9),
  '49': (5, "X X X XX  X XXXX   X X   ", 8),

  'test':(5, "   X X XXXXX X X         ", 2),
}


#The first thought is to have a list of 14 step.
#The complexity is 25^14. 37252902984619140625 : Way too much.
#
#The second thought is that the order don't import
#It's only 14 places in the field
#Places can't be twice the same, il would be counter intuitive
#We select the first, then the second from unocupied places
#The complexity is 25! / 14!, too much too : 388588515194880000
#
#The third thought is that multiples times the same result will come from the last try
#You have to select the next element from the places after the one selected before
#The qte is : 4457400 (14 permutation in 25), more managable

#If the computer can't find a solution, we will try with multiples elements per place
#But I think it will be easier to just do the same with less step avaiable

def genSteps(size, qtleft, limit = 0, res = []):
  if qtleft == 0: return [res]
  curResult = []
  for p in range(limit, size - qtleft + 1):
    curResult += genSteps(size, qtleft - 1, p + 1, res + [p])
  return curResult

   
def chunks(l, n): return [l[i:i+n] for i in range(0, len(l), n)]



class LightMap:

  def __init__(self, lineLen, start, pos):
    assert (len(start) % lineLen) == 0

    self.content = self.cleanMap(chunks(start, lineLen))
    self.solution = self.cleanMap(chunks([' ' for e in start], lineLen))

    self.size = (lineLen, len(self.content))

    #slow
    self.steps = self._genSteps(len(start), pos)

  def cleanMap(self, cur_map):
    return [[False if e == ' ' else True for e in line] for line in cur_map]

  def _genSteps(self, size, qtleft, limit = 0, res = []):
    if qtleft == 0: return [res]
    curResult = []
    for p in range(limit, size - qtleft + 1):
      curResult += self._genSteps(size, qtleft - 1, p + 1, res + [p])
    return curResult


  def printMap(self, m = None):
    for line in (m or self.content):
      for cell in line:
        print ' ' + ('O' if cell else '.'),
      print ''


class ApplyStep:

  def __init__(self, lightMap, steps):
    self.lm = lightMap
    self.content = [[e for e in line] for line in lightMap.content]
    self.sizeX, self.sizeY = self.lm.size
    self.steps = [(e % self.sizeX, e / self.sizeX) for e in steps]
  
  def applyMe(self):
    for e in self.steps: self.applyOne(e)

  def applyOne(self, (x, y)):
    self.change((x, y))
    self.change((x+1, y))
    self.change((x-1, y))
    self.change((x, y+1))
    self.change((x, y-1))

  def change(self, (x, y)):
    if not (0 <= x < self.sizeX): return
    if not (0 <= y < self.sizeY): return
    self.content[y][x] = not(self.content[y][x])

  def isGood(self):
    return self.content == self.lm.solution


if __name__ == "__main__":
  lm = LightMap(*levels['96'])
  lm.printMap()
  print "###################"

  for s in lm.steps:
    #raw_input('#############')
    aps = ApplyStep(lm, s)
    aps.applyMe()
    #print aps.steps
    #lm.printMap(aps.content)
    #print aps.isGood()
    if aps.isGood():
      print(aps.steps)
      break





















