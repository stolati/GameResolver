#!/usr/bin/env python

level71=(4, '*', "7122334*564*56008800", "************00**00**", []) #line len, empty, start, solution
level39=(4, '*', "0011002234**56775688", "************00**00**", []) #line len, empty, start, solution
level46=(4, '*', "1223455367**67008800", "************00**00**", ['582', '673']) #line len, empty, start, solution
level56=(4, '*', "10021002355637864**9", "*************00**00*", ['1236', '4789']) #line len, empty, start, solution, are sames

level79=(4, '*', "1008300937*947*A5566", "*************00**00*", ['18A4', '397', '56']) #line len, empty, start, solution, are sames
level88=(4, '*', "*00*1002355836684779", "*************00**00*", ['1249', '567', '38'])
level98=(4, '*', "1456170027002889**33", "*************00**00*", ['4569', '127', '83'])


#First version : {'level':56, 'steps':50, 'elements':17432, 'time':'38s'}
#Second version : {'level':56, 'steps':50, 'elements':440, 'time':'1.467s'}








def chunks(l, n): return [l[i:i+n] for i in range(0, len(l), n)]

class SlideMap:
  def __init__(self, lineLen, empty, start, solution, sames = []):
    assert len(start) == len(solution)
    assert (len(start) % lineLen) == 0
    
    self.content = self.cleanMap(chunks(start, lineLen), empty)
    self.solution = self.cleanMap(chunks(solution, lineLen), empty)
    self.forms = []
    self.sames = sames

    for line in self.content:
      for cell in line:
        if cell in self.forms: continue
        if cell == None: continue
        self.forms.append(cell)

    self.size = (lineLen, len(self.content))


  def cleanMap(self, cur_map, empty):
    return [[None if e == empty else e for e in line] for line in cur_map]


  def printMap(self, cur_map):
    for line in cur_map:
      for cell in line:
        if cell == None:
          print "  ",
        else:
          print cell + " ",
      print "\n",


  def getCloseMaps(self, cur_map):
    res = []
    for elem in self.forms:
      for move in [(1,0), (0,1), (-1,0), (0,-1)]:
        tmpRes = self.move(cur_map, elem, move)
        if tmpRes != None: res.append(tmpRes)

    return res


  def move(self, cur_map, elem, pos):
    sizeX, sizeY = self.size
    moveX, moveY = pos
    cur_map = [list(l) for l in cur_map] #copy the list
    
    for posX in range(sizeX)[:: -(moveX or 1)]:
      for posY in range(sizeY)[:: -(moveY or 1)]:
        curElem = cur_map[posY][posX]
        if elem != curElem: continue

        newPosX, newPosY = (posX + moveX, posY + moveY)
 
        if not (sizeX > newPosX > -1): return None #get out of limits
        if not (sizeY > newPosY > -1): return None #get out of limits
                
        newElem = cur_map[newPosY][newPosX]
        if newElem != None: return None #have a block in the way

        cur_map[newPosY][newPosX] = curElem
        cur_map[posY][posX] = None
        
    return cur_map
        


  def compare(self, cur_map):
    sizeX, sizeY = self.size

    for posX in range(sizeX):
      for posY in range(sizeY):
        solutionElem = self.solution[posY][posX]
        if solutionElem == None: continue
        curElem = cur_map[posY][posX]
        if solutionElem == curElem: continue
        return False
    return True

  def genHash(self, cur_map):
    return ''.join([''.join([self.simplifyElemForHash(l) for l in e]) for e in cur_map])


  def simplifyElemForHash(self, e):
    if e == None: return ' '
    for l in self.sames:
      if e in l: return l[0]
    return e


class Path:
  def __init__(self, parent, state):
    self.parent = parent
    self.state = state

  def children(self, state):
    return Path(self, state)

  def childrens(self, states):
    return [self.children(s) for s in states]

  def depile(self):
    if self.parent == None: return []
    return self.parent.depile() + [self.state]


def getAllChildrens(statesPath, slideMap):
  res = []
  for p in statesPath:
    res += p.childrens(slideMap.getCloseMaps(p.state))
  return res


class HashPath:
  def __init__(self):
    self.hash = {}

  def add(self, elemHash):
    if elemHash in self.hash: return False
    self.hash[elemHash] = None
    return True

def processChildrens(hashPath, allChildrens, slideMap):
  return [c for c in allChildrens if hashPath.add(slideMap.genHash(c.state))]

def findSucess(allChildrens, slideMap):
  return [c for c in allChildrens if slideMap.compare(c.state)]


if __name__ == "__main__":
  sm = SlideMap(*level98)
 
  hp = HashPath()
  allPaths = [Path(None, sm.content)]
  allPaths = processChildrens(hp, allPaths, sm)
  sucess = None

  print "####################"
  print "####################"
  print "####################"

  for i in range(1000):
    print "%s (%s)" % (i, len(allPaths))
    allPaths = getAllChildrens(allPaths, sm)
    allPaths = processChildrens(hp, allPaths, sm)
    sucess = findSucess(allPaths, sm)
    if sucess:
      sucess = sucess[0].depile()
      break

  if sucess:
    for e in sucess:
      raw_input('#################')
      sm.printMap(e)


#__EOF__
