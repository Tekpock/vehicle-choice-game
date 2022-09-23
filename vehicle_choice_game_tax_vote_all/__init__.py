from otree.api import *
import math

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'vehicle_choice_game_tax_vote_all'
    players_per_group = 6
    num_rounds = 30

    # THE ROUND FOR NO POLICY
    stage1_round = 1
    # THE ROUND FOR POLICY
    stage2_round = 11
    # THE ROUND FOR POLICY OR NO POLICY
    stage3_round = 21

    # NAME OF THE TREATMENT
    TREATMENTS = ['Policy', 'NoPolicy']

    # THE PASSWORD FOR THE TAXATION PERIOD
    # tax_password = "1234"

    # THE PASSWORD FOR THE NON TAXATION PERIOD
    # no_tax_password = "abcd"

    endowment = 100
    conventional_cost = 40
    public_cost = 10
    electric_cost = 55
    conventional_utility = 100
    electric_utility = 100
    public_utility_1 = 40
    public_utility_2 = 45
    public_utility_3 = 50
    public_utility_4 = 70
    public_utility_5 = 75
    public_utility_6 = 80
    conventional_pollution = 5
    public_pollution = 0
    electric_pollution = 0
    # The Tax is equal to the marginal damage of the vehicle's pollution
    conventional_tax = conventional_pollution * (players_per_group - 1)
    public_tax = 0
    electric_tax = 0


class Subsession(BaseSubsession):
    pass

# ASSIGNING TO ROLES

def creating_session(session):
    session.group_randomly()  # This randomizes the groups

    # Some role assignment below
    for p in session.get_players():
        if session.round_number == 1:
            if p.id_in_group == 1:
                p.participant.vars['type'] = 'player1'
            elif p.id_in_group == 2:
                p.participant.vars['type'] = 'player2'
            elif p.id_in_group == 3:
                p.participant.vars['type'] = 'player3'
            elif p.id_in_group == 4:
                p.participant.vars['type'] = 'player4'
            elif p.id_in_group == 5:
                p.participant.vars['type'] = 'player5'
            elif p.id_in_group == 6:
                p.participant.vars['type'] = 'player6'

        p.type = p.participant.vars['type']


class Group(BaseGroup):
    total_pollution = models.IntegerField()
    pollution_damage = models.IntegerField()
    total_tax = models.IntegerField()
    tax_redistribution = models.FloatField()
    # vote_taxation = models.BooleanField()

    # IS THIS ONE NESCESSARY ?
    vote_taxation = models.StringField()
    # IS THIS ONE NESCESSARY ?
    tax_present = models.BooleanField(initial=0)




# FUNCTIONS







# ASSIGNING GROUP TO TREATMENT


class Player(BasePlayer):
    # THE TREATMENT TO WHICH THE PLAYER WAS ASSIGNED

    type = models.StringField()

    adopt_tax1 = models.StringField()
    adopt_tax2 = models.StringField()
    adopt_tax3 = models.StringField()

    treatment = models.StringField(choices=Constants.TREATMENTS)

    vehicle_choice = models.StringField(
        label="Quelle est l'option que vous préférez?",
        choices=[
            ["Electric Vehicle", "Option A"],
            ["Public Vehicle", "Option B"],
            ["Conventional Vehicle", "Option C"]
        ]
    )
    vehicle_cost = models.IntegerField(initial=0)
    vehicle_pollution = models.IntegerField(intial=0)
    vehicle_utility = models.IntegerField(initial=0)
    vehicle_tax = models.IntegerField(initial=0)
    player_random_round = models.IntegerField(initial=0)


    # THIS IS THE FIELD FOR THE FINAL PAYOFF
    payoff_final = models.FloatField(initial=0)

    # THIS IS THE FIELD FOR TAXATION VOTE

    # FIRST POLICY VOTE
    vote_taxation = models.BooleanField(
        label="Veuillez voter pour ou contre l'implémentation de la taxe à la Partie 3 ?",
        choices=[
            [True,
             "Pour : Oui, je souhaite l'implémentation d'une taxe de 25 ECUs qui devra être payée par chaque membre "
             "du groupe qui choisit l'option C."],
            [False, "Contre : Non, je ne souhaite pas l'implémentation d'une taxe de 25 ECUs."],
        ]
    )

    # HERE ARE THE FIELDS FOR THE COMPREHENSION PAGE
    comprehension1 = models.StringField(
        label="1. Le résultat de quel vote sera implémenté lors de l'étape 2 de la Partie 3 ?",
        choices=[
            ["Option1", "Ceci dépend du tirage au sort d'une bille à la fin de l'expérience"],
            ["Option2", "Vote 1"],
            ["Option3", "Vote 2"],
            ["Option4", "Vote 3"],
        ]
    )

    comprehension2 = models.StringField(
        label="2. Combien d'ECUs perdez vous (sans prendre en compte le coût de l'option que vous avez choisi)"
              " si deux participants de votre groupe choisissent l'option C?",
        choices=[
            ["Option1", "0 ECUs"],
            ["Option2", "10 ECUs"],
            ["Option3", "20 ECUs"],
            ["Option4", "30 ECUs"],
        ]
    )

    comprehension3 = models.StringField(
        label="3. Dans le cas où il y a une mise en place de la taxe, combien d'ECUs supplémentaires"
              " devez vous payer si vous avez choisi l'option C ?",
        choices=[
            ["Option1", "0 ECUs"],
            ["Option2", "15 ECUs"],
            ["Option3", "25 ECUs"],
            ["Option4", "35 ECUs"],
        ]
    )



