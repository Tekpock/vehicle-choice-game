from otree.api import *
import math

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_simple_survey'
    players_per_group = 6
    num_rounds = 1
    # THE ROUND FOR NO POLICY
    stage1_round = 1
    # THE ROUND FOR POLICY
    stage2_round = 3
    # THE ROUND FOR POLICY OR NO POLICY
    stage3_round = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sex = models.BooleanField(
        label="Quel est votre sexe ?",
        choices=[
            [False, "Homme"],
            [True, "Femme"]
        ]
    )
    age = models.IntegerField(
        label="Quel est votre age ?",
        choices=[18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
                 92, 93, 94, 95, 96, 97, 98, 99]
    )
    student = models.BooleanField(
        label="Êtes-vous étudiant.e ?",
        choices=[
            [True, "Oui"],
            [False, "Non"]
        ]
    )
    education = models.IntegerField(
        label="Quel est votre niveau d'études ?",
        choices=[
            [1, "Sans diplôme ou Brevet des collèges"],
            [2, "CAP ou BEP"],
            [3, "Baccalauréat général, technologique ou professionnel"],
            [4, "Diplômes de niveau bac+2 (DUT, BTS, DEUG)"],
            [5, "Licence"],
            [6, "Master"],
            [7, "Doctorat"]
        ]
    )
    activity = models.BooleanField(
        label="Exercez-vous une activité professionnelle ?",
        choices=[
            [True, "Oui"],
            [False, "Non"]
        ]
    )
    profession = models.IntegerField(
        label="Quelle est votre catégorie socio-professionnelle ?",
        choices=[
            [1, "Agriculteur, exploitant agricole"],
            [2, "Artisan, commerçant, chef d’entreprise"],
            [3, "Cadres supérieurs et professions intellectuelles"],
            [4, "Profession intermédiaire"],
            [5, "Employé"],
            [6, "Ouvrier"]

        ]
    )

    iintrsts = models.IntegerField(
        label="1. Le gouvernement interfère beaucoup trop dans notre vie quotidienne.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    harm = models.IntegerField(
        label="2. Parfois, le gouvernement a besoin de faire des lois qui empêchent les gens de se blesser eux-mêmes.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    iprotect = models.IntegerField(
        label="3. Ce n'est pas le rôle du gouvernement d'essayer de protéger les gens d'eux-mêmes.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    privacy = models.IntegerField(
        label="4. Le gouvernement devrait arrêter de dire aux gens comment vivre leur vie.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    protect = models.IntegerField(
        label="5. Le gouvernement devrait faire plus pour faire avancer les objectifs de la société, même si cela "
              "signifie limiter la liberté et les choix des individus.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    limchoi = models.IntegerField(
        label="6. Le gouvernement devrait mettre des limites aux choix que les individus peuvent faire pour qu'ils ne "
              "constituent pas un obstacle de ce qui est bon pour la société.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    hequal = models.IntegerField(
        label="7. Nous sommes allés trop loin dans la promotion de l'égalité des droits en France.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    wealth = models.IntegerField(
        label="8. Notre société irait mieux si la distribution des richesses était plus égalitaire.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    radeq = models.IntegerField(
        label="9. Nous devons réduire considérablement les inégalités entre les riches et les pauvres, et les hommes "
              "et les femmes.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    discrim = models.IntegerField(
        label="10. La discrimination à l'égard des minorités reste un problème majeur dans notre société.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    hrevdis2 = models.IntegerField(
        label="11. Il semblerait que les minorités ne veulent pas l'égalité des droits, ils veulent seulement des "
              "droits exclusifs juste pour eux.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    hfeminin = models.IntegerField(
        label="12. La société dans son ensemble est devenue trop douce et féminine.",
        choices=[
            [1, "Pas du tout d’accord"],
            [2, "Pas d’accord"],
            [3, "Plutôt pas d'accord"],
            [4, "Plutôt d'accord"],
            [5, "D'accord"],
            [6, "Tout à fait d'accord"]
        ],
        widget=widgets.RadioSelect
    )

    # name = models.StringField()
    # age = models.IntegerField()


# PAGES
class SocioPage(Page):
    form_model = 'player'
    form_fields = ['sex', 'age', 'student', 'education', 'activity']


class SocioProfessionPage(Page):
    def is_displayed(player: Player):
        return player.activity == True

    form_model = 'player'
    form_fields = ['profession']


class PsychoPage1(Page):
    form_model = 'player'
    form_fields = ['iintrsts', 'harm', 'iprotect', 'privacy', 'protect', 'limchoi']


class PsychoPage2(Page):
    form_model = 'player'
    form_fields = ['hequal', 'wealth', 'radeq', 'discrim', 'hrevdis2', 'hfeminin']


# FINAL PAYOFF PAGE

class Payoff(Page):
    # @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):

        if player.participant.vars['selected_round'] < Constants.stage2_round:
            chosen_stage = 1
            chosen_round = player.participant.vars['selected_round']
        elif Constants.stage2_round <= player.participant.vars['selected_round'] < Constants.stage3_round:
            chosen_stage = 2
            chosen_round = player.participant.vars['selected_round'] - (Constants.stage2_round - Constants.stage1_round)
        else:
            chosen_stage = 3
            chosen_round = player.participant.vars['selected_round'] - (Constants.stage3_round - Constants.stage1_round)

        return dict(
            # vote1=player.participant.vars['vote_taxation1'],
            # vote2=player.participant.vars['vote_taxation2'],
            # vote3=player.participant.vars['vote_taxation3'],
            # I SHOULD MAKE A FOREACH FUNCTION WHERE I AUTOMATE THIS PROCESS TO DEPEND ON THE NUMBER OF ROUNDS

            # payoff1=player.in_round(1).payoff,
            # payoff2=player.in_round(2).payoff,
            # payoff3=player.in_round(3).payoff,
            payoff_final=math.ceil(player.participant.payoff),
            chosen_round=chosen_round,
            chosen_stage=chosen_stage,
            participation_fee=player.session.config['participation_fee'],
            conversion_rate=player.session.config['real_world_currency_per_point'],
            converted_payoff=math.ceil(player.participant.payoff * player.session.config['real_world_currency_per_point']),
            payoff_euro=math.ceil(player.participant.payoff_plus_participation_fee()),
            after_conversion=player.participant.payoff / player.session.config['real_world_currency_per_point']

            # last_round_payoff=player.in_round(player.round_number - 1).payoff
        )



# class ResultsWaitPage(WaitPage):
#    pass


page_sequence = [SocioPage, SocioProfessionPage, PsychoPage1, PsychoPage2, Payoff]
