import random
import math
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

    def GeneratePath(self,StartID,TargetID):
        self.StartID=StartID
        self.TargetID=TargetID
        self.ExploredList={}
        MovePosition=StartID

        self.ExploredList[MovePosition]={"CostFull":self.RefrenceFuntions["Distance"](StartID,TargetID),"DistanceFromStart":0,"Checked":False}
        Steps=0
        while Steps < 100:
            Lowest=self.GetLowestOpenCost()
            if len(Lowest) > 0:
                Lowest=Lowest[0]
                CheckPositions=self.RefrenceFuntions["NeighbourSquares"](Lowest[0])
                for ChekingPosition,CheckWeight in CheckPositions.items():
                    DistanceToOld=self.RefrenceFuntions["Distance"](Lowest[0],CheckPositions)
                    if CheckPositions in self.ExploredList:
                        
                    else:
                        self.ExploredList[CheckPositions]=
                print(CheckPositions)
                print(Lowest)
            Steps+=1


class GridAStar2D:
    def Distance(self,Position1:tuple[int],Position2:tuple[int]):
        if self.AllowDiagonals:
            return math.sqrt(((Position1[0] - Position2[0]) ** 2) + ((Position1[1] - Position2[1]) ** 2))
        return (Position1[0] - Position2[0]) + (Position1[1] - Position2[1])
    
    def Weight(self,Position:tuple[int]):
        return self.Grid.Board[Position[1]][Position[0]]

    def SquaresAround(self,Position:tuple[int]):
        OutputList={}
        Directions=[(0,1),(1,0),(0,-1),(-1,0)]
        for Direction in Directions:
            NewPosition=(Position[0] + Direction[0],Position[1] + Direction[1])
            if NewPosition[0] < self.Grid.Width and NewPosition[0] >= 0 and NewPosition[1] < self.Grid.Height and NewPosition[1] >= 0:
                OutputList[NewPosition]=self.Weight(NewPosition)
        return OutputList
    


    def __init__(self,Grid:Grid,AllowDiagonals=False):
        self.Grid=Grid
        self.AllowDiagonals=AllowDiagonals
        self.MainAStar=AStar({"Distance":self.Distance,"Weight":self.Weight,"NeighbourSquares":self.SquaresAround})
    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        self.MainAStar.GeneratePath(StartLocation,TargetLocation)

if __name__ == "__main__":
    A2D=GridAStar2D(Grid=Grid(10,10))
    A2D.GeneratePath((0,0),(5,5))
