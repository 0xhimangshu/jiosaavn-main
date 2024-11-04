


class Track:
    def __init__(self, data: dict):
        self.data = data

    @property
    def id(self) -> str:
        return self.data['perma_url'].split("/")[-1]
    
    @property
    def title(self) -> str:
        return self.data['title']

    @property
    def url(self) -> str:
        return self.data['url'] 
    
    @property
    def image(self) -> str:
        return self.data['image']
    
    @property
    def duration(self) -> int:
        return self.data['duration']
    
    @property
    def encrypted_media_url(self) -> str:
        return self.data['more_info']['encrypted_media_url']
    
    @property
    def has_lyrics(self) -> bool:
        return self.data['more_info']['has_lyrics']
    
    @property
    def media_url(self) -> str:
        return self.data['media_url'].split("?")[0].replace("ac.cf", "aac")
    

    @property
    def as_json(self) -> dict:
        return self.data