"""Games, or Adversarial Search. (Chapter 5)
"""

from utils import *
import random
import time

#______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a)))

#______________________________________________________________________________

def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Fig. 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity))

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    return argmax(game.actions(state),
                  lambda a: min_value(game.result(state, a),
                                      -infinity, infinity, 0))

#______________________________________________________________________________
# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))

def alphabeta_player(game, state):
    return alphabeta_search(state, game)

def play_game(game, *players):
    """Play an n-person, move-alternating game.
    >>> play_game(Fig52Game(), alphabeta_player, alphabeta_player)
    3
    """
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                return game.utility(state, game.to_move(game.initial))

#______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

class Fig52Game(Game):
    """The game represented in [Fig. 5.2]. Serves as a simple test case.
    >>> g = Fig52Game()
    >>> minimax_decision('A', g)
    'a1'
    >>> alphabeta_full_search('A', g)
    'a1'
    >>> alphabeta_search('A', g)
    'a1'
    """
    succs = dict(A=dict(a1='B', a2='C', a3='D'),
                 B=dict(b1='B1', b2='B2', b3='B3'),
                 C=dict(c1='C1', c2='C2', c3='C3'),
                 D=dict(d1='D1', d2='D2', d3='D3'))
    utils = Dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)
    initial = 'A'

    def actions(self, state):
        return self.succs.get(state, {}).keys()

    def result(self, state, move):
        return self.succs[state][move]

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A', 'B', 'C', 'D')

    def to_move(self, state):
        return if_(state in 'BCD', 'MIN', 'MAX')

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=4, v=4, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return if_(player == 'X', state.utility, -state.utility)

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y-1) in state.board]

__doc__ += random_tests("""
>>> play_game(Fig52Game(), random_player, random_player)
6
>>> play_game(TicTacToe(), random_player, random_player)
0
""")

def ispis(broj_pobjeda_prvog, broj_pobjeda_drugog, broj_nerjesenih, broj_rundi, broj_partija, pocetak, kraj):
    print ("Prosjecan broj pobjeda:")
    print ( "Pobjeda prvog je u %.3f%% slucajeva" % ((sum(broj_pobjeda_prvog)*100)/float(broj_rundi*broj_partija)) )
    print ( "Pobjeda drugog je u %.3f%% slucajeva" % ((sum(broj_pobjeda_drugog)*100)/float(broj_rundi*broj_partija)) )
    print ( "Nerjeseno je u %.3f%% slucajeva\n" % ((sum(broj_nerjesenih)*100)/float(broj_rundi*broj_partija)) )

    print("Srednji broj pobjeda po rundama:")
    print ( "Pobjeda prvog je u %.3f%% slucajeva" % ((median(broj_pobjeda_prvog)*100)/float(broj_partija)) )
    print ( "Pobjeda drugog je u %.3f%% slucajeva" % ((median(broj_pobjeda_drugog)*100)/float(broj_partija)) )
    print ( "Nerjeseno je u %.3f%% slucajeva\n" % ((median(broj_nerjesenih)*100)/float(broj_partija)) )
    print ( "Vrijeme potrebno za izvrsavanje je: %.3f sekundi." % (kraj - pocetak)) 
    print ("_____________________________________________________\n")


def igranje(h,v,k,broj_rundi,broj_partija, prvi_igrac, drugi_igrac):
    """A TicTacToe-like game, velicina polja (AxB) potrebnih u nizu za pobijedu, broj rundi, broj partija, prvi igrac, drugi igrac"""
    #print ("Ploca 3x3, prvi igrac je %s, a drugi %s. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (prvi_igrac, drugi_igrac, k, broj_rundi, broj_partija))
    pocetak = time.time()
    broj_pobjeda_prvog = []
    broj_pobjeda_drugog = []
    broj_nerjesenih = []
    for i in range(broj_rundi):
        prvi_pobjedio = 0
        drugi_pobjedio = 0
        nerjeseno = 0
        for j in range(broj_partija):
            pobjednik = play_game(TicTacToe(h,v,k), prvi_igrac, drugi_igrac)
            if(pobjednik  == 1):
                prvi_pobjedio += 1
            elif(pobjednik  == -1):
                drugi_pobjedio += 1
            else:
                nerjeseno += 1
        broj_pobjeda_prvog.append(prvi_pobjedio)
        broj_pobjeda_drugog.append(drugi_pobjedio)
        broj_nerjesenih.append(nerjeseno)
    kraj = time.time()
    ispis(broj_pobjeda_prvog, broj_pobjeda_drugog, broj_nerjesenih, broj_rundi, broj_partija, pocetak, kraj)
    

