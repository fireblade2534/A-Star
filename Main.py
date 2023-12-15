import random
import math
import time
class Grid:
    def __init__(self,Width:int,Height:int):
        self.Width=Width
        self.Height=Height
        self.Board=[[0 for X in range(0,Width)] for Y in range(0,Height)]

    def RandomPopulateGrid(self,WallChance:float):
        for Y in range(0,self.Height):
            for X in range(0,self.Width):
                if random.randint(0,100) < WallChance:
                    self.Board[Y][X]=-1
    





class AStarV1:
    def __init__(self,Board,FWeight=1.45,AllowDiagonals=False):
        self.Board={}
        self.AgentLocation=(0,0)
        self.FWeight=FWeight
        
        self.AllowDiagonals=AllowDiagonals
        self.Rows=Board.Width
        self.Columns=Board.Height
        
        for Y,F in enumerate(Board.Board):
            for X,G in enumerate(F):
                self.Board[(X,Y)]={"Cost":G,"Traveled":False,"Prevous":(-1,-1)}
    
    def GetCandidates(self):
        Candidates={}
        WallsCount=0
        for Y in [-1,0,1]:
            for X in [-1,0,1]:
                if ((X != 0 or Y != 0) and self.AllowDiagonals) or ((X == 0 or Y == 0) and (X != 0 or Y != 0) and not self.AllowDiagonals):
                    if self.AgentLocation[0] + X >= 0 and self.AgentLocation[0] + X < self.Rows and  self.AgentLocation[1] + Y >= 0 and self.AgentLocation[1] + Y < self.Columns:
                        Check=self.Board[(self.AgentLocation[0] + X,self.AgentLocation[1] + Y)]
                        #print(Check)
                        if Check["Cost"] != -1:
                            
                            if (X == 0 or Y == 0) or not self.AllowDiagonals:
                                Candidates[(self.AgentLocation[0] + X, self.AgentLocation[1] + Y)]=Check["Cost"]
                            else:
                                Check1=self.Board[(self.AgentLocation[0],self.AgentLocation[1] + Y)]
                                Check2=self.Board[(self.AgentLocation[0] + X,self.AgentLocation[1])]
                                if not (Check1["Cost"] == -1 and Check2["Cost"] == -1):
                                    Candidates[(self.AgentLocation[0] + X, self.AgentLocation[1] + Y)]=Check["Cost"]
        return Candidates

    def Hurestic(self,Pos,Dia=False):
        DX=Pos[0] - self.Target[0]
        DY=Pos[1] - self.Target[1]
        if Dia:
            return math.sqrt((DX ** 2) + (DY ** 2))
        return abs(DX) + abs(DY)


    def PrintBoard(self,RenderEnd=False,Path=[],ShowAgent=False,StartLocation=(0,0),Steps=""):

        Out=[[" " for X in range(0,self.Columns)] for Y in range(0,self.Rows)]
        #print(Out)
        for A,B in self.Board.items():
            #print(A[1],A[0])
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
        Out[StartLocation[1]][StartLocation[0]]="🟧"

        if ShowAgent:
            Out[self.AgentLocation[1]][self.AgentLocation[0]]="🟦"
        for X in range(0,len(Out)):
            Out[X]="".join(Out[X])
        print("\n".join(Out) + "\n" + str(Steps))

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

    def RunPathFind(self,Target,PrintBoard=True,PrintFinal=True,ShowSearching=False,StartLocation=(0,0),MaxDistanceMultiplyer=5):
        self.Target=Target
        self.OpenList={}
        self.ClosedList={}
        self.OpenList[StartLocation]={"CostF":self.Hurestic(StartLocation,Dia=False),"CostG":0,"Parent":(-1,-1),"Checked":False}
        Steps=0
        MaxSteps=self.Hurestic(StartLocation,Dia=self.AllowDiagonals) * MaxDistanceMultiplyer
        while True:
            Steps+=1
            L=self.GetLowestOpenCost()
            if len(L) == 0:
                self.AgentLocation=self.Target
                if self.Validate():
                    Path=self.CompilePath()
                    if PrintFinal:
                        self.PrintBoard(RenderEnd=True,Path=Path,StartLocation=StartLocation)
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
                        self.OpenList[X]={"CostF":self.Hurestic(X,Dia=False) * self.FWeight + Lowest[1]["CostG"] + 1,"CostG":Lowest[1]["CostG"] + 1,"Parent":self.AgentLocation,"Checked":self.OpenList[X]["Checked"]}
                else:
                    self.OpenList[X]={"CostF":self.Hurestic(X,Dia=False) * self.FWeight + Lowest[1]["CostG"] + 1,"CostG":Lowest[1]["CostG"] + 1,"Parent":self.AgentLocation,"Checked":False}

                if X == self.Target:
                    if self.Validate():
                        Path=self.CompilePath()
                        if PrintFinal:
                            
                            self.PrintBoard(RenderEnd=True,Path=Path,StartLocation=StartLocation)
                        return Path
                    return False
                
            if PrintBoard:
                self.PrintBoard(ShowAgent=ShowSearching,StartLocation=StartLocation,Steps=Steps)
            if ShowSearching:
                time.sleep(0.05)
            if Steps >= MaxSteps:
                return False
            #return 

