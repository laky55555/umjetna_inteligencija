from copy import deepcopy
from collections import deque
import sys
import time

class State:
    def __init__(self,Polje, b):
        self.polje = Polje
        self.b = b
    def successors(self):
        if self.b == 0:
            sgn = 1
            direction = " from the new shore to the beginnig shore"
        else:
            sgn = -1
            direction = " from the first shore to the new shore"
        for i in range (6):
             novi = []
             novi.extend(self.polje)
             novi[i] = novi[i]+sgn
             if novi[i] > 1 or novi[i] < 0:
                 continue
             newState = State(novi, self.b+sgn)
             #action = (novi, direction, newState)
             if newState.isValid():
                 action = (novi, direction, newState)
                 #print novi
                 yield newState,action
             for j in range (i+1,6):
                 novi1 = []
                 novi1.extend(novi)
                 novi1[j] = novi[j]+sgn
                 if novi1[j] > 1 or novi1[j] < 0:
                     continue
                 if (i == 0 and j ==3) or (i == 0 and j == 5) or (i ==1 and j ==2) or (i == 1 and j == 4) or ( i == 2 and j ==5) or (i ==3 and j ==4) :
                     continue
                 newState = State(novi1, self.b+sgn)
                 #action = (novi1, direction, newState)
                 if newState.isValid():
                    action = (novi1, direction, newState)
                    #print novi1
                    yield newState,action



    def isValid(self):
          #ako je zena1 bez muza1 u prisustvu nekog drugog decka
         if self.polje[1] != self.polje[0] and(self.polje[1] == self.polje[2] or self.polje[1] == self.polje[4]):
             #print "tu1"
             #print self.polje
             return False
         if self.polje[3] != self.polje[2] and(self.polje[3] == self.polje[0] or self.polje[3] == self.polje[4]):
             #print "tu2"
             #print self.polje
             return False
         if self.polje[5] != self.polje[4] and(self.polje[5] == self.polje[2] or self.polje[5] == self.polje[0]):
             #print "tu3"
             #print self.polje
             return False
         return True


    def is_goal_state(self):
        return self.polje[0] == 0 and self.polje[1] == 0 and self.polje[2] == 0 and self.polje[3] == 0 and self.polje[4] == 0 and self.polje[5] == 0 and self.b == 0

    def __repr__(self):
        return "<State (%d,%d, %d, %d, %d, %d, %d)" %(self.polje[0], self.polje[1], self.polje[2], self.polje[3], self.polje[4], self.polje[5], self.b)

class Node:
    def __init__(self, parent_node, state,action, depth):
        self.parent_node = parent_node
        self.state = state
        self.action = action
        self.depth = depth
    def expand(self):
        for (succ_state, succ_action) in self.state.successors():
            succ_node = Node(parent_node = self,
                             state = succ_state,
                             action = succ_action,
                             depth = self.depth+1)
            yield succ_node
    def extract_solution(self):
        solution = []
        node = self
        while node.parent_node is not None:
            solution.append(node.action)
            node = node.parent_node
        solution.reverse()
        return solution

def breadth_first_tree_search(initial_state):
  initial_node = Node(
                      parent_node=None,
                      state=initial_state,
                      action=None,
                      depth=0)
  fifo = deque([initial_node])
  num_expansions = 0
  max_depth = -1
  while True:
    if not fifo:
      print ("%d expansions" % num_expansions)
      return None
    node = fifo.popleft()
    if node.depth > max_depth:
      max_depth = node.depth
      print ("[depth = %d] %.3fs" % (max_depth, time.clock()))
    if node.state.is_goal_state():
      print ("%d expansions" % num_expansions)
      solution  = node.extract_solution()
      return solution
    num_expansions += 1
    fifo.extend(node.expand())

def main():
      polje = [1,1,1,1,1,1]
      initial_state = State(polje,1)
      for solution in breadth_first_tree_search(initial_state):
          if solution is None:
            print ("no solution")
          else:
            print ("solution (%d steps):" % len(solution), end=" ")
            for step in solution:
              print (step)
      print ("elapsed time: %.2fs" % time.clock())
main()
