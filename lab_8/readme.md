# Battle of the Bugs

*Submission to website:* November 14, 10pm

*Checkoff by LA/TA*: November 17, 10pm

This lab assumes you have Python 2.7 installed on your machine.  Please use the Chrome web browser.

## Introduction

The 6.009 course staff has to release the next lab to you tomorrow at 9 AM, but they are only halfway done. Everything is going smoothly until midnight, when a swarm of nasty bugs suddenly starts attacking the staff. The course staff is now bombarded with out-of-range errors, stack overflows, and other nonsensical bugs, draining them of their already limited energy. The only way for the staff to make the deadline is to defeat the evil bugs in a battle by using their debugging skills. 

Your task is to simulate a turn-based battle between the staff and the bugs. Remember, if the staff can't release the lab, you automatically get a 0, so the fate of your grade is in your hands!


## Battle Mechanics

The staff members and bugs will fight on two opposing teams. Each team can send out one fighter at a time, and both fighters must stay in the battlefield until defeated. The bugs have shown some mercy by allowing the course staff to go first, but after that, both fighters must take turns.

Each fighter has a limited number of energy points. Attacks by the opposing team will inflict damage and deplete a figher's energy points. If a fighter's energy points falls to zero, he or she is defeated, and you must send out the next fighter on your team. When all of the fighters of a team are defeated, the team loses the battle.

### Fighter Attributes

Every fighter is different. For example, no two fighters can perform the same set of attacks. In addition, some have more stamina while others are more powerful. Each fighter is defined by the following attributes:

* *Max energy* - the number of energy points that the fighter starts with.
* *Attack* - determines how strong a fighter's attack is. A fighter with a high attack will deal more damage.
* *Defense* - determines how well a fighter can take hits. Attacks will do less damage on fighters with high defense.
* *Moveset* - the set of attacks that a fighter can use.

### Attacks

There are three factors that determine how much damage an attack inflicts on the opponent: the attack's base power, the attacker's attack, and the defender's defense. The formula for attack damage is:

	damage = base_power * (attacker's attack / defender's defense)

As mentioned in the previous section, damage increases as the attacker's attack increases, and it decreases as the defender's defense increases. If the attack and defense are equal, the damage will be equal to the attack's base power.

### Status Conditions 

To make things more interesting, fighters can also be affected by status conditions, which handicap them in different ways. Status conditions can be inflicted on opponents by using items (see below). The two possible status conditions are sleep and poison:

* *Sleep* - When a fighter falls asleep, it cannot attack its opponent their next 2 turns. However, the fighter can still use items.
* *Poison* - When a fighter is poisoned, it loses 10 energy points turn for 5 turns (in addition to damage from the opponent's move).

Status conditions can be very devastating, but the good news is that you can only be inflicted with one status condition at a time. If you use any status-inducing item on an opponent that is already poisoned or asleep, the item will do nothing. After your opponent recovers, you will be able to successfully use another status-inducing item.

### Items

In addition to attacking, you can also use items. You can use some items on yourself and others on your opponent. However, you can't use an item and also attack on the same turn. For example, drinking coffee will restore 50 energy points, but you lose your chance to inflict damage to your opponent for that turn. The available items are listed below:

* *Coffee* - Restores up to 50 energy points. You cannot exceed your maximum energy points.
* *Red Bull* - Doubles your attack for the next 3 turns, but then makes you fall asleep on the next turn after that. If you try to drink another Red Bull while your attack is doubled, the Red Bull will do nothing.
* *Pesticide* - Poisons your opponent.
* *Textbook* - Reading this out loud will make your opponent fall asleep.

## lab.py

You must implement your code in this file. You are not expected to read or write any other code provided as part of this lab. In addition, when you complete the lab, please fill in your name and hours spent at the top of the `lab.py` file. 

We will create a `Team` class to represent each team of fighters. The team parameter is represented as a list of dictionaries that store each fighter's attributes and moveset. Movesets are also stored as lists of dictionaries, where each dictionary contains the attack's name and power. Here is an example of how a team with two fighters is represented:

	[{"name": "Adam", "energy": 100, "attack": 70, "defense": 60,
	  "moveset": [{"name": "Print", "power": 10},
	  			  {"name": "Test Case", "power": 30}, 
	  			  {"name": "Refactor", "power": 25},
	  			  {"name": "Analyze", "power": 50}]},
	 {"name": "Chris", "energy": 120, "attack": 60, "defense": 80,
	  "moveset": [{"name": "Analyze", "power": 50},
	  			  {"name": "Computer Smash", "power": 5}, 
	  			  {"name": "Stack Trace", "power": 20},
	  			  {"name": "Refactor", "power": 25}]
	}]

### Warmup

Implement the `get_active_fighter_name()` and `switch()` methods in the `Team` class. `get_active_fighter_name()` should return the name of the fighter that is currently on the battlefield. `switch()` updates the active fighter to the next fighter on the team and either returns this next fighter's name or `False` if there are no more fighters left. When a battle starts, the active fighter should be the first member of the team.

Using the above example, calling `get_active_fighter_name()` should return "Adam" because he is the first fighter on the team. Calling `switch()` should then return "Chris". However, if we call `switch()` again, it should return `False` because Chris is the last member of the team.

### Battle Simulation

Next, we will create the `Battle` class to simulate the battle between the staff and the bugs. The `Battle` class takes in two `Team` objects that represent the course-staff team and the bugs team as parameters. You will need to implement three methods in the `Battle` class: `turn()`, `get_battle_state()`, and `get_winner()`. 

`turn()` is passed two arguments: `action` and `param`. *action* can either be "attack" or "item," and *param* specifies which attack or item should be used. 

* If the action is "attack", *param* will be an integer that represents the move corresponding to *param*'s index in the fighter's moveset. 

* If the action is "item", *param* will be a string that represents which item should be used. 

* Example: If it is Chris's turn and `turn("attack", 2)` is called, Chris should use the move "Stack Trace" since this move corresponds to index 2 in his moveset.

To implement `turn()` correctly, you will need to keep track of which team is currently attacking and then switch turns after the action has been completed. The `turn()` method should not return anything, but it should be updating instance variables in your classes to keep track of the states of both fighters. You will probably find it helpful to define another class to store each Fighter's attributes and then implement additional methods that can update these attributes.

`get_battle_state()` should return a representation of the current fighters' energy levels and status conditions. If a fighter is currently poisoned or asleep, the `"status"` field should be `"poison"` or `"sleep"`, respectively. If a fighter has been drained of all its energy, its `"status"` should be `"defeated"`. Otherwise, status should be `None`. You should return a list of dictionaries, where the first element in the list corresponds to the state of the active fighter on the course staff's team and the second element in the list corresponds to the active fighter on the bugs' team. 

**Example**: Adam and ASCII-Ant are currently on the battlefield. Adam is asleep and has 80/100 energy points, while ASCII Ant has 30/60 energy points and no status conditions. `get_battle_state()` should return:

	[{"name": "Adam", "energy": 80, "max_energy": 100, "status": "sleep"},
	 {"name": "ASCII Ant", "energy": 30, "max_energy": 60, "status": None}]

`get_winner()` should return the name of the winning team if there is one, and `None` otherwise. The name of the winning team should be either `"staff"` or `"bugs"`. When the last fighter on a team is defeated, we know that we can find a winner.

### Additional Clarifications
* If you are currently asleep, you may still choose an attack, but your attack will do nothing.
* If you are already poisoned and your opponent uses another Pesticide, the item will do nothing and your status timer does not get reset! 
* If you get poisoned right after drinking a Red Bull, you won't fall asleep after 3 turns due to the restriction that you can only have one status condition at a time.
* Status conditions take effect at the *beginning* of the turn. For example, if you are poisoned, you will first lose 10 energy points and then use an attack or item. Therefore, if you are poisoned while you have 10 or fewer energy points, you will be defeated before you get the chance to attack.
* Consequently, if a fighter on your team is defeated due to poisoning, you should switch to the next team member immediately instead of waiting until your next turn. Otherwise, your opponent will have no target for his or her next action.

The "Example Battles" section contains examples of these special cases.

## Example Battles

Here are two example battles between Adam and ASCII-Tarantula (as the sole members of their teams) to illustrate how the battle state changes on each turn:

**Staff team roster:**

    [{"name": "Adam", "energy": 100, "attack": 70, "defense": 60,
      "moveset": [{"name": "Print", "power": 10},
                  {"name": "Test Case", "power": 30}, 
                  {"name": "Refactor", "power": 25},
                  {"name": "Analyze", "power": 50}]}]

**Bugs team roster:**

    [{"name": "ASCII-Tarantula", "energy": 120, "attack": 60, "defense": 70,
      "moveset": [{"name": "Null Pointer", "power": 10},
                  {"name": "Deadlock", "power": 35}, 
                  {"name": "Blue Screen of Death", "power": 40},
                  {"name": "Heisenbug", "power": 50}]}]

### Example 1: Simple Battle

**Adam's turn:** `turn("item", "Pesticide")`

Adam uses a Pesticide, which poisons the Tarantula. `get_battle_state()` should now return:

    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "poison"}]