#New codde

class AStar:

    def __init__(self,RefrenceFuntions:dict):

        self.RefrenceFuntions=RefrenceFuntions

    @staticmethod
    def FastLowest(List:list):
        return min(List, key=lambda x: x[1]["CostFull"], default=None)


    def GetLowestOpenCost(self):
        Fil=list(self.OpenList.items())
        #Fil=[(X,self.ExploredList[X]) for X in self.OpenList]
        #Fil=filter(lambda X: not X[1]["Checked"],self.ExploredList.items())
        return AStar.FastLowest(Fil)

    def CompilePath(self):
        CurrentSquare=self.TargetID
        Path=[]
        while True:
            Path.append(CurrentSquare)
            if CurrentSquare == self.StartID:
                return Path[::-1]
            CurrentSquare=self.ExploredList[CurrentSquare]["PreviousPlace"]
            
            


    def GeneratePath(self,StartID,TargetID,DTWeight:float=1.55,DBWeight:float=1,AnimatePathing:bool=False,ShowEndPath:bool=False):
        self.StartID=StartID
        self.TargetID=TargetID
        self.ExploredList={}
        self.OpenList={}

        DefaultItem={"CostFull":self.RefrenceFuntions["Distance"](StartID,TargetID),"DistanceFromStart":0,"PreviousPlace":StartID,"Checked":False}

        self.ExploredList[StartID]=DefaultItem
        self.OpenList[StartID]=DefaultItem
        Steps=0
        while Steps < 140000:
            Lowest=self.GetLowestOpenCost()

            if Lowest != None:
                if AnimatePathing:
                    
                    self.RefrenceFuntions["Render"](list(self.ExploredList.keys()),[],Lowest[0],StartID,TargetID)
                    time.sleep(0.1)
                #print(self.ExploredList)
                CheckPositions=self.RefrenceFuntions["NeighbourSquares"](Lowest[0])
                for CheckingPosition,CheckWeight in CheckPositions.items():
                    DistanceToOld=self.RefrenceFuntions["Distance"](Lowest[0],CheckingPosition)
                    NewDistanceToStart=self.ExploredList[Lowest[0]]["DistanceFromStart"] + DistanceToOld
                    if CheckingPosition in self.ExploredList:
                        if NewDistanceToStart < self.ExploredList[CheckingPosition]["DistanceFromStart"]:
                            NewChecking={"CostFull":(self.RefrenceFuntions["Distance"](CheckingPosition,TargetID) * DTWeight) + (NewDistanceToStart * DBWeight) + CheckWeight,"DistanceFromStart":NewDistanceToStart,"PreviousPlace":Lowest[0],"Checked":self.ExploredList[CheckingPosition]["Checked"]}
                            self.ExploredList[CheckingPosition]=NewChecking
                            if NewChecking["Checked"] == False:
                                self.OpenList[CheckingPosition]=NewChecking
                    else:
                        NewChecking={"CostFull":(self.RefrenceFuntions["Distance"](CheckingPosition,TargetID) * DTWeight) + (NewDistanceToStart * DBWeight) + CheckWeight,"DistanceFromStart":NewDistanceToStart,"PreviousPlace":Lowest[0],"Checked":False}
                        self.ExploredList[CheckingPosition]=NewChecking
                        self.OpenList[CheckingPosition]=NewChecking

                    if CheckingPosition == self.TargetID:
                        #print("DONE")
                        FinalPath=self.CompilePath()
                        if ShowEndPath:
                            self.RefrenceFuntions["Render"](list(self.ExploredList.keys()),FinalPath,Lowest[0],StartID,TargetID)
                        return FinalPath

                self.ExploredList[Lowest[0]]["Checked"]=True
                del self.OpenList[Lowest[0]]
               

                #print(CheckPositions)
                #print(Lowest)
            Steps+=1
        return []

