import glob
import random
import re

import markovify

import tekinbot.utils.post as pu
from tekinbot.utils.config import tekin_id

comm_re = re.compile(f'{tekin_id}.*tell.*a story.*', flags=re.IGNORECASE)
ALL_CHARS = ["@nomworthy", "@jhoak", "@logan_w",
             "@nanflasted", "@nomworthy", "@TekinBot"]


def process(request):
    # Choose 2..5 stories.
    stories = random.sample(
        glob.glob("**/corpus/*", recursive=True),
        random.randint(2, 5)
    )

    models = []
    # Create markov models and merge them.
    for story in stories:
        with open(story) as f:
            models.append(markovify.Text(f.read(), well_formed=False))

    finished_model = markovify.combine(models, range(len(stories)))

    # Decide on paragraphs and sentence count.
    para_length = []
    for i in range(random.randint(2, 5)):
        para_length.append(random.randint(3, 5))

    story_text = "\n".join([
        " ".join([
            finished_model.make_sentence() for _ in range(para)
        ]) for para in para_length
    ])

    characters = random.sample(ALL_CHARS, 3)
    for (token, character) in zip(["_A_", "_B_", "_C_"], characters):
        story_text = story_text.replace(token, character)

    return story_text


def post(request, response):
    return pu.post_plain_text(request, response, auth=pu.bot_auth())