# FUNCTIONS
# FOR EACH PLAYER THIS RETURNS THE PLAYERS ROLE

# def role(player):
#    return player.participant.vars['type']



# HERE WE ASSIGN THE TREATMENTS TO THE GROUPS
def assign_treatment(player: Player):
    group_id = player.group.id_in_subsession
    treatment_assignments = player.session.vars['treatment_assignments']
    for t, v in treatment_assignments.items():
        if group_id in v:
            player.treatment = t
            player.participant.vars['final_policy'] = t


# FUNCTIONS
### HERE WE SET THE MAJORITY FOR THE FIRST VOTE

def set_majority(group: Group):
    # Obtain a list of all player votes
    players = group.get_players()
    policy_votes = [p.vote_taxation for p in players]
    # If True is greater than half the amounts of player in the group
    # Then it is set as the majority
    if policy_votes.count(True) > (Constants.players_per_group / 2):
        # group.vote_taxation = True
        group.vote_taxation = "Adopted"
        # STORING FOR LATER APPS THAT THE GROUP MAJORITY HAS VOTED FOR THE SUBSIDY
        for player in players:
            if player.round_number == Constants.stage1_round:
                player.participant.vars['vote_taxation1'] = 1
            elif player.round_number == Constants.stage2_round:
                player.participant.vars['vote_taxation2'] = 1
            elif player.round_number == Constants.stage3_round:
                player.participant.vars['vote_taxation3'] = 1
    elif policy_votes.count(False) > (Constants.players_per_group / 2):
        # group.vote_taxation = False
        group.vote_taxation = "Not Adopted"
        # STORING FOR LATER APPS THAT THE GROUP MAJORITY HAS NOT VOTED FOR THE SUBSIDY
        for player in players:
            if player.round_number == Constants.stage1_round:
                player.participant.vars['vote_taxation1'] = 0
            elif player.round_number == Constants.stage2_round:
                player.participant.vars['vote_taxation2'] = 0
            elif player.round_number == Constants.stage3_round:
                player.participant.vars['vote_taxation3'] = 1
    else:
        group.vote_taxation = "Tie"

    # NEED TO TAKE INTO CONSIDERATION THAT IT MIGHT BE A TIE


####### THIS TAKES INTO ACCOUNT THE VOTING SYSTEM
####### HOWEVER NOW IT IS IMPORTANT TO TAKE INTO ACCOUNT THE TREATMENT SYSTEM