**ASCII Tarantula's turn:** `turn("attack", 0)`

Since ASCII Tarantula is poisoned, he loses 10 energy points immediately. Then he uses "Null Pointer," which deals 10 damage because Adam's defense is equal to the tarantula's attack. ASCII Tarantula will remain poisoned for 4 more turns.

    [{"name": "Adam", "energy": 90, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 110, "max_energy": 120,
      "status": "poison"}]

**Adam's turn:** `turn("attack", 1)`

Adam uses "Test Case," which deals 30 damage because ASCII Tarantula's defense is equal to Adam's attack.

    [{"name": "Adam", "energy": 90, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 80, "max_energy": 120,
      "status": "poison"}]

**ASCII Tarantula's turn:** `turn("attack", 2)`

Since ASCII Tarantula is still poisoned, he loses 10 energy points. Then he uses "Blue Screen of Death," which deals 40 damage. ASCII Tarantula will remain poisoned for 3 more turns.

    [{"name": "Adam", "energy": 50, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 70, "max_energy": 120,
      "status": "poison"}]

**Adam's turn:** `turn("item", "Coffee")`

Adam drinks some coffee, restoring 50 energy points.

    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 70, "max_energy": 120,
     "status": "poison"}]

**ASCII Tarantula's turn:** `turn("attack", 2)`

Since ASCII Tarantula is still poisoned, he loses 10 energy points. Then he uses "Blue Screen of Death" again, which deals 40 damage. ASCII Tarantula will remain poisoned for 2 more turns.

    [{"name": "Adam", "energy": 60, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 60, "max_energy": 120,
     "status": "poison"}]

**Adam's turn:** `turn("item", "Pesticide")`

Adam tries to use a Pesticide, but the Tarantula is already poisoned, so nothing happens. ASCII Tarantula still has 2 turns of poisoning left (the turn counter does not get reset).

	[{"name": "Adam", "energy": 60, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 60, "max_energy": 120,
      "status": "poison"}]

**ASCII Tarantula's turn:** `turn("attack", 2)`

Since ASCII Tarantula is still poisoned, he loses 10 energy points. Then he uses "Blue Screen of Death" again, which deals 40 damage. ASCII Tarantula will remain poisoned for 1 more turn.

    [{"name": "Adam", "energy": 20, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 50, "max_energy": 120,
     "status": "poison"}]

**Adam's turn:** `turn("attack", 3)`

Adam uses "Analyze", which deals 50 damage. ASCII Tarantula now has no energy points left, so he is defeated.

    [{"name": "Adam", "energy": 20, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 0, "max_energy": 120,
     "status": "defeated"}]

Since there are no more fighters left on the bugs team, this means that the course staff has won! `get_winner()` should now return `"staff"`.

### Example 2: More Items

**Adam's turn:** `turn('item', "Textbook")`

Adam uses the Textbook, which makes ASCII Tarantula fall asleep. 

    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "sleep"}]

**ASCII Tarantula's turn:** `turn('attack', 0)`

ASCII Tarantula wants to use "Null Pointer", but he is asleep, so nothing happens. ASCII Tarantula will wake up in 2 turns.
  
    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "sleep"}]