class GridAStar2D:
    def Distance(self,Position1:tuple[int],Position2:tuple[int]):
        return math.sqrt(((Position1[0] - Position2[0]) ** 2) + ((Position1[1] - Position2[1]) ** 2))
        #if self.AllowDiagonals:
            
        #return abs(Position1[0] - Position2[0]) + abs(Position1[1] - Position2[1])
    
    def Weight(self,Position:tuple[int]):
        return self.Grid.Board[Position[1]][Position[0]]

    def SquaresAround(self,Position:tuple[int]):
        OutputList={}
        Directions=[(1,0),(0,1),(0,-1),(-1,0)]
        for Direction in Directions:
            NewPosition=(Position[0] + Direction[0],Position[1] + Direction[1])
            if NewPosition[0] < self.Grid.Width and NewPosition[0] >= 0 and NewPosition[1] < self.Grid.Height and NewPosition[1] >= 0:
                SquareWeight=self.Grid.Board[NewPosition[1]][NewPosition[0]]
                if SquareWeight != -1:
                    OutputList[NewPosition]=SquareWeight
        return OutputList
    
    def RenderGrid(self,ExploredSquares=[],Path=[],SearchLocation=(-1,-1),StartLocation=(0,0),TargetLocation=(0,0)):
        Out=""
        for Y in range(0,self.Grid.Height):
            for X in range(0,self.Grid.Width):
                Final="⬜"
                if self.Grid.Board[Y][X] == -1:
                    Final="⬛"
                if (X,Y) in ExploredSquares:
                    Final="🟨"
                if SearchLocation != (-1,-1) and SearchLocation == (X,Y):
                    Final="🟦"
                
                if (X,Y) in Path:
                    Final="🟩"
                #print(StartLocation)
                if (X,Y) == StartLocation:
                    Final="🟧"
                if (X,Y) == TargetLocation:
                    Final="🟪"
                Out+=Final

            Out+="\n"

        print(Out)




    def __init__(self,Grid:Grid,AllowDiagonals=False):
        self.Grid=Grid
        self.AllowDiagonals=AllowDiagonals
        self.MainAStar=AStar({"Distance":self.Distance,"NeighbourSquares":self.SquaresAround,"Render":self.RenderGrid})
    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0),AnimatePathing=False,ShowEndPath=False,DTWeight:float=1.5):
        self.StartLocation=StartLocation
        self.TargetLocation=TargetLocation
        return self.MainAStar.GeneratePath(StartLocation,TargetLocation,AnimatePathing=AnimatePathing,ShowEndPath=ShowEndPath,DTWeight=DTWeight)

if __name__ == "__main__":
    #RunProfiling()
   # exit()
    G=Grid(35,35)
    G.RandomPopulateGrid(28)

    
    StartLocation=(5,5)
    TargetLocation=(30,30)
    G.Board[TargetLocation[1]][TargetLocation[0]]=0
    StartTime=time.time()
    A2D=GridAStar2D(Grid=G)
    Path=A2D.GeneratePath(StartLocation,TargetLocation,AnimatePathing=True,ShowEndPath=True,DTWeight=2)


