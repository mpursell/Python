# Shopping list creator
# Creates the list using the classes of meal you define
# Tested under Windows 7, Python2.7
# Michael Pursell 2013

#base class
class Food():

  Meat = []
	Carbs = []
	Veg = []
	Herbs = []
	Cooked_meat = []
	Dog_meat = []
	Salad = []
	Junk = []
	Breakfast = []
	Drinks = []
	Dairy = []
	Wine = []
	Oil = []
	Fruit = []
	
	#function that iterates over the lists of ingredients and adds them to a 'master' list for each recipe
	def list_ingredients(self):
		
		list = []
		for carbs in self.Carbs:
			list.append(carbs)
		for herbs in self.Herbs:
			list.append(herbs)
		for cooked_meat in self.Cooked_meat:
			list.append(cooked_meat)
		for dog in self.Dog_meat:
			list.append(dog)
		for salad in self.Salad:
			list.append(salad)
		for junk in self.Junk:
			list.append(junk)
		for breakfast in self.Breakfast:
			list.append(breakfast)
		for drink in self.Drinks:
			list.append(drink)
		for dairy in self.Dairy:
			list.append(dairy)
		for veg in self.Veg:
			list.append(veg)
		for oil in self.Oil:
			list.append(oil)
		for wine in self.Wine:
			list.append(wine)
		for fruit in self.Fruit:
			list.append(fruit)
		return list

		
#classes that hold the ingredients for each recipe		
class Bolognese(Food):

	name = 'Bolognese'
	Meat = ['Beef Mince']
	Carbs = ['Pasta']
	Veg = ['Onion','Carrots','Garlic', 'Tinned Tomatos']
	Herbs = ['Basil', 'Oregano']
	Wine = ['Red Wine']
	
	
class Risotto(Food):

	name = 'Risotto'
	Carbs = ['Arborio Rice']
	Veg = ['Onion','Courgette','Peppers', 'Celery', 'Tomato']
	Herbs = ['Bouquet Garni']
	Wine = ['White Wine']


class ChickenBake(Food):

	name = 'Chicken Bake'
	Meat = ['Chicken Breast', 'Sausages', 'Chorizo']
	Carbs = ['New Potatoes']
	Veg = ['Red Onion', 'Onion','Peppers','Cherry Tomato']
	Herbs = ['Paprika', 'Oregano', 'Black Pepper']
	Wine = ['White Wine']
	

		
class AnchovyPasta(Food):

	name = 'Anchovy Pasta'
	Meat = ['Anchovies']
	Carbs = ['Pasta']
	Veg = ['Garlic', 'Passata']
	Dairy = ['Creme Fraiche']

class SausageAndMash(Food):

	name = 'Sausage and Mash'
	Meat = ['Sausages']
	Carbs = ['Potatoes']
	Veg = ['Baked Beans']


class RoastDinner(Food):

	name = 'Roast Dinner'
	Meat = ['Joint / Chicken']
	Carbs = ['Potatoes']
	Veg = ['Green Beans']
	


class ChickenCalvados(Food):

	name = 'Chicken Calvados'
	Meat = ['Chicken Breast']
	Carbs = ['Potatoes']
	Veg = ['Green Beans']
	Dairy = ['Cream', 'Butter']
	Fruit = ['Crisp Eating Apples']


		
class CountryPie(Food):

	name = 'Country Pie'
	Meat = ['Beef Mince']
	Carbs = ['Potatoes']
	Veg = ['Peas', 'Carrots']


class BaconAndTomatoPasta(Food):

	name = 'Bacon and Tomato Pasta'
	Meat = ['Bacon']
	Carbs = ['Pasta']
	Veg = ['Tomatos', 'Onion', 'Garlic']
		


class LatinosPasta(Food):

	name = 'Latino\'s Special Pasta'
	Meat = ['Pepperoni']
	Carbs = ['Pasta']
	Veg = ['Passata', 'Red Onion', 'Garlic', 'Peppers']
	Dairy = ['Cream']

	
class BeefBourgignon(Food):

	name = 'Beef Bourgignon'
	Meat = ['Diced Beef']
	Carbs = ['Potatoes']
	Veg = ['Carrots', 'Onion', 'Garlic']
	Wine = ['Red Wine']
	
class ChickenInCider(Food):
	
	name = 'Chicken In Cider'
	Meat = ['Chicken Breast']
	Carbs = ['Potatoes', 'Flour']
	Veg = ['Carrots', 'Onion']
	Wine = ['Cider']
	Dairy = ['Butter']	
	