def main():

    #funkcija igranje() pokrece igru
    #Upisuje se velicina ploce, broj potrebnih u nizu za pobjedu, broj rundi koliko ce se vrtiti, broj partija po svakoj rundi, te vrste igraca
    print ("Nakon nekoliko testova, dobio sam slijedece zanimljive rezultate:")
    print ("Moze se zakljucit, kod igranja 4x4 gdje je niz od 3 pobjednicki gotovo nikad nema neodlucenog rezultata")
    print ("Kad alphabeta igra prvi protiv random igraca, onda nikad ne gubi, te neodlucenih rezlutata bude samo kod 4x4 ploce s pobjednickim nizom 4")
    print ("Kad alphabeta igra prvi protiv random igraca, vrijeme izvrsavanja za 4x4 tablu u kojoj niz od 3 pobjeduje je mnogo vece od ostalih")
    print ("Kad alphabeta igra drugi protiv random igraca, gotovo uvijek pobjeduje, iako u nesto manjem postotku nego kad igra prvi")
    print ("Kad alphabeta igra prvi protiv alphabeta, onda za plocu 4x4 s nizom 3 za pobjedu prvi uvijek pobjedi, inace uvijek bude neodluceno")
    print ("Kad je niz potreban za pobjedu manji od dimenzije ploce, optimalne igre vodit ce do pobjednika, koji nije uvijek prvi igrac. Npr. za igru 5x5 s nizom 4 za pobjedu")
    print ("Ukupno vrijeme izvrsavanja je oko 4 minute.\n\n")
    time.sleep(8)
    

    pocetak_programa = time.time()
    print("Igre izmedu random igraca:\n")
    print ("1) Ploca %dx%d, oba igraca su random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (3,3,3, 10, 50))
    igranje(3,3,3,10,50, random_player,random_player)

    print ("2) Ploca %dx%d, oba igraca su random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,3, 10, 50))
    igranje(4,4,3,10,50, random_player,random_player)

    print ("3) Ploca %dx%d, oba igraca su random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,4, 10, 50))
    igranje(4,4,4,10,50, random_player,random_player)

    print("Igre izmedu random i alphabeta igraca\n")
    print ("1) Ploca %dx%d, prvi igrac je alphabeta_player, a drugi random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (3,3,3, 10, 20))
    igranje(3,3,3,10,20, alphabeta_player,random_player)

    print ("2) Ploca %dx%d, prvi igrac je alphabeta_player, a drugi random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,3, 5, 5))
    igranje(4,4,3,5,5, alphabeta_player,random_player)

    print ("3) Ploca %dx%d, prvi igrac je alphabeta_player, a drugi random_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,4, 5, 5))
    igranje(4,4,4,5,5, alphabeta_player,random_player)
    
    print ("1) Ploca %dx%d, prvi igrac je random_player, a drugi alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (3,3,3, 10, 20))
    igranje(3,3,3,10,20, random_player,alphabeta_player)

    print ("2)Ploca %dx%d, prvi igrac je random_player, a drugi alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,3, 5, 5))
    igranje(4,4,3,5,5, random_player,alphabeta_player)

    print ("3) Ploca %dx%d, prvi igrac je random_player, a drugi alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,4, 5, 5))
    igranje(4,4,4,5,5, random_player,alphabeta_player)

    print("Igre izmedu alphabeta igraca:\n")
    print ("1) Ploca %dx%d, oba igraca su alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (3,3,3, 10, 10))
    igranje(3,3,3,10,10, alphabeta_player,alphabeta_player)

    print ("2) Ploca %dx%d, oba igraca su alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,3, 4, 4))
    igranje(4,4,3,4,4, alphabeta_player,alphabeta_player)

    print ("3) Ploca %dx%d, oba igraca su alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (4,4,4, 4, 4))
    igranje(4,4,4,4,4, alphabeta_player,alphabeta_player)

    print ("4) Ploca %dx%d, oba igraca su alphabeta_player. Pobjednik je onaj koji ostvari %d u nizu.\nIgra se %d rundi po %d partija\n" % (5,5,4, 1, 1))
    igranje(5,5,4,1,1, alphabeta_player,alphabeta_player)


    kraj_programa = time.time()
    print ("Ukupno vrijeme izvrsavanja programa je %.3f sekundi.\n" % (kraj_programa-pocetak_programa))


if __name__ == "__main__":
  main()
