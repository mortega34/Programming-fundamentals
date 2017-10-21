## Lab 8: Battle of the Bugs
## Name: Michael Ortega
## Hours Spent: 12

class Team(object):
    def __init__(self, team):
        """
        Initialize instance variables needed to keep track of the Team's status
        :param team: A list of dictionaries that stores all of the team's members and their movesets (see readme)
        """

        self.team_members = [Fighter(member) for member in team]
        #print self.team_members
        self.active_fighter_index = 0


    def get_active_fighter_name(self):
        """
        Return the name of the team member that is currently battling
        :return: string
        """
        return self.team_members[self.active_fighter_index].get_name()

    def get_active_fighter_state(self):
        try:
            return self.team_members[self.active_fighter_index].get_current_state()
        except IndexError:
            return 

    def get_active_fighter(self):
        return self.team_members[self.active_fighter_index]

    def switch(self):
        """
        Switch the active fighter to the next member on the team and return the name of the next fighter. If there are
        no more fighters left, return False
        :return: name of the next fighter (string) or False
        """
        self.active_fighter_index += 1
        if self.active_fighter_index < len(self.team_members):
            return self.team_members[self.active_fighter_index].get_name()
        return False





class Fighter(object):
    def __init__(self, member):
        self.name = member['name']
        self.max_energy = member['energy']
        self.energy = member['energy']
        self.attack = member['attack']
        self.defense = member['defense']
        self.moveset = member['moveset'][:]
        self.status = None
        self.status_remaining_time = 0
        self.redbull = 0

    def get_current_state(self):
        current_state = {}
        current_state["name"] = self.name
        current_state["energy"] = self.energy
        current_state["max_energy"] = self.max_energy
        current_state["status"] = self.status
        return current_state

    def get_max_energy(self):
        return self.max_energy

    def get_energy(self):
        return self.energy

    def set_energy(self, new_energy):
        self.energy = new_energy

    def get_attack_power(self):
        return self.attack

    def get_move_power(self, index):
        return self.moveset[index]['power']

    def get_defense(self):
        return self.defense

    def get_name(self):
        """
        Return name of fighter
        """
        return self.name

    def get_status(self):
        return self.status

    def set_status(self, effect, effect_time):
        self.status = effect
        if self.status_remaining_time == 0:
            self.status_remaining_time = effect_time

    def drink_redbull(self):
        self.redbull = 4

    def redbull_status(self):
        return self.redbull

    def update(self):
        if self.status == "sleep":
            #print self.status_remaining_time
            self.status_remaining_time -= 1
            if self.status_remaining_time == 0:
                self.set_status(None, 0)
            
        elif self.status == "poison":
            
            #print self.status_remaining_time
            if self.status_remaining_time != 0:
                self.energy -= 10
            if self.energy < 0:
                self.set_energy(0)
            if self.status_remaining_time == 0:
                self.set_status(None, 0)
            self.status_remaining_time -= 1
            

        if self.redbull > 0: 
            #print self.redbull
            self.redbull -= 1
            if self.redbull == 0 and self.status == None:
                self.set_status("sleep", 2)
                self.redbull = 0
            




