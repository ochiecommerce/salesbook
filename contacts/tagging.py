import re
from .models import Tag
class TagListener:
    def __init__(self,tagger_app) -> None:
        self.tagger = tagger_app
        self.tag_pattern = re.compile(r'@[a-z]+/[a-z0-9]+')

    def check(self,text,tagger_id):
        print('taglistener=>',tagger_id,self.tagger)
        tags = self.tag_pattern.findall(text)
        for tag in tags:
            tagged_app, tagged_id = tag.split('/')
            tagged_app = tagged_app[1:]
            self.save(tagged_app,tagger_id,tagged_id)


    def save(self,taggable,tagger_id,tagged_id):
        print('saving tag',taggable,tagger_id,tagged_id)
        tag = Tag(tagger_app=self.tagger,tagged_app=taggable,tagger_id=tagger_id,tagged_id=tagged_id)
        tag.save()
