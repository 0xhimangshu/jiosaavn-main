class Artist:
    def __init__(self, data: dict):
        self.data = data

    @property
    def id(self) -> str:
        return self.data['id']  
    
    @property
    def name(self) -> str:
        return self.data['name']
    
    @property
    def image(self) -> str:
        return self.data['image']
    
    @property
    def url(self) -> str:
        return self.data['perma_url']
    
    #NOT IMPLEMENTED