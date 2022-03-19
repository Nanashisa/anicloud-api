class Rating:
    def __init__(self, _min: int, _max: int, _val: int, _count: int):
        self.min = _min
        self.max = _max
        self.value = _val
        self.count = _count
    
    def __str__(self):
        return f"{self.value}/{self.max} ({self.count})"
