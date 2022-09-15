from otree.api import *
import math

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'vehicle_choice_game_regulation_vote_all'
    players_per_group = 6
    num_rounds = 6

    # THE ROUND FOR NO POLICY
    stage1_round = 1
    # THE ROUND FOR POLICY
    stage2_round = 3
    # THE ROUND FOR POLICY OR NO POLICY
    stage3_round = 5

    # NAME OF THE TREATMENT
    TREATMENTS = ['Policy', 'NoPolicy']

    # THE PASSWORD FOR THE REGULATION PERIOD
    # regulation_password = "1234"

    # THE PASSWORD FOR THE NON REGULATION PERIOD
    # no_regulation_password = "abcd"

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
    # The Regulation is equal to the marginal damage of the vehicle's pollution
    conventional_regulation = conventional_pollution * (players_per_group - 1)
    public_regulation = 0
    electric_regulation = 0


class Subsession(BaseSubsession):

    # ASSIGNING TO ROLES

    def creating_session(self):
        # self.group_randomly()  # This randomizes the groups

        # Some role assignment below
        for p in self.get_players():
            if self.round_number == 1:
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
    total_regulation = models.IntegerField()
    regulation_redistribution = models.FloatField()
    # vote_regulation = models.BooleanField()

    # IS THIS ONE NESCESSARY ?
    vote_regulation = models.StringField()
    # IS THIS ONE NESCESSARY ?
    regulation_present = models.BooleanField(initial=0)




# FUNCTIONS







# ASSIGNING GROUP TO TREATMENT


