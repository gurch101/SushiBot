import mousebot
import time
import numpy
import ImageGrab
import ImageOps
from threading import Timer

class GameCoords:
	# all coordinates are specified relative to this offset which marks the top
	# left corner of the game
	OFFSET = (37, 157)
	
	# Game menus
	PLAY_BUTTON = (321, 205)
	CONTINUE_BUTTON = (297, 392)
	SKIP_BUTTON = (584, 453)
	SECOND_CONTINUE_BUTTON = (310, 379)
	
	# Ingredients
	SHRIMP = (31, 331)
	RICE = (94, 331)
	NORI = (31, 387)
	ROE = (94, 387)
	SALMON = (31, 443)
	UNAGI = (94, 443)
	SUSHI_MAT = (212, 388)
	
	# Dirty Plates
	PLATES = [(94, 209),(198, 209),(297, 209),(398, 209),(499, 209),(602, 209)]
	
	# Customer Bubbles
	CUSTOMERS = [(34,53,79,83),(135,53,180,83),(236,53,281,83),(337,53,382,83),(438,53,483,83),(539,53,584,83)]
	
	# Phone navigation
	PHONE = (585, 361)
	PH_TOPPING_MENU = (543, 272)
	PH_RICE_MENU = (543, 293)
	PH_SAKE_MENU = (537, 316)
	PH_SHRIMP = (462, 210)
	PH_UNAGI = (548, 210)
	PH_NORI = (465, 275)
	PH_ROE = (549, 276)
	PH_SALMON = (465, 334)
	PH_RICE = (517, 282)
	PH_NORMAL_DELIVERY = (494, 295)
	PH_EXIT = (594, 338)
	
class GameColor:
	TOPPING_UNAVAILABLE_TO_ORDER = (109, 123, 127)
	RICE_UNAVAILABLE_TO_ORDER = (118,83,85)
	MAT_EMPTY = (232,232,204)
	CALI_REQUEST = 3439
	ONIGIRI_REQUEST = 2795
	GUNKAN_REQUEST = 2802
	SALMON_REQUEST = 2770
	SHRIMP_REQUEST = 3217
	UNAGI_REQUEST = 3018
	DRAGON_REQUEST = 3405
	COMBO_REQUEST = 4708
	
