import glob
import markovify
import random
import re
import time
import os

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'{tekin_id}.*tell.*a story', flags=re.IGNORECASE)

def process(request):
    # Choose 2..5 stories.
    stories = random.sample(glob.glob("corpus/*"),random.randint(2, 5)) 

    models = []
    # Create markov models and merge them.
    for story in stories:
        with open(story) as f:
            models.append(markovify.Text(f.read(),well_formed = False))

    finished_model = markovify.combine(models, range(len(stories)))

    # Decide on paragraphs and sentence count.
    para_length = []
    for i in range(random.randint(2, 5)):
        para_length.append(random.randint(3,5))

    story = ""
    for para in para_length:
        for i in range(para):
            sent = finished_model.make_sentence()
            if(sent != None):
                story += sent
                story += " "
        story += "\r\n"

    characters = random.sample(["@nomworthy","@jhoak","@logan_w","@nanflasted","@nomworthy","@TekinBot"],3)
    story = story.replace("_A_","<"+characters[0]+">")
    story = story.replace("_B_","<"+characters[1]+">")
    story = story.replace("_C_","<"+characters[2]+">")
    return story

def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())