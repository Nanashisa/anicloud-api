class Director:
    def __init__(self, url: str, name: str):
        self.url: str = url
        self.name: str = name
    
    def __str__(self):
        return self.name
    # TODO