class Game:

	def __init__(self):
		self.screen = ()
		self.running = False
		self.NUM_CUSTOMERS = 6
		self.ingredients = {
			'RICE': {
				'ct': 10,
				'order_ct': 10,
				'coord': GameCoords.RICE,
				'order_coord': GameCoords.PH_RICE,
				'unavailable_color': GameColor.RICE_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_RICE_MENU
			},
			'SHRIMP': {
				'ct': 5, 
				'order_ct': 5,
				'coord': GameCoords.SHRIMP, 
				'order_coord': GameCoords.PH_SHRIMP,
				'unavailable_color': GameColor.TOPPING_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_TOPPING_MENU
			},
			'NORI': {
				'ct': 10,
				'order_ct': 10,
				'coord': GameCoords.NORI, 
				'order_coord': GameCoords.PH_NORI,
				'unavailable_color': GameColor.TOPPING_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_TOPPING_MENU			
			},
			'ROE': {
				'ct': 10,
				'order_ct': 10,
				'coord': GameCoords.ROE, 
				'order_coord': GameCoords.PH_ROE,
				'unavailable_color': GameColor.TOPPING_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_TOPPING_MENU			
			},
			'SALMON': {
				'ct': 5, 
				'order_ct': 5,
				'coord': GameCoords.SALMON, 
				'order_coord': GameCoords.PH_SALMON,
				'unavailable_color': GameColor.TOPPING_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_TOPPING_MENU
			},
			'UNAGI': {
				'ct': 5,
				'order_ct': 5,
				'coord': GameCoords.UNAGI, 
				'order_coord': GameCoords.PH_UNAGI,
				'unavailable_color': GameColor.TOPPING_UNAVAILABLE_TO_ORDER,
				'order_menu_coord': GameCoords.PH_TOPPING_MENU			
			}
		}
		
		self.rolls = {
			'CALI': {
				'ingredients': ['RICE','NORI','ROE'],
				'color': GameColor.CALI_REQUEST
			},
			'ONIGIRI': {
				'ingredients': ['RICE','RICE','NORI'],
				'color': GameColor.ONIGIRI_REQUEST
			},
			'GUNKAN': {
				'ingredients': ['RICE','NORI','ROE','ROE'],
				'color': GameColor.GUNKAN_REQUEST
			},
			'SALMON': {
				'ingredients': ['RICE', 'NORI', 'SALMON', 'SALMON'],
				'color': GameColor.SALMON_REQUEST
			},
			'SHRIMP': {
				'ingredients': ['RICE', 'NORI', 'SHRIMP', 'SHRIMP'],
				'color': GameColor.SHRIMP_REQUEST
			},
			'UNAGI': {
				'ingredients': ['RICE', 'NORI', 'UNAGI', 'UNAGI'],
				'color': GameColor.UNAGI_REQUEST
			},
			'DRAGON': {
				'ingredients': ['RICE', 'RICE', 'ROE', 'NORI', 'UNAGI', 'UNAGI'],
				'color': GameColor.DRAGON_REQUEST
			},
			'COMBO': {
				'ingredients': ['RICE', 'RICE', 'NORI', 'ROE', 'SALMON', 'UNAGI', 'SHRIMP'],
				'color': GameColor.COMBO_REQUEST
			}
		}
		
		self.pending_requests = range(len(self.ingredients))


	def make_roll(self,roll_name):
		for ingredient in self.rolls[roll_name]['ingredients']:
			ingredient = self.ingredients[ingredient]
			ingredient['ct'] -= 1
			left_click(ingredient['coord'])
		time.sleep(.5)
		left_click(GameCoords.SUSHI_MAT, 1.5)
	
	def clear_tables(self):
		for plate in GameCoords.PLATES:
			left_click(plate)
		
	def is_available_to_order(self, ingredient_name):
		ingredient = self.ingredients[ingredient_name]
		px_color = self.screen.getpixel(ingredient['order_coord'])
		return px_color != ingredient['unavailable_color']	
	
	def click_through_to_phone_menu(self, ingredient_name):
		left_click(GameCoords.PHONE)
		left_click(self.ingredients[ingredient_name]['order_menu_coord'],0.5)
		self.screen = screen_grab()
			
	def order_ingredient(self,ingredient_name):
		self.click_through_to_phone_menu(ingredient_name)
		
		if self.is_available_to_order(ingredient_name):
			ingredient = self.ingredients[ingredient_name]
			print "ordering " + ingredient_name
			left_click(ingredient['order_coord'],0.5)
			left_click(GameCoords.PH_NORMAL_DELIVERY, 0.5)
			return True
		else:
			print "insufficient funds for " + ingredient_name
			left_click(GameCoords.PH_EXIT, 0.5)		
			return False
			
	def order_low_ingredients(self):
		for ingredient_name, ingredient in self.ingredients.iteritems():
			if ingredient['ct']	< ingredient['order_ct'] * 0.4 \
			and ingredient_name not in self.pending_requests \
			and self.order_ingredient(ingredient_name):
				self.pending_requests.append(ingredient_name)
				Timer(8,self.add_ingredients,args=[ingredient_name]).start()

	def add_ingredients(self, ingredient_name):
		self.ingredients[ingredient_name]['ct'] += self.ingredients[ingredient_name]['order_ct']
		self.pending_requests.remove(ingredient_name)
		
	def get_customer_order(self,customer_num):
		im = screen_grab(GameCoords.CUSTOMERS[customer_num])	
		im = ImageOps.grayscale(im)
		a = numpy.array(im.getcolors())
		sum = a.sum()
		for roll_name, roll in self.rolls.iteritems():
			if roll['color'] == sum:
				return roll_name
		return 'BLANK'

	def has_sufficient_ingredients_for_roll(self, roll_name):
		ingredients = {}
		for ingredient_name, ingredient in self.ingredients.iteritems():
			ingredients[ingredient_name] = ingredient['ct']
			
		for ingredient_name in self.rolls[roll_name]['ingredients']:
			ingredients[ingredient_name] -= 1
			if ingredients[ingredient_name] < 0:
				return False
		return True
		
	def is_mat_empty(self):
		im = screen_grab()
		return im.getpixel(GameCoords.SUSHI_MAT) == GameColor.MAT_EMPTY
		
	def fill_customer_order(self):
		for i in xrange(self.NUM_CUSTOMERS):
			roll_name = self.get_customer_order(i)	
			if roll_name != 'BLANK' \
			and self.has_sufficient_ingredients_for_roll(roll_name) \
			and self.is_mat_empty():
					print "making " + roll_name
					self.make_roll(roll_name)
			
	def click_through_to_game(self):
		left_click(GameCoords.PLAY_BUTTON)
		left_click(GameCoords.CONTINUE_BUTTON)
		left_click(GameCoords.SKIP_BUTTON)
		left_click(GameCoords.SECOND_CONTINUE_BUTTON)
		
	def start(self):
		self.click_through_to_game()
		self.running = True
		while self.running:
			self.order_low_ingredients()
			self.fill_customer_order()
			self.clear_tables()
			
	def stop(self):
		self.running = False
	

def left_click(coord, sleep=0.1):
	mousebot.left_click(GameCoords.OFFSET[0] + coord[0], GameCoords.OFFSET[1] + coord[1])
	time.sleep(sleep)

def print_game_coords():
	x,y = mousebot.get_mouse_position()
	print x - GameCoords.OFFSET[0], y - GameCoords.OFFSET[1]

def screen_grab(coords=(1,1,641,481)):
	return ImageGrab.grab((GameCoords.OFFSET[0] + coords[0], GameCoords.OFFSET[1] + coords[1], GameCoords.OFFSET[0] + coords[2], GameCoords.OFFSET[1] + coords[3]))


	