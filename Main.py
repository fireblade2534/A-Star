import random
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
    def __init__(self,Grid:Grid):
        self.Grid=Grid

    def GeneratePath(self,StartLocation:tuple[int]=(0,0),TargetLocation:tuple[int]=(0,0)):
        self.StartLocation=StartLocation
        self.TargetLocation=TargetLocation
        ExploredList={}
        MovePosition=StartLocation

        ExploredList[MovePosition]={}
