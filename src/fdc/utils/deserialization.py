import re
import json
import humps


def loads_json(text):
    return key_snakecase(json.loads(text))
