from os import environ


SESSION_CONFIGS = [

dict(
        name='vehicle_choice_game_tax_vote_all',
        display_name="vehicle_choice_game_tax_vote_all",
        num_demo_participants=6,
        app_sequence=['vehicle_choice_game_tax_vote_all', 'my_simple_survey'
                      ]
    ),

dict(
        name='vehicle_choice_game_regulation_vote_all',
        display_name="vehicle_choice_game_regulation_vote_all",
        num_demo_participants=6,
        app_sequence=['vehicle_choice_game_regulation_vote_all', 'my_simple_survey'
                      ]
    ),

# dict(
#        name='vehicle_choice_game_both_treatments',
#        display_name="vehicle_choice_game_both_treatments",
#        num_demo_participants=6,
#        app_sequence=['vehicle_choice_game_both_treatments', 'my_simple_survey'
#                      ],
#        session_treatment=1,
#        doc="""
#        For sessions with taxation leave the value to the default value of 1.
#        For sessions with regulation please change the value to 0.
#        """
#    ),

dict(
        name='my_simple_survey',
        display_name='my_simple_survey',
        app_sequence=['my_simple_survey'],
        num_demo_participants=6
    )

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.125, participation_fee=7.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'fr'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [

    dict(name='vehicle_choice', display_name='vehicle_choice')
]



ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4197730932197'

INSTALLED_APPS = ['otree']