class Battle(object):
    
    def __init__(self, staff, bugs):
        """
        Initialize instance variables needed to keep track of the battle state
        :param staff: a Team object representing the course staff
        :param bugs: a Team object representing the bugs
        """
        self.staff_team = staff
        self.bug_team = bugs
        self.current_staff_fighter = self.staff_team.get_active_fighter()
        self.current_bug_fighter = self.bug_team.get_active_fighter()
        self.staff_team_turn = True

    def turn(self, action, param):
        """
        Given an action name and action param, update the battle state to represent the current fighter taking
        the given action.

        :param action: If action is "attack", param will be the index of the move to use in the fighter's moveset.
        If action is "item", param will be the name of the item.
        """

        if self.current_staff_fighter.get_status() == "defeated":
            self.staff_team.switch()
            self.current_staff_fighter = self.staff_team.get_active_fighter()

        if self.current_bug_fighter.get_status() == "defeated":
            self.bug_team.switch()
            self.current_bug_fighter = self.bug_team.get_active_fighter()



        if self.staff_team_turn:# staff is performing action
            #print self.get_battle_state(),"\n"
            #print "Fighter: ",self.current_staff_fighter.get_name()," action: ", action," param: ", param



            # MAKE CHANGES DUE TO STATUS EFFECTS
            self.current_staff_fighter.update()

            # CHECK IF ANYBODY IS DEFEATED IF TRUE SWITCH TO NEXT FIGHTER
            # if current fighter dies from status effects switch to next but don't allow action
            if self.current_staff_fighter.get_energy() == 0:
                self.current_staff_fighter.set_status("defeated",0)
                action = None

            if action == "attack" and self.current_staff_fighter.get_status() != "sleep":
                self.do_attack(self.current_staff_fighter, self.current_bug_fighter, param)
            elif action == "item":
                self.use_item(self.current_staff_fighter, self.current_bug_fighter, param)
            self.staff_team_turn = False

            # Check if opponent was defeated at the end of this turn
            if self.current_bug_fighter.get_energy() == 0:
                self.current_bug_fighter.set_status("defeated",0)



        else:# bug is performing action

            #print self.get_battle_state(),"\n"
            #print "Fighter: ",self.current_bug_fighter.get_name()," action: ", action," param: ", param

             
            # MAKE CHANGES DUE TO STATUS EFFECTS
            self.current_bug_fighter.update()

            # CHECK IF ANYBODY IS DEFEATED IF TRUE SWITCH TO NEXT FIGHTER
            # if current fighter dies from status effects switch to next but don't allow action
            if self.current_bug_fighter.get_energy() == 0:
                self.current_bug_fighter.set_status("defeated",0)
                action = None

            if action == "attack" and self.current_bug_fighter.get_status() != "sleep":
                self.do_attack(self.current_bug_fighter, self.current_staff_fighter, param)
            elif action == "item":
                self.use_item(self.current_bug_fighter, self.current_staff_fighter, param)
            self.staff_team_turn = True

            # Check if opponent was defeated at the end of this turn
            if self.current_staff_fighter.get_energy() == 0:
                self.current_staff_fighter.set_status("defeated",0)

        
        

    def do_attack(self, attacker, defender, param):
        if attacker.redbull_status():
            #print "DOUBLE"
            damage = attacker.get_move_power(param) * (2 * attacker.get_attack_power()) / defender.get_defense()
        else:
            damage = attacker.get_move_power(param) * attacker.get_attack_power() / defender.get_defense()

        if defender.get_energy() - damage >= 0:
            defender.set_energy(defender.get_energy() - damage)
        else:
            defender.set_energy(0)




    #ITEM = {"coffee": coffee_effect, "redbull": redbull_effect, "pesticide": pesticide_effect, "textbook": textbook_effect}
    def use_item(self, attacker, defender, item):
        if item == "Coffee":
            max_energy = attacker.get_max_energy()
            current_energy = attacker.get_energy()

            if ( max_energy - current_energy ) <= 50:
                attacker.set_energy(max_energy)
            else:
                attacker.set_energy(current_energy+50)
        elif item == "Pesticide":
            if defender.get_status() == None:
                defender.set_status("poison", 5)
        elif item == "Red Bull":
            if attacker.redbull_status() == 0:
                attacker.drink_redbull()
        elif item == "Textbook":
            if defender.get_status() == None:
                defender.set_status("sleep", 3)


    def get_battle_state(self):
        """
        Return a list of dictionaries representing the current state of the active staff member and the active bug. The
        current state includes the fighter's name, current energy points, max energy, and status condition.

        Ex: [{"name": "Adam", "energy": 80, "max_energy": 100, "status": "poison"},
             {"name": "ASCII Ant", "energy": 30, "max_energy": 60, "status": None}]
        """
        return [self.staff_team.get_active_fighter_state(), self.bug_team.get_active_fighter_state()]

    def get_winner(self):
        """
        Return the name of the winning team, or None if neither team has won
        """
        if self.current_staff_fighter.get_status() != "defeated" and self.current_bug_fighter.get_status() == "defeated":
            return "staff"
        elif self.current_staff_fighter.get_status() == "defeated" and self.current_bug_fighter.get_status() != "defeated":
            return "bugs"
        return None
