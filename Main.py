import random
import math
import time

class Grid:
    def __init__(self,Rows,Column,RandomGen=True,Board=[]):
        self.Board=Board
        self.Rows=Rows
        self.Column=Column
        if RandomGen:
            for X in range(0,Column):
                Row=[]
                for Y in range(0,Rows):
                    if random.randint(0,100) < 30:
                        Row.append(-1)
                    else:
                        Row.append(1)
                self.Board.append(Row)


class AStar:
    def __init__(self,Board,HWeight=1,CWeight=1,AllowDiagonals=False):
        self.Board={}
        self.AgentLocation=(0,0)
        self.HWeight=HWeight
        self.CWeight=CWeight
        self.AllowDiagonals=AllowDiagonals
        self.Rows=Board.Rows
        self.Columns=Board.Column
        
        for Y,F in enumerate(Board.Board):
            for X,G in enumerate(F):
                self.Board[(X,Y)]={"Cost":G,"Traveled":False,"Prevous":(-1,-1)}
    
    def GetCandidates(self):
        Candidates={}
        
        for Y in [-1,0,1]:
            for X in [-1,0,1]:
                if ((X != 0 or Y != 0) and self.AllowDiagonals) or ((X == 0 or Y == 0) and (X != 0 or Y != 0) and not self.AllowDiagonals):
                    if self.AgentLocation[0] + X >= 0 and self.AgentLocation[0] + X < self.Rows and  self.AgentLocation[1] + Y >= 0 and self.AgentLocation[1] + Y < self.Columns:
                        Check=self.Board[(self.AgentLocation[0] + X,self.AgentLocation[1] + Y)]
                        #print(Check)
                        if Check["Cost"] != -1 and Check["Traveled"] == False:
                            Candidates[(self.AgentLocation[0] + X, self.AgentLocation[1] + Y)]=Check["Cost"]
        return Candidates

    def Hurestic(self,Pos):
        DX=Pos[0] - self.Target[0]
        DY=Pos[1] - self.Target[1]
        return math.sqrt(DX ** 2 + DY ** 2)


    def PrintBoard(self):

        Out=[[" " for X in range(0,self.Columns)] for Y in range(0,self.Rows)]
        #print(Out)
        for A,B in self.Board.items():
            Item=""
            if B["Traveled"] == True:
                Item="🟥"
            elif B["Cost"] == -1:
                Item="⬛"
            else:
                Item="⬜"
            

            Out[A[1]][A[0]]=Item
        
        Path=self.CompilePath()
        for A in Path:
            Out[A[1]][A[0]]="🟩"
        for X in range(0,len(Out)):
            Out[X]="".join(Out[X])
        print("\n".join(Out) + "\n")

    def CompilePath(self):
        Path=[]
        Pos=self.AgentLocation
        Path.append(Pos)
        while True:
            Item=self.Board[Pos]
            if Item["Prevous"] == (-1,-1):
                return Path
            else:
                Path.append(Item["Prevous"])
                Pos=Item["Prevous"]
        
            

    def RunPathFind(self,Target,PrintBoard=True):
        self.Target=Target
        StartDistance=self.Hurestic(self.AgentLocation)
        Count=0
        while True:
            Count+=1
            Candidates=self.GetCandidates()
            #print(Candidates)
            if len(Candidates) == 0:

                #DoBackProp
                if self.AgentLocation == (-1,-1):
                    return False
                self.Board[self.AgentLocation]["Traveled"]=True
                
                self.AgentLocation=self.Board[self.AgentLocation]["Prevous"]
                #print(":()")
                #pass
            else:
                if PrintBoard:
                    self.PrintBoard()
                #print("1")
                for A,B in Candidates.items():
                    Huristic=self.Hurestic(A)
                    #print(Huristic)
                    #print(Candidates[A])
                    Candidates[A]=(B * self.CWeight) + ((Huristic - StartDistance) * self.HWeight)
                #print("2")
                Candidates=sorted(Candidates.items(), key=lambda x:x[1])
                NewPos=Candidates[0][0]
                self.Board[NewPos]["Prevous"]=self.AgentLocation
                self.Board[self.AgentLocation]["Traveled"]=True
                self.AgentLocation=NewPos
                #print(NewPos,Candidates)

                #time.sleep(0.4)
            if self.AgentLocation == self.Target:
                return self.CompilePath()

        #print(self.GetCandidates())


if __name__ == "__main__":

    Target=(799,799)
    Board=Grid(800,800)
    #print(Board.Board)
    #Board.Board[1][1]=-1
    #print(Board.Board)
    Board.Board[Target[0]][Target[1]]=1
    AS=AStar(Board,AllowDiagonals=False,HWeight=3)
    
    Start=time.time()
    #time.sleep(1)
    Out=AS.RunPathFind(Target=Target,PrintBoard=False)
    if Out != False:
        print("Success")
    else:
        print("Failed")
    print(time.time() - Start)
                    


