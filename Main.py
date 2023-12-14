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
    

class AStar:

    def __init__(self,RefrenceFuntions:dict):

        self.RefrenceFuntions=RefrenceFuntions


    def GetLowestOpenCost(self):
        return list(filter(lambda X: not X[1]["Checked"],sorted(self.ExploredList.items(),key=lambda X: X[1]["CostFull"])))

    def CompilePath(self):
        CurrentSquare=self.TargetID
        Path=[]
        while True:
            Path.append(CurrentSquare)
            if CurrentSquare == self.StartID:
                return Path[::-1]
            CurrentSquare=self.ExploredList[CurrentSquare]["PreviousPlace"]
            
            


    def GeneratePath(self,StartID,TargetID,DTWeight:float=1.5,DBWeight:float=1,AnimatePathing:bool=False):
        self.StartID=StartID
        self.TargetID=TargetID
        self.ExploredList={}


        self.ExploredList[StartID]={"CostFull":self.RefrenceFuntions["Distance"](StartID,TargetID),"DistanceFromStart":0,"PreviousPlace":StartID,"Checked":False}
        Steps=0
        while Steps < 100:
            Lowest=self.GetLowestOpenCost()

            if len(Lowest) > 0:
                Lowest=Lowest[0]
                if AnimatePathing:
                    time.sleep(0.1)
                self.RefrenceFuntions["Render"](list(self.ExploredList.keys()),SearchLocation=Lowest[0])
                #print(self.ExploredList)
                CheckPositions=self.RefrenceFuntions["NeighbourSquares"](Lowest[0])
                for CheckingPosition,CheckWeight in CheckPositions.items():
                    DistanceToOld=self.RefrenceFuntions["Distance"](Lowest[0],CheckingPosition)
                    NewDistanceToStart=self.ExploredList[Lowest[0]]["DistanceFromStart"] + DistanceToOld
                    if CheckingPosition in self.ExploredList:
                        if NewDistanceToStart < self.ExploredList[CheckingPosition]["DistanceFromStart"]:
                            self.ExploredList[CheckingPosition]={"CostFull":(self.RefrenceFuntions["Distance"](CheckingPosition,TargetID) * DTWeight) + (NewDistanceToStart * DBWeight) + CheckWeight,"DistanceFromStart":NewDistanceToStart,"PreviousPlace":Lowest[0],"Checked":self.ExploredList[CheckingPosition]["Checked"]}
                    else:
                        self.ExploredList[CheckingPosition]={"CostFull":(self.RefrenceFuntions["Distance"](CheckingPosition,TargetID) * DTWeight) + (NewDistanceToStart * DBWeight) + CheckWeight,"DistanceFromStart":NewDistanceToStart,"PreviousPlace":Lowest[0],"Checked":False}

                    if CheckingPosition == self.TargetID:
                        #print("DONE")
                        FinalPath=self.CompilePath()
                        self.RefrenceFuntions["Render"](list(self.ExploredList.keys()),Path=FinalPath,SearchLocation=Lowest[0])
                        return

                self.ExploredList[Lowest[0]]["Checked"]=True
               

                #print(CheckPositions)
                #print(Lowest)
            Steps+=1


class GridAStar2D:
    def Distance(self,Position1:tuple[int],Position2:tuple[int]):
        if self.AllowDiagonals:
            return math.sqrt(((Position1[0] - Position2[0]) ** 2) + ((Position1[1] - Position2[1]) ** 2))
        return abs(Position1[0] - Position2[0]) + abs(Position1[1] - Position2[1])
    
    def Weight(self,Position:tuple[int]):
        return self.Grid.Board[Position[1]][Position[0]]

    def SquaresAround(self,Position:tuple[int]):
        OutputList={}
        Directions=[(0,1),(1,0),(0,-1),(-1,0)]
        for Direction in Directions:
            NewPosition=(Position[0] + Direction[0],Position[1] + Direction[1])
            if NewPosition[0] < self.Grid.Width and NewPosition[0] >= 0 and NewPosition[1] < self.Grid.Height and NewPosition[1] >= 0:
                SquareWeight=self.Weight(NewPosition)
                if SquareWeight != -1:
                    OutputList[NewPosition]=SquareWeight
        return OutputList
    
    def RenderGrid(self,ExploredSquares=[],Path=[],SearchLocation=(-1,-1)):
        Out=""
        for Y in range(0,self.Grid.Height):
            for X in range(0,self.Grid.Width):
                Final="⬜"
                if self.Weight((X,Y)) == -1:
                    Final="⬛"
                if (X,Y) in ExploredSquares:
                    Final="🟨"
                if SearchLocation != (-1,-1) and SearchLocation == (X,Y):
                    Final="🟦"
                if (X,Y) in Path:
                    Final="🟩"
                Out+=Final

            Out+="\n"

        print(Out)




    def __init__(self,Grid:Grid,AllowDiagonals=False):
        self.Grid=Grid
        self.AllowDiagonals=AllowDiagonals
        self.MainAStar=AStar({"Distance":self.Distance,"Weight":self.Weight,"NeighbourSquares":self.SquaresAround,"Render":self.RenderGrid})
    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        self.StartLocation=StartLocation
        self.TargetLocation=TargetLocation
        self.MainAStar.GeneratePath(StartLocation,TargetLocation,AnimatePathing=True)

if __name__ == "__main__":
    A2D=GridAStar2D(Grid=Grid(10,10))
    A2D.GeneratePath((0,0),(5,5))