def set_payoffs(group: Group):
    # SETTING A GAME SETTING BASED ON THE PREVIOUS VOTING SYSTEM
    players = group.get_players()
    # WE ASSIGN COSTS AND POLLUTION AMOUNTS PER VEHICLE
    for p in players:

        # PAYOFF FOR STAGE 1 : NO POLICY
        if Constants.stage2_round > p.round_number >= Constants.stage1_round:
            # THIS IS THE CASE FOR WITHOUT TAXATION
            group.tax_present = 0
            # WE ASSIGN COSTS AND POLLUTION AMOUNTS PER VEHICLE
            if p.vehicle_choice == "Conventional Vehicle":
                p.vehicle_cost = Constants.conventional_cost
                p.vehicle_pollution = Constants.conventional_pollution
                p.vehicle_utility = Constants.conventional_utility
            # THIS IS THE PUBLIC VEHICLE OPTION
            elif p.vehicle_choice == "Public Vehicle":
                p.vehicle_cost = Constants.public_cost
                p.vehicle_pollution = Constants.public_pollution
                # SETTING UP THE HETEROGENEITY
                if p.id_in_group == 1:
                    p.vehicle_utility = Constants.public_utility_1
                elif p.id_in_group == 2:
                    p.vehicle_utility = Constants.public_utility_2
                elif p.id_in_group == 3:
                    p.vehicle_utility = Constants.public_utility_3
                elif p.id_in_group == 4:
                    p.vehicle_utility = Constants.public_utility_4
                elif p.id_in_group == 5:
                    p.vehicle_utility = Constants.public_utility_5
                elif p.id_in_group == 6:
                    p.vehicle_utility = Constants.public_utility_6
            elif p.vehicle_choice == "Electric Vehicle":
                p.vehicle_cost = Constants.electric_cost
                p.vehicle_pollution = Constants.electric_pollution
                p.vehicle_utility = Constants.electric_utility

        # PAYOFF FOR STAGE 2 : POLICY
        elif Constants.stage3_round > p.round_number >= Constants.stage2_round:
            # THIS IS THE PAYOFF WITH TAXATION
            group.tax_present = 1
            ####################################
            if p.vehicle_choice == "Conventional Vehicle":
                p.vehicle_cost = Constants.conventional_cost
                p.vehicle_pollution = Constants.conventional_pollution
                p.vehicle_tax = Constants.conventional_tax
                p.vehicle_utility = Constants.conventional_utility

                # THIS IS THE PUBLIC VEHICLE OPTION
            elif p.vehicle_choice == "Public Vehicle":
                p.vehicle_cost = Constants.public_cost
                p.vehicle_pollution = Constants.public_pollution
                # SETTING UP THE HETEROGENEITY
                if p.id_in_group == 1:
                    p.vehicle_utility = Constants.public_utility_1
                elif p.id_in_group == 2:
                    p.vehicle_utility = Constants.public_utility_2
                elif p.id_in_group == 3:
                    p.vehicle_utility = Constants.public_utility_3
                elif p.id_in_group == 4:
                    p.vehicle_utility = Constants.public_utility_4
                elif p.id_in_group == 5:
                    p.vehicle_utility = Constants.public_utility_5
                elif p.id_in_group == 6:
                    p.vehicle_utility = Constants.public_utility_6
            elif p.vehicle_choice == "Electric Vehicle":
                p.vehicle_cost = Constants.electric_cost
                p.vehicle_pollution = Constants.electric_pollution
                p.vehicle_tax = Constants.electric_tax
                p.vehicle_utility = Constants.electric_utility



        # PAYOFF FOR STAGE 3 : POLICY OR NO POLICY
        elif p.round_number >= Constants.stage3_round:

            # prev_vote_tax = p.participant.vars['final_policy']
            final_policy = p.participant.vars['final_policy']
            if final_policy == "Policy":
                # THIS IS THE PAYOFF WITH TAXATION
                group.tax_present = 1
                ##################################
                if p.vehicle_choice == "Conventional Vehicle":
                    p.vehicle_cost = Constants.conventional_cost
                    p.vehicle_pollution = Constants.conventional_pollution
                    p.vehicle_tax = Constants.conventional_tax
                    p.vehicle_utility = Constants.conventional_utility
                    # p.vehicle_subsidy = Constants.conventional_subsidy
                # THIS IS THE PUBLIC VEHICLE OPTION
                elif p.vehicle_choice == "Public Vehicle":
                    p.vehicle_cost = Constants.public_cost
                    p.vehicle_pollution = Constants.public_pollution
                    # SETTING UP THE HETEROGENEITY
                    if p.id_in_group == 1:
                        p.vehicle_utility = Constants.public_utility_1
                    elif p.id_in_group == 2:
                        p.vehicle_utility = Constants.public_utility_2
                    elif p.id_in_group == 3:
                        p.vehicle_utility = Constants.public_utility_3
                    elif p.id_in_group == 4:
                        p.vehicle_utility = Constants.public_utility_4
                    elif p.id_in_group == 5:
                        p.vehicle_utility = Constants.public_utility_5
                    elif p.id_in_group == 6:
                        p.vehicle_utility = Constants.public_utility_6
                elif p.vehicle_choice == "Electric Vehicle":
                    p.vehicle_cost = Constants.electric_cost
                    p.vehicle_pollution = Constants.electric_pollution
                    p.vehicle_tax = Constants.electric_tax
                    p.vehicle_utility = Constants.electric_utility
                    # p.vehicle_subsidy = Constants.electric_subsidy
            elif final_policy == "NoPolicy":
                # THIS IS THE CASE FOR WITHOUT TAXATION
                group.tax_present = 0
                # WE ASSIGN COSTS AND POLLUTION AMOUNTS PER VEHICLE
                if p.vehicle_choice == "Conventional Vehicle":
                    p.vehicle_cost = Constants.conventional_cost
                    p.vehicle_pollution = Constants.conventional_pollution
                    p.vehicle_utility = Constants.conventional_utility
                # THIS IS THE PUBLIC VEHICLE OPTION
                elif p.vehicle_choice == "Public Vehicle":
                    p.vehicle_cost = Constants.public_cost
                    p.vehicle_pollution = Constants.public_pollution
                    # SETTING UP THE HETEROGENEITY
                    if p.id_in_group == 1:
                        p.vehicle_utility = Constants.public_utility_1
                    elif p.id_in_group == 2:
                        p.vehicle_utility = Constants.public_utility_2
                    elif p.id_in_group == 3:
                        p.vehicle_utility = Constants.public_utility_3
                    elif p.id_in_group == 4:
                        p.vehicle_utility = Constants.public_utility_4
                    elif p.id_in_group == 5:
                        p.vehicle_utility = Constants.public_utility_5
                    elif p.id_in_group == 6:
                        p.vehicle_utility = Constants.public_utility_6
                elif p.vehicle_choice == "Electric Vehicle":
                    p.vehicle_cost = Constants.electric_cost
                    p.vehicle_pollution = Constants.electric_pollution
                    p.vehicle_utility = Constants.electric_utility
    # WE ASSIGN THE GROUP TOTAL POLLUTION AMOUNT
    pollution_contributions = [p.vehicle_pollution for p in players]
    group.total_pollution = sum(pollution_contributions)
    # WE ASSIGN INDIVIDUAL POLLUTION DAMAGE
    group.pollution_damage = group.total_pollution
    # WE ASSIGN THE GROUP TAXATION AMOUNT
    tax_contributions = [p.vehicle_tax for p in players]
    group.total_tax = sum(tax_contributions)
    # WE ASSIGN INDIVIDUAL TAXATION REDISTRIBUTION
    group.tax_redistribution = group.total_tax / Constants.players_per_group

    # WE ASSIGN PAYOFFS PER PLAYER (WITH TAXATION)
    for p in players:
        p.payoff = Constants.endowment + p.vehicle_utility + group.tax_redistribution \
                   - (p.vehicle_cost + p.vehicle_tax) - group.pollution_damage




