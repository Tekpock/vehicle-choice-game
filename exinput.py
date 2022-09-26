import requests  # pip3 install requests

GET = requests.get
POST = requests.post

SERVER_URL = 'https://vehicle-choice-game.herokuapp.com'  # Change this to https://your_app_web_address
ROOM_NAME = 'vehicle_choice'
REST_KEY = 'EconomiX'  # fill this as indicated here https://otree.readthedocs.io/en/latest/misc/rest_api.html#authentication
TREATMENT_ASSIGNMENTS = dict(
    Policy=[1, 2],
    NoPolicy=[3]
)

if list(TREATMENT_ASSIGNMENTS) != list(TREATMENT_ASSIGNMENTS):
    raise ValueError(
        "Please, make sure that the treatment assigned corresponds to the treatments included in the constants of "
        "your oTree app."
    )


def call_api(method, *path_parts, **params) -> dict:
    path_parts = '/'.join(path_parts)
    url = f'{SERVER_URL}/api/{path_parts}/'
    resp = method(url, json=params, headers={'otree-rest-key': REST_KEY})
    if not resp.ok:
        msg = (
            f'Request to "{url}" failed '
            f'with status code {resp.status_code}: {resp.text}'
        )
        raise Exception(msg)
    return resp.json()


session_code = [room for room in call_api(GET, 'rooms') if room['name'] == ROOM_NAME][0]['session_code']
if session_code:
    call_api(POST, 'session_vars', session_code, vars=dict(treatment_assignments=TREATMENT_ASSIGNMENTS))
    print('Treatment assignments completed')
else:
    print('No session exists in the specified room')