**Adam's turn:** `turn('item', "Red Bull")`

Adam drinks a Red Bull, doubling his attack to 140. The battle state is unchanged because Adam did not use an attack.

    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "sleep"}]

**ASCII Tarantula's turn:** `turn('item', "Coffee")`

ASCII Tarantula wants to drink some Coffee, but he is at his maximum energy, so nothing happens. ASCII Tarantula will wake up on the next turn.
  
    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "sleep"}]

**Adam's turn:** `turn('item', "Red Bull")`

Adam wants to drink another Red Bull, but he needs to wait for his first Red Bull to leave his system first, so the battle state is unchanged. The effects of his first Red Bull will last for 2 more turns.

    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": None},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": "sleep"}]

**ASCII Tarantula's turn:** `turn('item', "Pesticide")`

ASCII Tarantula wakes up! Now he uses a Pesticide to poison Adam.
  
    [{"name": "Adam", "energy": 100, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 120, "max_energy": 120,
      "status": None}]

**Adam's turn:** `turn('attack', 0)`

Adam loses 10 energy points because he is poisoned. Then he uses "Print." Print deals 20 damage because Adam's attack is 140 and Tarantula's defense is 70. Adam's Red Bull will last for 1 more turn.

    [{"name": "Adam", "energy": 90, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 100, "max_energy": 120,
      "status": None}]

**ASCII Tarantula's turn:** `turn("attack", 2)`

ASCII Tarantula uses "Blue Screen of Death", which deals 40 damage.

    [{"name": "Adam", "energy": 50, "max_energy": 100, "status": "poison"},
      {"name": "ASCII Tarantula", "energy": 100, "max_energy": 120,
       "status": None}]

**Adam's turn:** `turn('attack', 0)`

Adam loses 10 energy points because he is poisoned. Then he uses "Print" again, which deals 20 damage. Adam should fall asleep on the next turn.

    [{"name": "Adam", "energy": 40, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 80, "max_energy": 120,
      "status": None}]

**ASCII Tarantula's turn:** `turn("attack", 0)`

ASCII Tarantula uses "Null Pointer," which deals 10 damage.

    [{"name": "Adam", "energy": 30, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 80, "max_energy": 120,
      "status": None}]

**Adam's turn:** `turn('attack', 0)`

Adam loses 10 energy points because he is poisoned. Adam is supposed to fall asleep, but he is already poisoned. Then he uses "Print," which only deals 10 damage this time because his attack stat is back to normal.

    [{"name": "Adam", "energy": 20, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 70, "max_energy": 120,
      "status": None}]

**ASCII Tarantula's turn:** `turn("attack", 0)`

ASCII Tarantula uses "Null Pointer," which deals 10 damage. 

    [{"name": "Adam", "energy": 10, "max_energy": 100, "status": "poison"},
     {"name": "ASCII Tarantula", "energy": 70, "max_energy": 120,
      "status": None}]

**Adam's turn:** `turn('attack', 0)`

Adam loses 10 energy points because he is poisoned. Adam now has no more energy points, so he is defeated and cannot attack ASCII Tarantula again.

    [{"name": "Adam", "energy": 0, "max_energy": 100, "status": "defeated"},
     {"name": "ASCII Tarantula", "energy": 70, "max_energy": 120,
      "status": None}]

`get_winner()` should now return `"bugs"`.

## Testing your lab

To see the battle in action, run `server.py` and open your browser to `localhost:8000`. You will be able to step through three full battles between the 6.009 course staff and the bugs.

As before, you can run `test.py` to verify the correctness of your code. Each test case for the battle-simulation portion of the lab will pass in a series of actions. The .out files contain lists of battle states, each recording all intermediate states between turns, so you may find it helpful to look at the .out files when debugging. If you want to see all of the possible staff members' and bugs' stats and movesets, you can find them in `resources/fighters.json` and `resources/moves.json`.

Does your lab work? Do all tests in `test.py` pass? You're done! Submit your `lab.py` on [fun.csail.mit.edu](https://fun.csail.mit.edu) and get your lab checked off by a friendly staff member. 