# PAGES


# FIRST VOTING PAGE
class Vote(Page):
    # ONLY SHOWS THE APP ON THE ROUNDS WITH A VOTING STAGE
    # @staticmethod
    def is_displayed(player: Player):
        if player.round_number == Constants.stage1_round:
            return True
        elif player.round_number == Constants.stage2_round:
            return True
        elif player.round_number == Constants.stage3_round:
            return True
        else:
            return False

            # or Constants.stage2_round or Constants.stage3_round

    form_model = "player"
    form_fields = ["vote_taxation"]


# VOTING WAIT PAGE
class VoteWaitPage(WaitPage):
    # ONLY SHOWS THE APP ON THE FIRST ROUND
    # @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [Constants.stage1_round, Constants.stage2_round, Constants.stage3_round]

    after_all_players_arrive = set_majority


# VOTE RESULTS PAGE
class VoteResults(Page):
    # @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.stage3_round

    # @staticmethod
    def vars_for_template(player: Player):
        vote1 = player.group.in_round(Constants.stage1_round).vote_taxation
        vote2 = player.group.in_round(Constants.stage2_round).vote_taxation
        vote3 = player.group.in_round(Constants.stage3_round).vote_taxation

        # SETTING AN OUTPUT FOR THE ADMINISTRATOR NEED TO TEST IF THIS WORKS
        player.adopt_tax1 = vote1
        player.adopt_tax2 = vote2
        player.adopt_tax3 = vote3

        #########################

        players = player.group.get_players()
        policy_votes1 = [p.in_round(Constants.stage1_round).vote_taxation for p in players]
        policy_votes2 = [p.in_round(Constants.stage2_round).vote_taxation for p in players]
        policy_votes3 = [p.in_round(Constants.stage3_round).vote_taxation for p in players]
        for_vote1 = policy_votes1.count(True)
        against_vote1 = policy_votes1.count(False)
        for_vote2 = policy_votes2.count(True)
        against_vote2 = policy_votes2.count(False)
        for_vote3 = policy_votes3.count(True)
        against_vote3 = policy_votes3.count(False)

        return dict(
            # vote1=player.participant.vars['vote_taxation1'],
            # vote2=player.participant.vars['vote_taxation2'],
            # vote3=player.participant.vars['vote_taxation3'],
            vote1=vote1,
            vote2=vote2,
            vote3=vote3,
            for_vote1=for_vote1,
            for_vote2=for_vote2,
            for_vote3=for_vote3,
            against_vote1=against_vote1,
            against_vote2=against_vote2,
            against_vote3=against_vote3
        )

    # ASSIGNS TREATMENTS TO PLAYERS
    # @staticmethod
    def before_next_page(player: Player, timeout_happened):
        assign_treatment(player)


