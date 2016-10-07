import copy
import random
from math import *

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of player_na_potezu.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.player_na_potezu = state.player_na_potezu # the only part of the state that the Node needs later
        self.bodovi=state.bodovi
        self.prvi_igrac = state.player_na_potezu
    #ne treba nicemo nista radit s tom listom TREBA    
        #pricaj tamo 
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        maxNode = None
        maxi = -1.0
        mini = 1.1
        minNode=None
        #moramo vratiti cvor koji je najbolji iz perspektive roditelja
        #biramo dijete koje nam je donijelo najvise pobjeda
        for i in range (len(self.childNodes)):
            if(maxi < float(self.childNodes[i].wins)/float(self.childNodes[i].visits)+ sqrt(2*log(self.visits)/self.childNodes[i].visits)):
                maxNode = self.childNodes[i]
                maxi = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)+sqrt(2*log(self.visits)/self.childNodes[i].visits)
            """#zelimo najveci umjer u kojem pobjedjuje komp ili najmanjii omjer u kojem pobjedjuje covjek
            if(maxi<float(self.childNodes[i].wins)/float(self.childNodes[i].visits)and self.childNodes[i].player_na_potezu == 2):
                maxi = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)
                maxNode = self.childNodes[i]
            if(mini>float(self.childNodes[i].wins)/float(self.childNodes[i].visits)and self.childNodes[i].player_na_potezu == 1):
                mini = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)
                minNode = self.childNodes[i]
        #print mini
        #print maxi
        if(1-mini>maxi):
            return minNode
        else:
            return maxNode"""
        #print "U SELCET CHILD "+str(maxi)
        
        return maxNode
       
        
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of player_na_potezu.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"+"potez igra "+str(self.player_na_potezu)

    def TreeToString(self, indent):
        #ovo je ako zelimo ispisati citav score po potezima UCT-a
        """s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s"""

        #ovo je ako zelimo ispisati samo stablo do dubine 1
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.IndentString(indent+1)+ str(c)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def UCT(rootstate, itermax, verbose = False, brojac=-1):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)
    pobjednik = rootstate.pobjednik
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        j = brojac
        j=brojac
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            #print state.print1()+" "+str(node.move)+" select"
            state.DoMove(node.move)
            j+=1            

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            #print state.print1()+" "+str(node.move)+" expand "+str(j)
            state.DoMove(m)
            j+=1
            node = node.AddChild(m,state) # add child and descend tree
            
            
        
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            izbacujem_kartu = random.choice(state.GetMoves())
            #print state.print1()+str(node.move)+" rollout"
            state.DoMove(izbacujem_kartu)
            j+=1

            
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            #print str(node.player_na_potezu)+" je prosao s "+str(state.GetResult(node.player_na_potezu))
            if(node.parentNode!=None):
                node.Update(state.GetResult(node.parentNode.player_na_potezu)) # state is terminal. Update node with result from POV of node.player_na_potezu
            else:
                node.Update(state.GetResult(1))
            node = node.parentNode
            
        #print "na kraju iteracije j je "+str(j)
       
    if (verbose==False): print rootnode.TreeToString(0)
    #else: print rootnode.ChildrenToString()
    
    
    # Output some information about the tree - can be omitted
    #print "prosli smo"+str(j)
    

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited






###Koristimo Node2 i UCT2 kod provjere UCT_vs_UCT s razlicitim koeficijentima
###treba promijeniti koeficijent u UCTSelectChild ispred sqrt

class Node2:
    """ A node in the game tree. Note wins is always from the viewpoint of player_na_potezu.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.player_na_potezu = state.player_na_potezu # the only part of the state that the Node needs later
        self.bodovi=state.bodovi
        self.prvi_igrac = state.player_na_potezu
    #ne treba nicemo nista radit s tom listom TREBA    
        #pricaj tamo 
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        maxNode = None
        maxi = -1.0
        mini = 1.1
        minNode=None
        #moramo vratiti cvor koji je najbolji iz perspektive roditelja
        #biramo dijete koje nam je donijelo najvise pobjeda
        for i in range (len(self.childNodes)):
            if(maxi < float(self.childNodes[i].wins)/float(self.childNodes[i].visits)+ 100*sqrt(1*log(self.visits)/self.childNodes[i].visits)):
                maxNode = self.childNodes[i]
                maxi = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)+100*sqrt(1*log(self.visits)/self.childNodes[i].visits)
            """#zelimo najveci umjer u kojem pobjedjuje komp ili najmanjii omjer u kojem pobjedjuje covjek
            if(maxi<float(self.childNodes[i].wins)/float(self.childNodes[i].visits)and self.childNodes[i].player_na_potezu == 2):
                maxi = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)
                maxNode = self.childNodes[i]
            if(mini>float(self.childNodes[i].wins)/float(self.childNodes[i].visits)and self.childNodes[i].player_na_potezu == 1):
                mini = float(self.childNodes[i].wins)/float(self.childNodes[i].visits)
                minNode = self.childNodes[i]
        #print mini
        #print maxi
        if(1-mini>maxi):
            return minNode
        else:
            return maxNode"""
        #print "U SELCET CHILD "+str(maxi)
        
        return maxNode
       
        
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of player_na_potezu.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"+"potez igra "+str(self.player_na_potezu)

    def TreeToString(self, indent):
        #ovo je ako zelimo ispisati citav score po potezima UCT-a
        """s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s"""

        #ovo je ako zelimo ispisati samo stablo do dubine 1
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.IndentString(indent+1)+ str(c)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


###Koristimo Node2 i UCT2 kod provjere UCT_vs_UCT s razlicitim koeficijentima
###treba promijeniti koeficijent u UCTSelectChild ispred sqrt
    
def UCT2(rootstate, itermax, verbose = False, brojac=-1):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node2(state = rootstate)
    pobjednik = rootstate.pobjednik
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        j = brojac
        j=brojac
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            #print state.print1()+" "+str(node.move)+" select"
            state.DoMove(node.move)
            j+=1            

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            #print state.print1()+" "+str(node.move)+" expand "+str(j)
            state.DoMove(m)
            j+=1
            node = node.AddChild(m,state) # add child and descend tree
            
            
        
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            izbacujem_kartu = random.choice(state.GetMoves())
            #print state.print1()+str(node.move)+" rollout"
            state.DoMove(izbacujem_kartu)
            j+=1

            
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            #print str(node.player_na_potezu)+" je prosao s "+str(state.GetResult(node.player_na_potezu))
            if(node.parentNode!=None):
                node.Update(state.GetResult(node.parentNode.player_na_potezu)) # state is terminal. Update node with result from POV of node.player_na_potezu
            else:
                node.Update(state.GetResult(1))
            node = node.parentNode
            
        #print "na kraju iteracije j je "+str(j)
       
    if (verbose==False): print rootnode.TreeToString(0)
    #else: print rootnode.ChildrenToString()
    
    
    # Output some information about the tree - can be omitted
    #print "prosli smo"+str(j)
    

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited



             
