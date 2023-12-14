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

    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        self.StartLocation=StartLocation
        self.TargetLocation=TargetLocation
        ExploredList={}
        MovePosition=StartLocation

        ExploredList[MovePosition]={"Distance":AStar.Distance(StartLocation,TargetLocation,self.AllowDiagonals),"DistanceFromStart":0}


class GridAStar2D:
    def Distance(self,Position1:tuple[int],Position2:tuple[int]):
        if self.AllowDiagonals:
            return math.sqrt(((Position1[0] - Position2[0]) ** 2) + ((Position1[1] - Position2[1]) ** 2))
        return (Position1[0] - Position2[0]) + (Position1[1] - Position2[1])
    
    def Weight(self,Position:tuple[int]):
        return self.Grid
    def __init__(self,Grid:Grid,AllowDiagonals=False):
        self.Grid=Grid
        self.AllowDiagonals=AllowDiagonals
        MainAStar=AStar({"Distance":self.Distance,})
    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        pass
