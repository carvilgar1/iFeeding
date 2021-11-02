class TMB():
    def __init__(self, age, weigth, height, genre, activity=1) -> None:
        self.age = age
        self.weight = weigth
        self.height = height
        self.genre = genre
        self.activity = activity
    
    def get_tbm_harris_benedict(self) -> int:
        tbm = 66 + 13.7 * self.weight + 5*self.height - 6.8 * self.age
        return int(tbm)+1
    
    def get_tbm_revisada(self) -> int:
        tbm = 5 + 10 * self.weight + 6.25*self.height - 5 * self.age
        return int(tbm+1)*self.activity

if __name__ == '__main__':
    tmb1 = TMB(21,84.1,174,0,activity=1.725)