class Player(BasePlayer):
    # THE TREATMENT TO WHICH THE PLAYER WAS ASSIGNED

    adopt_regulation1 = models.StringField()
    adopt_regulation2 = models.StringField()
    adopt_regulation3 = models.StringField()

    treatment = models.StringField(choices=Constants.TREATMENTS)

    vehicle_choice = models.StringField(
        label="Quelle est l'option que vous préférez?",
        choices=[
            ["Electric Vehicle", "Option A"],
            ["Public Vehicle", "Option B"],
            ["Conventional Vehicle", "Option C"]
        ]
    )

    vehicle_choice_regulation = models.StringField(
        label="Quelle est l'option que vous préférez?",
        choices=[
            ["Electric Vehicle", "Option A"],
            ["Public Vehicle", "Option B"]
        ]
    )


    vehicle_cost = models.IntegerField(initial=0)
    vehicle_pollution = models.IntegerField(intial=0)
    vehicle_utility = models.IntegerField(initial=0)
    vehicle_regulation = models.IntegerField(initial=0)
    player_random_round = models.IntegerField(initial=0)

    # THESE ARE THE PLAYER FIELDS THAT DETERMINE THE LAST STAGE OF THE GAME
    # password = models.StringField(label="Veuillez introduire le mot de passe indiqué par l’expérimentateur :")
    # final_policy = models.IntegerField(initial=0)

    # THIS IS THE FIELD FOR THE FINAL PAYOFF
    payoff_final = models.FloatField(initial=0)

    # THIS IS THE FIELD FOR REGULATION VOTE

    # FIRST POLICY VOTE
    vote_regulation = models.BooleanField(
        label="Souhaitez vous une mise en place de la regulatione à l'étape 2 de la Partie 3 ?",
        choices=[
            [True,
             "Oui, je souhaite la mise en place d'une regulatione de 25 ECUs pour chaque membre du groupe qui choisit l'option C."],
            [False, "Non, je ne souhaite pas la mise en place d'une regulatione de 25 ECUs."],
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
        label="3. Dans le cas où il y a une mise en place de la regulatione, combien d'ECUs supplémentaires"
              " devez vous payer si vous avez choisi l'option C ?",
        choices=[
            ["Option1", "0 ECUs"],
            ["Option2", "15 ECUs"],
            ["Option3", "25 ECUs"],
            ["Option4", "35 ECUs"],
        ]
    )


# HERE WE ASSIGN THE TREATMENTS TO THE GROUPS

# FUNCTIONS
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
    policy_votes = [p.vote_regulation for p in players]
    # If True is greater than half the amounts of player in the group
    # Then it is set as the majority
    if policy_votes.count(True) > (Constants.players_per_group / 2):
        # group.vote_regulation = True
        group.vote_regulation = "Adopted"
        # STORING FOR LATER APPS THAT THE GROUP MAJORITY HAS VOTED FOR THE SUBSIDY
        for player in players:
            if player.round_number == Constants.stage1_round:
                player.participant.vars['vote_regulation1'] = 1
            elif player.round_number == Constants.stage2_round:
                player.participant.vars['vote_regulation2'] = 1
            elif player.round_number == Constants.stage3_round:
                player.participant.vars['vote_regulation3'] = 1
    elif policy_votes.count(False) > (Constants.players_per_group / 2):
        # group.vote_regulation = False
        group.vote_regulation = "Not Adopted"
        # STORING FOR LATER APPS THAT THE GROUP MAJORITY HAS NOT VOTED FOR THE SUBSIDY
        for player in players:
            if player.round_number == Constants.stage1_round:
                player.participant.vars['vote_regulation1'] = 0
            elif player.round_number == Constants.stage2_round:
                player.participant.vars['vote_regulation2'] = 0
            elif player.round_number == Constants.stage3_round:
                player.participant.vars['vote_regulation3'] = 1
    else:
        group.vote_regulation = "Tie"

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
            # THIS IS THE CASE FOR WITHOUT REGULATION
            group.regulation_present = 0
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
            # THIS IS THE PAYOFF WITH REGULATION
            group.regulation_present = 1
            ####################################
                # THIS IS THE PUBLIC VEHICLE OPTION
            if p.vehicle_choice_regulation == "Public Vehicle":
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
            elif p.vehicle_choice_regulation == "Electric Vehicle":
                p.vehicle_cost = Constants.electric_cost
                p.vehicle_pollution = Constants.electric_pollution
                p.vehicle_regulation = Constants.electric_regulation
                p.vehicle_utility = Constants.electric_utility



        # PAYOFF FOR STAGE 3 : POLICY OR NO POLICY
        elif p.round_number >= Constants.stage3_round:

            # prev_vote_regulation = p.participant.vars['final_policy']
            final_policy = p.participant.vars['final_policy']
            if final_policy == "Policy":
                # THIS IS THE PAYOFF WITH REGULATION
                group.regulation_present = 1
                ##################################
                # THIS IS THE PUBLIC VEHICLE OPTION
                if p.vehicle_choice_regulation == "Public Vehicle":
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
                elif p.vehicle_choice_regulation == "Electric Vehicle":
                    p.vehicle_cost = Constants.electric_cost
                    p.vehicle_pollution = Constants.electric_pollution
                    p.vehicle_regulation = Constants.electric_regulation
                    p.vehicle_utility = Constants.electric_utility
                    # p.vehicle_subsidy = Constants.electric_subsidy
            elif final_policy == "NoPolicy":
                # THIS IS THE CASE FOR WITHOUT REGULATION
                group.regulation_present = 0
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
    # WE ASSIGN THE GROUP REGULATION AMOUNT
    # regulation_contributions = [p.vehicle_regulation for p in players]
    # group.total_regulation = sum(regulation_contributions)
    # WE ASSIGN INDIVIDUAL REGULATION REDISTRIBUTION
    # group.regulation_redistribution = group.total_regulation / Constants.players_per_group

    # WE ASSIGN PAYOFFS PER PLAYER (WITH REGULATION)
    for p in players:
        p.payoff = Constants.endowment + p.vehicle_utility  \
                   - p.vehicle_cost - group.pollution_damage




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
    form_fields = ["vote_regulation"]


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
        vote1 = player.group.in_round(Constants.stage1_round).vote_regulation
        vote2 = player.group.in_round(Constants.stage2_round).vote_regulation
        vote3 = player.group.in_round(Constants.stage3_round).vote_regulation

        # SETTING AN OUTPUT FOR THE ADMINISTRATOR NEED TO TEST IF THIS WORKS
        player.adopt_regulation1 = vote1
        player.adopt_regulation2 = vote2
        player.adopt_regulation3 = vote3

        #########################

        players = player.group.get_players()
        policy_votes1 = [p.in_round(Constants.stage1_round).vote_regulation for p in players]
        policy_votes2 = [p.in_round(Constants.stage2_round).vote_regulation for p in players]
        policy_votes3 = [p.in_round(Constants.stage3_round).vote_regulation for p in players]
        for_vote1 = policy_votes1.count(True)
        against_vote1 = policy_votes1.count(False)
        for_vote2 = policy_votes2.count(True)
        against_vote2 = policy_votes2.count(False)
        for_vote3 = policy_votes3.count(True)
        against_vote3 = policy_votes3.count(False)

        return dict(
            # vote1=player.participant.vars['vote_regulation1'],
            # vote2=player.participant.vars['vote_regulation2'],
            # vote3=player.participant.vars['vote_regulation3'],
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
        return player.round_number < Constants.stage2_round

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
        #    # CASE WITH REGULATION
        #   if player.treatment == "Regulation":
        #        regulation_present = 1
        #    if player.treatment == "NoRegulation":
        #        noregulation_present = 1
        # else:
        #   regulation_present = 0
        #    noregulation_present = 0

        return dict(
            stage_remaining=stage_remaining,
            stage_round=stage_round,
            current_stage=current_stage,
            # regulation_present=regulation_present,
            # noregulation_present=noregulation_present
        )



class VehicleChoiceRegulation(Page):
    def is_displayed(player: Player):
        return Constants.stage2_round <= player.round_number < Constants.stage3_round

    form_model = "player"
    form_fields = ["vehicle_choice_regulation"]

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
        #    # CASE WITH REGULATION
        #   if player.treatment == "Regulation":
        #        regulation_present = 1
        #    if player.treatment == "NoRegulation":
        #        noregulation_present = 1
        # else:
        #   regulation_present = 0
        #    noregulation_present = 0

        return dict(
            stage_remaining=stage_remaining,
            stage_round=stage_round,
            current_stage=current_stage,
            # regulation_present=regulation_present,
            # noregulation_present=noregulation_present
        )






class VehicleChoiceFinal(Page):
    def is_displayed(player: Player):
        return player.round_number >= Constants.stage3_round and player.participant.vars['final_policy'] == 'NoPolicy'

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
            # regulation_present=regulation_present,
            # noregulation_present=noregulation_present
        )



class VehicleChoiceFinalRegulation(Page):
    def is_displayed(player: Player):
        return player.round_number >= Constants.stage3_round and player.participant.vars['final_policy'] == 'Policy'

    form_model = "player"
    form_fields = ["vehicle_choice_regulation"]

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
            # regulation_present=regulation_present,
            # noregulation_present=noregulation_present
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

        # FOR ROUNDS WITH REGULATION
        if player.group.regulation_present == 1:
            all_choices = [p.vehicle_choice_regulation for p in players]
            player_choice = player.field_display('vehicle_choice_regulation')
        # FOR ROUNDS WITHOUT REGULATION
        elif player.group.regulation_present == 0:
            all_choices = [p.vehicle_choice for p in players]
            player_choice = player.field_display('vehicle_choice')


        all_conventional = all_choices.count("Conventional Vehicle")
        all_public = all_choices.count("Public Vehicle")
        all_electric = all_choices.count("Electric Vehicle")



        # FETCHING NUMBER OF PLAYERS WHO CHOSE THE CONVENTIONAL VEHICLE
        # players = player.group.get_players()
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







page_sequence = [Instructions1, Instructions2, Instructions3, Instructions4, Instructions5, Instructions6, Comprehension,
                 InstructionsWaitPage, Vote, VoteWaitPage, VoteResults,
                 VehicleChoice, VehicleChoiceRegulation, VehicleChoiceFinal, VehicleChoiceFinalRegulation,
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
