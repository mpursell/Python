# Simple beginnings of a dungeon game using an OOP approach
# Tested on Windows 7 / Ubuntu with Python2.7
# Michael Pursell

import random, sys

#create the base class for the hero
class Hero():
  
	#set some base stats for the hero
	stats = {'health':100, 'attack':25, 'defence':25, 'skill':1, 'poisoned':'no',}

	#create an inventory for the hero
	bag ={}

	#function to handle combat using the hero's and enemy's attributes
	def combat(self, enemy):
		
		fight_or_flight = raw_input('Type \'fight\' to fight or \'run\' to run:  ')
		
		if fight_or_flight == 'fight':
			print('\n----------Let Battle Commence-----------\n')

			current_health = self.stats['health']
			current_attack = self.stats['attack']
			current_defence = self.stats['defence']
			current_skill = self.stats['skill']
			current_poisoned = self.stats['poisoned']
			success = 'no'

			#if the hero's attack is better than the enemies defence, and his defence better than the enemies attack he wins outright.
			if current_attack > enemy.defence and current_defence > enemy.attack:
				print('You Win!')
				success = 'yes'
				return current_health, current_attack, current_defence, current_skill, current_poisoned, success

			elif current_attack < enemy.defence and current_defence > enemy.attack:
				print('\nYou clash, there is no winner, you strike again...')

				#as there is no clear winner, create randomish multipliers for the hero and enemy attacks.  
				#highest attack wins - no holds barred...
				hero_multiplier = random.choice(range(1, 5, 1))
				current_attack = (current_attack*hero_multiplier)+current_skill
				enemy_multiplier = random.choice(range(1, 5, 1))
				enemy.attack = enemy.attack*enemy_multiplier

				if current_attack >= enemy.attack:
					print('After a long struggle you slay the {}'.format(Goblin.name))
					success = 'yes'
					current_attack = (current_attack-current_skill)/hero_multiplier # undo the multipliers for attack
					return current_health, current_attack, current_defence, current_skill, current_poisoned, success

				#if the hero is beaten he retreats; unless the fight has drained his health past 0, in which case he dies.
				else:
					hero_damage = random.choice(range(1,4,1))
					current_health = current_health - hero_damage

					if current_health <= 0:
						print('You died!')
						sys.exit()
					else:
						print('You retreat after taking {} points of damage.  Your health is now {}'.format(hero_damage, current_health))
						return current_health, current_attack, current_defence, current_skill, current_poisoned, 

			#in the case of the enemy being clearly superior the hero retreats, taking maximum damage
			#the damage incurred is equal to that of the enemy's attack stat.
			#if the enemy has a poisoned blade, there is a chance here to use it on the hero
			else:
				if enemy.poison_blade > 70: #30% chance the blade is poisoned
					print('\nPoisoned!  \n')
					current_poisoned = 'Yes'
					current_health = current_health - enemy.attack
					print('You Lose!  You retreat quickly.  You\'ve lost {} health'.format(enemy.attack))
					return current_health, current_attack, current_defence, current_skill, current_poisoned
				else:
					current_health = current_health - enemy.attack
					print('You Lose!  You retreat quickly.  You\'ve lost {} health'.format(enemy.attack))
					return current_health, current_attack, current_defence, current_skill, current_poisoned
		else:
			print('You ran from the dungeon!')
			sys.exit()



	#function to handle the results of combat
	def result(self, enemy, combat_results):

		print('\n***********{} Battle Over************\n'.format(enemy.name))
		self.stats['health'] = combat_results[0]
		self.stats['attack'] = combat_results[1]
		self.stats['defence'] = combat_results[2]
		self.stats['skill'] = combat_results[3]
		self.stats['poisoned'] = combat_results[4]

		print('\nYour stats are now: \n\n {}'.format(self.stats))
	
	#function to take spoils of war	
	def take_item(self, combat_results, room_item):

		item_choice = raw_input('Would you like to take the {}? '.format(room_item))

		if item_choice == 'yes':
			self.bag[room_item] = '1' ####this needs amending to add to the dictionary properly###
			print('\nYour inventory is:\n {}'.format(self.bag))
		else:
			print('\nNo spoils of war this time!\n')
		


#base class for baddies
class Baddie():
	name = 'Minion'
	attack = 5
	defence = 5


class Goblin(Baddie):
	name = 'Goblin'
	attack = Baddie.attack*4
	defence = Baddie.defence*6


class Orc(Baddie):
	name = 'Orc'
	#generate some varying stats for the Orc
	attack = Baddie.attack*random.choice(range(1,7,1))
	defence = Baddie.defence*random.choice(range(1,7,1))
	#generate a blade integer to see if blade is poisoned or not
	poison_blade = random.choice(range(1,100,5))


#base class for rooms	
class Room():


	name = 'room'
	length = random.choice(range(5,20,2))
	width = random.choice(range(5,20,2))
	item = random.choice(range(1,3,1))
	enemy = random.choice(['Goblin', 'Orc'])


	orientation = '\nYou are in a {} {} by {} metres'.format(name, length, width)
	room_check = '\nThere is a {} in this room'.format(enemy)

	def roomScan(self):
		print self.orientation
		print self.room_check

	def roomItems(self):
		if self.item == 1:
			print('\nThere is a healing potion in this room\n')
			item = 'Healing Potion'
		elif self.item == 2:
			print('\nThere is a vial of antidote in this room\n')
			item = 'Antidote'		
		else:
			print('\nThere is a bookshelf in this room\n')
			item = 'Book'
		return item


class Corridor(Room):

	name = 'corridor'
	length = 15
	width = 3
	enemy = random.choice(['Goblin', 'Orc'])
	orientation = '\nYou are in a {} {} by {} metres'.format(name, length, width)
	room_check = '\nThere is a {} in this {}'.format(enemy, name)




def main():

	#create the hero
	my_guy = Hero()

	#create a room with items in it
	room1 = Room()
	room1.roomScan()
	room1.roomItems()

	raw_input('Press Enter to continue')

	#check which enemy is in the room and fight it
	if room1.enemy == 'Goblin':
		enemy = Goblin()
		combat = my_guy.combat(enemy)
		result = my_guy.result(enemy, combat)
		my_guy.take_item(combat, room1.roomItems())
	else:
		enemy = Orc()
		combat = my_guy.combat(enemy)
		result = my_guy.result(enemy, combat)
		my_guy.take_item(combat, room1.roomItems())
		




	corridor1 = Corridor()
	corridor1.roomScan()
	

	if corridor1.enemy == 'Goblin':
		enemy = Goblin()
		combat = my_guy.combat(enemy)
		result = my_guy.result(enemy, combat)
		
	else:
		enemy = Orc()
		combat = my_guy.combat(enemy)
		result = my_guy.result(enemy, combat)
		


if __name__=="__main__":
	main()
