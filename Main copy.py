import random
import math
import time

class Grid:
    def __init__(self,Rows,Column,RandomGen=True,Board=[],WallChance=30):
        self.Board=Board
        self.Rows=Rows
        self.Column=Column
        if RandomGen:
            for X in range(0,Column):
                Row=[]
                for Y in range(0,Rows):
                    if random.randint(0,100) < WallChance:
                        Row.append(-1)
                    else:
                        Row.append(1)
                self.Board.append(Row)


class AStar:
    def __init__(self,Board,FWeight=1.2,AllowDiagonals=False):
        self.Board={}
        self.AgentLocation=(0,0)
        self.FWeight=FWeight
        
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
                        if Check["Cost"] != -1:
                            Candidates[(self.AgentLocation[0] + X, self.AgentLocation[1] + Y)]=Check["Cost"]
        return Candidates

    def Hurestic(self,Pos,Dia=False):
        DX=Pos[0] - self.Target[0]
        DY=Pos[1] - self.Target[1]
        if Dia:
            return math.sqrt((DX ** 2) + (DY ** 2))
        return abs(DX) + abs(DY)


    def PrintBoard(self,RenderEnd=False,Path=[],ShowAgent=False):

        Out=[[" " for X in range(0,self.Columns)] for Y in range(0,self.Rows)]
        #print(Out)
        for A,B in self.Board.items():
            Item=""
            if B["Cost"] == -1:
                Item="⬛"
            else:
                Item="⬜"

            Out[A[1]][A[0]]=Item
        for X,A in self.OpenList.items():
            Out[X[1]][X[0]]="🟨"

        if RenderEnd:
            
            for A in Path:
                Out[A[1]][A[0]]="🟩"
        Out[self.Target[1]][self.Target[0]]="🟪"


        if ShowAgent:
            Out[self.AgentLocation[1]][self.AgentLocation[0]]="🟦"
        for X in range(0,len(Out)):
            Out[X]="".join(Out[X])
        print("\n".join(Out) + "\n")

    def CompilePath(self):
        Path=[]
        Pos=self.AgentLocation
        Path.append(Pos)
        while True:
            Item=self.OpenList[Pos]
            if Item["Parent"] == (-1,-1):
                return Path
            else:
                Path.append(Item["Parent"])
                Pos=Item["Parent"]
    def Validate(self):
        Pos=self.AgentLocation
        
        while True:
            try:
                Item=self.OpenList[Pos]
            except KeyError:
                return False
            if Item["Parent"] == (-1,-1):
                return True
            else:
                
                Pos=Item["Parent"]
        
    def GetLowestOpenCost(self):
        return list(filter(lambda X: not X[1]["Checked"],sorted(self.OpenList.items(),key=lambda X: X[1]["CostF"])))

    def RunPathFind(self,Target,PrintBoard=True,PrintFinal=True,ShowSearching=False):
        self.Target=Target
        self.OpenList={}
        self.ClosedList={}
        self.OpenList[(0,0)]={"CostF":self.Hurestic((0,0),Dia=True),"CostG":0,"Parent":(-1,-1),"Checked":False}
        Steps=0
        while True:
            Steps+=1
            L=self.GetLowestOpenCost()
            if len(L) == 0:
                self.AgentLocation=self.Target
                if self.Validate():
                    Path=self.CompilePath()
                    if PrintFinal:
                        self.PrintBoard(RenderEnd=True,Path=Path)
                    return Path
                
                return False
                
            Lowest=L[0]

            self.AgentLocation=Lowest[0]
            #print(self.AgentLocation,self.OpenList,L)
            Candidates=self.GetCandidates()

            self.OpenList[self.AgentLocation]["Checked"]=True
            for X,A in Candidates.items():
                
                
                #print(X,A)
                if X in self.OpenList:
                    if Lowest[1]["CostG"] + 1 < self.OpenList[X]["CostG"]:
                        self.OpenList[X]={"CostF":self.Hurestic(X,Dia=True) * self.FWeight + Lowest[1]["CostG"] + 1,"CostG":Lowest[1]["CostG"] + 1,"Parent":self.AgentLocation,"Checked":self.OpenList[X]["Checked"]}
                else:
                    self.OpenList[X]={"CostF":self.Hurestic(X,Dia=True) * self.FWeight + Lowest[1]["CostG"] + 1,"CostG":Lowest[1]["CostG"] + 1,"Parent":self.AgentLocation,"Checked":False}

                if X == self.Target:
                    if self.Validate():
                        Path=self.CompilePath()
                        if PrintFinal:
                            if ShowSearching:
                                print("Full Step")
                            self.PrintBoard(RenderEnd=True,Path=Path)
                        return Path
                    return False
            if PrintBoard:
                self.PrintBoard(ShowAgent=ShowSearching)
            if ShowSearching:
                time.sleep(0.1)
            if Steps == 30000:
                return False
            #return 

class GreedyBestFirstSearch:
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
        
            

    def RunPathFind(self,Target,PrintBoard=True,PrintFinal=True):
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
                if PrintFinal:
                    self.PrintBoard()
                return self.CompilePath()

        #print(self.GetCandidates())



        #print(self.GetCandidates())


if __name__ == "__main__":

    Target=(25,25)
    Board=Grid(30,30,WallChance=35)
    #print(Board.Board)
    #Board.Board[1][1]=-1
    #print(Board.Board)
    Board.Board[Target[0]][Target[1]]=1
    AS=AStar(Board,AllowDiagonals=False,FWeight=1.2)
    GBFS=GreedyBestFirstSearch(Board,AllowDiagonals=False)
    
    Start=time.time()
    #time.sleep(1)
    OutAS=AS.RunPathFind(Target=Target,PrintBoard=True,ShowSearching=True)
    if OutAS != False:
        print("Success AS")
        print(time.time() - Start)
        exit()
        Start=time.time()
        OutGBFS=GBFS.RunPathFind(Target=Target,PrintBoard=False)
        if OutGBFS != False:
            print("Success GBFS")
            print(time.time() - Start)
            
        else:
            print("Failed GBFS")
    else:
        print("Failed AS")

    

    
    
                    


