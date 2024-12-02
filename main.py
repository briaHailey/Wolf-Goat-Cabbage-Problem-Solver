import math
import copy

"""

Name:Bria Weisblat
Date: 01/28/24
Assignment:Assignment #3- Implement Search
Due Date: 01/28/24
About this project: This project uses a depth first search algorithm to solve the wolf goat cabbage problem.
The farmer must bring the cabbage, goat, and wolf across the river without leaving the goat alone with
the cabbage or the wolf alone with the goat.
Assumptions: Assume the boat can only hold the farmer and one other object.
All work below was performed by Bria Weisblat

"""

class State():
	def __init__(self, farmerLeft, wolfLeft, goatLeft, cabbageLeft, boat, farmerRight, wolfRight, goatRight, cabbageRight):
		self.farmerLeft = farmerLeft
		self.wolfLeft = wolfLeft
		self.goatLeft = goatLeft
		self.cabbageLeft = cabbageLeft
		self.boat = boat
		self.farmerRight = farmerRight
		self.wolfRight = wolfRight
		self.goatRight = goatRight
		self.cabbageRight = cabbageRight
		self.parent = None

	def is_goal(self):
		if self.farmerLeft == 0 and self.wolfLeft == 0 and self.goatLeft == 0 and self.cabbageLeft == 0:
			return True
		else:
			return False

	def is_valid(self):
		# check all invalid states

		# check left validity
		if (not self.farmerLeft):
			if (self.goatLeft and self.cabbageLeft):
				return False
			elif (self.goatLeft and self.wolfLeft):
				return False

		# check right validity
		elif (not self.farmerRight):
			if (self.goatRight and self.cabbageRight):
				return False
			elif (self.goatRight and self.wolfRight):
				return False

		return True


	def __eq__(self, other):
		if (self.farmerLeft == other.farmerLeft and self.wolfLeft == other.wolfLeft and self.goatLeft == other.goatLeft and self.cabbageLeft == other.cabbageLeft):
			if (self.farmerRight == other.farmerRight and self.wolfRight == other.wolfRight and self.goatRight == other.goatRight and self.cabbageRight == other.cabbageRight):
				if self.boat == other.boat:
					return True
		return False

	def __hash__(self):
		return hash((self.farmerLeft,self.wolfLeft,self.goatLeft,self.cabbageLeft,self.boat,self.farmerRight,self.wolfRight,self.goatRight, self.cabbageRight))

def printState(st):
	print(str(st.farmerLeft).center(15, ' ') + str(st.wolfLeft).center(17, ' ') + \
		  str(st.goatLeft).center(15, ' ') + str(st.cabbageLeft).center(17, ' ') \
		  + st.boat.center(7, ' ') + str(st.farmerRight).center(16, ' ') + \
		  str(st.wolfRight).center(18, ' ') + \
		  str(st.goatRight).center(15, ' ') + str(st.cabbageRight).center(17, ' '))