#class to hold the weekly purchases / checks	
class Weekly(Food):
			
	Meat = []
	Carbs = ['Bread','Wraps']
	Veg = []
	Herbs = ['Stock']
	Cooked_meat = ['Chicken Pieces', 'Sandwich Meat']
	Dog_meat = ['Dog Mince']
	Salad = ['Lettuce','Tomato','Cucumber','Peppers']
	Junk = ['Crisps', 'Chocolate Biscuits']
	Breakfast = ['Cereal', 'Breakfast Biscuits']
	Drinks = ['Barley Water', 'Lemonade', 'Beer','Tea']
	Dairy = ['Milk', 'Eggs', 'Cheese', 'Butter']
	Wine = []
	Oil = ['Olive Oil']

	
def main():

	#create the empty shopping list
	shoppingList = []
	
	#instantiate the meal objects from their respective classes
	bolognese = Bolognese()
	risotto = Risotto()
	weekly = Weekly()
	chickenBake = ChickenBake()
	anchovyPasta = AnchovyPasta()
	sausageAndMash = SausageAndMash()
	roastDinner = RoastDinner()
	chickenCalvados = ChickenCalvados()
	countryPie = CountryPie()
	baconAndTomatoPasta = BaconAndTomatoPasta()
	latinosPasta = LatinosPasta()
	beefBourgignon = BeefBourgignon()
	chickenInCider = ChickenInCider()


	
	#provide a list of meals to choose from
	print('\nPlease choose from the following meals (seperate each choice with a comma):\n\n1: {}\n2: {}\n3: {}\n4: {}\n5: {}\n6: {}\n7: {}\n8: {}\n9: {}\n10: {}\n11: {}\n\n'.format(bolognese.name, chickenBake.name, risotto.name, anchovyPasta.name, roastDinner.name, chickenCalvados.name, countryPie.name, baconAndTomatoPasta.name, latinosPasta.name, beefBourgignon.name,chickenInCider.name))
	
	#take the choice as input
	mealInput = raw_input('Enter the numbers of the meals you\'d like: ')
	
	#create an empty list
	mealChoice = []
	
	#iterate over the items from the input, splitting them by comma, then appending each item to the mealChoice list
	selection = mealInput.split(',')
	for item in selection:
		mealChoice.append(item)
	raw_input('You chose {}\nPress Enter to continue:\n'.format(mealChoice))
	
	#create an empty list of meal names to track what we've selected
	mealList = []
	
	#corrsponds to the order in the print statement above
	#iterate over the list created from the raw_input and select the ingredients
	for item in mealChoice:
		if item == '1':
			shoppingList = shoppingList + bolognese.list_ingredients()
			mealList.append(bolognese.name)
		if item == '2':
			shoppingList = shoppingList + chickenBake.list_ingredients()
			mealList.append(chickenBake.name)
		if item == '3':
			shoppingList = shoppingList + risotto.list_ingredients()
			mealList.append(risotto.name)
		if item == '4':
			shoppingList = shoppingList + anchovyPasta.list_ingredients()
			mealList.append(anchovyPasta.name)
		if item == '5':
			shoppingList = shoppingList + roastDinner.list_ingredients()
			mealList.append(roastDinner.name)
		if item == '6':
			shoppingList = shoppingList + chickenCalvados.list_ingredients()
			mealList.append(chickenCalvados.name)
		if item == '7':
			shoppingList = shoppingList + countryPie.list_ingredients()
			mealList.append(countryPie.name)
		if item == '8':
			shoppingList = shoppingList + baconAndTomatoPasta.list_ingredients()
			mealList.append(baconAndTomatoPasta.name)
		if item == '9':
			shoppingList = shoppingList + latinosPasta.list_ingredients()
			mealList.append(latinosPasta.name)
		if item == '10':
			shoppingList = shoppingList + beefBourgignon.list_ingredients()
			mealList.append(beefBourgignon.name)
		if item == '11':
			shoppingList = shoppingList + chickenInCider.list_ingredients()
			mealList.append(chickenInCider.name)
		
	#always tack on the weekly list
	shoppingList = shoppingList + weekly.list_ingredients()
	
	#make the list a set, this removes duplicates, then convert back to a list 
	shoppingList = sorted(list(set(shoppingList)))
	
	with open("c:\shoppingList.txt",'w') as file:
	
		file.write('List:\n\n')
		#print the list in a nice pretty format
		for entry in shoppingList:
			print(entry)
			file.write(entry+'\n')
			
		#print the meals we've chosen
		print('\n\n\nMeals:\n')
		file.write('\n\n\nMeals:\n\n')
		for entry in mealList:
			print(entry)
			file.write(entry+'\n')
			
	
	



if __name__=="__main__":
	main()