# VEHICLE CHOICE PAGE

class Instructions1(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions2(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions3(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions4(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions5(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions6(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsWaitPage(WaitPage):
    pass


class Comprehension(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    form_model = "player"
    form_fields = ["comprehension1", "comprehension2", "comprehension3"]


class VehicleChoice(Page):
    def is_displayed(player: Player):
        return player.round_number < Constants.stage3_round

    form_model = "player"
    form_fields = ["vehicle_choice"]

    def vars_for_template(player: Player):

        # DISPLAY FOR FIRST STAGE OF THE GAME
        if player.round_number < Constants.stage2_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_remaining = stage_duration - player.round_number
            stage_round = player.round_number
            current_stage = 1

        # DISPLAY FOR THE SECOND STAGE OF THE GAME
        elif Constants.stage2_round <= player.round_number < Constants.stage3_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_round = player.round_number - stage_duration
            stage_remaining = stage_duration - stage_round
            current_stage = 2
        # DISPLAY FOR THE THIRD STAGE OF THE GAME
        elif player.round_number >= Constants.stage3_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_round = player.round_number - Constants.stage3_round + 1
            stage_remaining = stage_duration - stage_round
            current_stage = 3

        # DISPLAY OF VOTE RESULTS

        # if player.round_number >= Constants.stage3_round:
        #    # CASE WITH TAXATION
        #   if player.treatment == "Tax":
        #        tax_present = 1
        #    if player.treatment == "NoTax":
        #        notax_present = 1
        # else:
        #   tax_present = 0
        #    notax_present = 0

        return dict(
            stage_remaining=stage_remaining,
            stage_round=stage_round,
            current_stage=current_stage,
            # tax_present=tax_present,
            # notax_present=notax_present
        )


class VehicleChoiceFinal(Page):
    def is_displayed(player: Player):
        return player.round_number >= Constants.stage3_round

    form_model = "player"
    form_fields = ["vehicle_choice"]

    def vars_for_template(player: Player):

        # DISPLAY FOR FIRST STAGE OF THE GAME
        if player.round_number < Constants.stage2_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_remaining = stage_duration - player.round_number
            stage_round = player.round_number
            current_stage = 1

        # DISPLAY FOR THE SECOND STAGE OF THE GAME
        elif Constants.stage2_round <= player.round_number < Constants.stage3_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_round = player.round_number - stage_duration
            stage_remaining = stage_duration - stage_round
            current_stage = 2
        # DISPLAY FOR THE THIRD STAGE OF THE GAME
        elif player.round_number >= Constants.stage3_round:
            stage_duration = Constants.stage2_round - Constants.stage1_round
            stage_round = player.round_number - Constants.stage3_round + 1
            stage_remaining = stage_duration - stage_round
            current_stage = 3
        final_policy = player.participant.vars['final_policy']

        return dict(
            stage_remaining=stage_remaining,
            stage_round=stage_round,
            current_stage=current_stage,
            final_policy=final_policy
            # tax_present=tax_present,
            # notax_present=notax_present
        )


# VEHICLE CHOICE WAITING PAGE
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


# VEHICLE CHOICE RESULT PAGE
class Results(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random

        participant = player.participant

        # if it's the last round
        if player.round_number == Constants.num_rounds:
            random_round = random.randint(1, Constants.num_rounds)
            participant.vars['selected_round'] = random_round
            player_in_selected_round = player.in_round(random_round)
            player.payoff_final = float(player_in_selected_round.payoff)
            participant.payoff = math.ceil(player.payoff_final)

    def vars_for_template(player: Player):
        # FETCHING OTHER PLAYERS VEHICLE CHOICE
        players = player.group.get_players()
        all_choices = [p.vehicle_choice for p in players]
        all_conventional = all_choices.count("Conventional Vehicle")
        all_public = all_choices.count("Public Vehicle")
        all_electric = all_choices.count("Electric Vehicle")
        player_choice = player.field_display('vehicle_choice')
        # FETCHING NUMBER OF PLAYERS WHO CHOSE THE CONVENTIONAL VEHICLE
        players = player.group.get_players()
        # all_choices = [p.vehicle_choice for p in players]
        # all_conventional = all_choices.count("Conventional Vehicle")

        # DISPLAY FOR FIRST STAGE OF THE GAME
        if player.round_number < Constants.stage2_round:
            stage_round = player.round_number

        # DISPLAY FOR THE SECOND STAGE OF THE GAME
        elif Constants.stage2_round <= player.round_number < Constants.stage3_round:
            stage_round = player.round_number - Constants.stage2_round + 1
        # DISPLAY FOR THE THIRD STAGE OF THE GAME
        elif player.round_number >= Constants.stage3_round:
            stage_round = player.round_number - Constants.stage3_round + 1

        if player.round_number != Constants.stage1_round and Constants.stage2_round and Constants.stage3_round:
            show_previous = 1
            prev_player = player.in_round(player.round_number - 1)
        else:
            show_previous = 0
            prev_player = 0

        return dict(
            all_conventional=all_conventional,
            all_public=all_public,
            all_electric=all_electric,
            player_choice=player_choice,
            stage_round=stage_round,
            show_previous=show_previous,
            prev_player=prev_player,


        )




page_sequence = [Instructions1, Instructions2, Instructions3, Instructions4, Instructions5, Comprehension,
                 InstructionsWaitPage, Vote, VoteWaitPage, VoteResults, VehicleChoice, VehicleChoiceFinal,
                 ResultsWaitPage, Results]

# page_sequence = [Instructions1, Instructions2, Instructions3, Instructions4, Instructions5, Comprehension,
#                 InstructionsWaitPage, Vote, VoteWaitPage, VoteResults, VehicleChoice, VehicleChoiceFinal,
#                 ResultsWaitPage, Results,
#                 Payoff]

#page_sequence = [VehicleChoice, VehicleChoiceFinal,
#                 ResultsWaitPage, Results,
#                 Payoff]

#page_sequence = [Vote, VoteWaitPage, VoteResults
#]
