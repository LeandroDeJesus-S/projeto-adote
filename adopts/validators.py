from django.core.exceptions import ValidationError
from unidecode import unidecode


def validate_state(states, state_to_validate: str) -> str|None:
    for state in states:
        print(state_to_validate.lower(), '---', unidecode(state['estado']))
        if unidecode(state_to_validate.lower()) in unidecode(state['estado'].lower()):
            return state['id']
    return None