def successors(cur_state):
	children = []

	# need to add successors here...

	# new states are to be "appended" to the list
	# in search, states are popped off of the list (back to front)
	# seems like a STACK implementation

	# create a new test state as a child of cur_state

	# if farmer is left
	if cur_state.farmerLeft:
		# count possible options (not necessarily the valid ones)
		options = 1
		if cur_state.goatLeft:
			options += 1
		if cur_state.wolfLeft:
			options += 1
		if cur_state.cabbageLeft:
			options += 1
		# loop through all options for validity
		wolfTried = False
		goatTried = False
		cabbageTried = False
		for i in range(options):
			test_state = copy.deepcopy(cur_state)
			test_state.parent = copy.deepcopy(cur_state)
			test_state.farmerLeft = 0
			test_state.farmerRight = 1
			test_state.boat = 'right'
			# if the wolf is left, try moving it
			if test_state.wolfLeft and not wolfTried:
				test_state.wolfLeft = 0
				test_state.wolfRight = 1
				wolfTried = True
			elif test_state.cabbageLeft and not cabbageTried:
				test_state.cabbageLeft = 0
				test_state.cabbageRight = 1
				cabbageTried = True
			elif test_state.goatLeft and not goatTried:
				test_state.goatLeft = 0
				test_state.goatRight = 1
				goatTried = True
			last_state = test_state.parent.parent
			if not last_state:
				last_state = State(1,1,1,1,'left',0,0,0,0)
			if test_state.is_valid() and (test_state != last_state):

				children.append(test_state)

	# if farmer is right
	if cur_state.farmerRight:
		# count possible options (not necessarily the valid ones)
		options = 1
		if cur_state.goatRight:
			options += 1
		if cur_state.wolfRight:
			options += 1
		if cur_state.cabbageRight:
			options += 1
		# loop through all options for validity
		wolfTried = False
		goatTried = False
		cabbageTried = False
		for i in range(options):
			test_state = copy.deepcopy(cur_state)
			test_state.parent = copy.deepcopy(cur_state)
			test_state.farmerRight = 0
			test_state.farmerLeft = 1
			test_state.boat = 'left'
			# if the wolf is right, try moving it
			if test_state.wolfRight and not wolfTried:
				test_state.wolfRight = 0
				test_state.wolfLeft = 1
				wolfTried = True
			elif test_state.cabbageRight and not cabbageTried:
				test_state.cabbageRight = 0
				test_state.cabbageLeft = 1
				cabbageTried = True
			elif test_state.goatRight and not goatTried:
				test_state.goatRight = 0
				test_state.goatLeft = 1
				goatTried = True
			last_state = test_state.parent.parent
			if not last_state:
				last_state = State(1, 1, 1, 1, 'left',0,0,0,0)
			if test_state.is_valid() and not (test_state == last_state):
				children.append(test_state)

	return children

def explore_state(current_state, path, max_depth=10):
	# check if the current state is the goal state
	if current_state.is_goal():
		print("Reached the end state")
		return path + [current_state]

	if len(path) >= max_depth:
		return None  # Indicate a dead end

	# Recursive case: Explore successors
	next_states = successors(current_state)

	if not next_states:
		# No possible successors, it's a dead end
		print("Dead end")
		return None

	for next_state in next_states:
		if next_state.is_valid():
			# Recursively explore the next state
			result_path = explore_state(next_state, path+[current_state])
			if result_path is not None:
				return result_path

	return None

def search():
	initial_state = State(1, 1,1,1, 'left',0,0,0,0)
	frontier = successors(initial_state)


	path = []
	for upcoming_state in frontier:
		if upcoming_state.is_valid():
			result_path = explore_state(upcoming_state, [])
			if result_path:
				return result_path
			else:
				return None


def print_solution(solution):
	# path = []
	# path.append(solution)
	# if solution:
	# 	parent = solution.parent
	# while parent:
	# 	path.append(parent)
	# 	parent = parent.parent

	# initial state is not saved in "solution", so print initial state
	print(str(1).center(15, ' ') + str(1).center(17, ' ') + \
		  str(1).center(15, ' ') + str(1).center(17, ' ') \
		  + ("left").center(7, ' ') + str(0).center(16, ' ') + \
		  str(0).center(18, ' ') + \
		  str(0).center(15, ' ') + str(0).center(17, ' '))
	for t in range(len(solution)):
		state = solution[t]
		print(str(state.farmerLeft).center(15, ' ')  + str(state.wolfLeft).center(17, ' ') + \
				str(state.goatLeft).center(15, ' ') + str(state.cabbageLeft).center(17, ' ') \
				+ state.boat.center(7, ' ') + str(state.farmerRight).center(16, ' ') + \
						  str(state.wolfRight).center(18, ' ')+ \
				str(state.goatRight).center(15, ' ') + str(state.cabbageRight).center(17, ' '))


def main():
	solution = search()
	print(" solution:")
	print("Farmer Left   |    Wolf Left   |    Goat Left  | Cabbage Left |   Boat  | Farmer Right |  Wolf Right   |   Goat Right   |   Cabbage Right    ")
	print_solution(solution)

# if called from the command line, call main()
if __name__ == "__main__":
	main()