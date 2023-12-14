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

    @staticmethod
    def Distance(Position1:tuple[int],Position2:tuple[int],Diagonal:bool):
        if Diagonal:
            return math.sqrt(((Position1[0] - Position2[0]) ** 2) + ((Position1[1] - Position2[1]) ** 2))
        return (Position1[0] - Position2[0]) + (Position1[1] - Position2[1])

    def __init__(self,Grid:Grid,AllowDiagonals:bool=False):
        self.Grid=Grid
        self.AllowDiagonals=AllowDiagonals

    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        self.StartLocation=StartLocation
        self.TargetLocation=TargetLocation
        ExploredList={}
        MovePosition=StartLocation

        ExploredList[MovePosition]={"Distance":AStar.Distance(StartLocation,TargetLocation,self.AllowDiagonals),"DistanceFromStart"}


class 2DGridAStar:
    def __init__()
