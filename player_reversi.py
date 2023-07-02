import random
import copy
'''
Literature:
http://pressibus.org
https://othellomaster.com
https://samsoft.org.uk/reversi
https://www.coolmathgames.com

'''
BLACK=0
WHITE=1
EMPTY=-1
DIRACTION=[[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]
INFINITH = 214748364
#N:  size of board
N=8
#EVAL_BOARD : a board with an assessment of each position
EVAL_BOARD=[ [10000, -3000, 1000, 800, 800, 1000, -3000, 10000], 
            [-3000, -5000, -450, -500, -500, -450, -5000, -3000], 
            [1000, -450, 30, 10, 10, 30, -450, 1000], 
            [800, -500, 10, 50, 50, 10, -500, 800], 
            [800, -500, 10, 50, 50, 10, -500, 800], 
            [1000, -450, 30, 10, 10, 30, -450, 1000], 
            [-3000, -5000, -450, -500, -500, -450, -5000, -3000], 
            [10000, -3000, 1000, 800, 800, 1000, -3000, 10000] ]
#MAX_DEPTH: depth for alpha-beta pruning
MAX_DEPTH =3
# K:Account significance coefficient
K=10


class MyPlayer:
    '''Player is playing with using alpha-beta pruning'''
    def __init__(self,my_color,opponent_color):
        self.name= 'pimenol1'
        self.my_color=my_color
        self.opponent_color=opponent_color
        # actual_move: The move I can make in this round
        self.actual_move=[]

    def move(self,board):
        self.board=board
        list_moves=self.possible_moves(board,self.my_color, self.opponent_color)
        if len(list_moves)==0:
            return None
        maxEval=-INFINITH
        for r,c in list_moves:
            self.actual_move=[r,c]
            new_board= self.make_move(r,c, copy.deepcopy(board),self.my_color, self.opponent_color)
            eval=self.alphaBeta_serch(new_board,MAX_DEPTH,maxEval, +INFINITH, True)
            if eval >maxEval:
                maxEval=eval
                maxr=r
                maxc=c
        return (maxr, maxc)
            
    def on_the_board(self,r,c):
        '''True: if position on the board, else False'''
        return r>=0 and c>=0 and r<=7 and c<=7

    def is_move_correct(self, r, c, board, my_color,opponent_color):
        '''Return True if this is correct move '''
        if(board[r][c]!=EMPTY or not self.on_the_board(r,c)):
            return False
        for r_dir, c_dir in DIRACTION:
            #rtmp and ctmp: temporary variables for serching in all possible direction
            rtmp=r+r_dir
            ctmp=c+c_dir
            if self.on_the_board(rtmp,ctmp) and board[rtmp][ctmp]==opponent_color :
                while board[rtmp][ctmp]==opponent_color:
                    rtmp+=r_dir
                    ctmp+=c_dir
                    if not self.on_the_board(rtmp,ctmp):
                        break
                if not self.on_the_board(rtmp,ctmp):
                    continue
                if board[rtmp][ctmp]==my_color:
                    return True
        return False
        
    def possible_moves(self, board,my_color,opponent_color):
        '''Return all possible moves for "my_color" '''
        list_moves=[]
        for i in range(N):
            for j in range(N):
                if self.is_move_correct(i, j, board,my_color,opponent_color)==True:
                    list_moves.append([i,j])
        return list_moves

    def eval_board(self, board):
        '''
        my_score: count number of squares at board for me
        op_score: count number of squares at board for opponent
        return: difference between numbers
        '''
        my_score=0
        op_score=0
        for x in range(N):
            for y in range(N):
                if board[x][y]== self.my_color:
                    my_score+=1
                elif board[x][y]==self.opponent_color:
                    op_score+=1
        return my_score - op_score
                    
        
                                          
    def make_move(self, r, c, board, my_color, opponent_color):
        '''Makes a move [r.c] at board'''
        board[r][c]=my_color
        for r_dir, c_dir in DIRACTION:
            # rtmp and ctmp: temporary variables for serching in all possible direction
            rtmp=r+r_dir
            ctmp=c+c_dir
            # counter: how much square will be flipped
            counter=1
            if self.on_the_board(rtmp,ctmp) and board[rtmp][ctmp]==opponent_color :
                while board[rtmp][ctmp]==opponent_color:
                    rtmp+=r_dir
                    ctmp+=c_dir
                    counter+=1
                    if not self.on_the_board(rtmp,ctmp):
                        break
                if not self.on_the_board(rtmp,ctmp):
                    continue
                if board[rtmp][ctmp]==my_color:
                    # shoudn't flip my square
                    counter-=1
                else: counter=0
            for i in range(counter):
                # go back and flip
                ctmp -= c_dir
                rtmp -= r_dir
                board[rtmp][ctmp] = self.my_color
        return board
          
    def alphaBeta_serch(self, board, depth, alpha, beta, player):
        '''
        How work alpha-beta pruning:
        https://www.youtube.com/watch?v=l-hh51ncgDI
        '''
        if depth==0 :
            '''
            To the difference in the number of my squares 
            and the opponent's squares multiplied by K, I add an estimate 
            of the position of the move that can be made in round
            '''
            return self.eval_board(board)*K + EVAL_BOARD[self.actual_move[0]][self.actual_move[1]]
        if player:
            list_moves=self.possible_moves(board, self.my_color, self.opponent_color)
            if len(list_moves)==0:
                return self.eval_board(board)*K + EVAL_BOARD[self.actual_move[0]][self.actual_move[1]]
            for x,y in list_moves:
                new_board= self.make_move(x, y,copy.deepcopy(board), self.my_color, self.opponent_color)
                eval=self.alphaBeta_serch(new_board, depth-1, alpha, beta, False)
                alpha= max(eval,alpha)
                if alpha >= beta:
                    return alpha
            return alpha
        else:
            list_moves=self.possible_moves(board, self.opponent_color, self.my_color)
            if len(list_moves)==0:
                return self.eval_board(board)*K + EVAL_BOARD[self.actual_move[0]][self.actual_move[1]]
            for x,y in list_moves:
                new_board= self.make_move(x, y,copy.deepcopy(board), self.opponent_color, self.my_color)
                eval=self.alphaBeta_serch(new_board, depth-1, alpha, beta, True)
                beta=min(beta,eval)
                if beta<=alpha:
                    return beta
            return beta
        
