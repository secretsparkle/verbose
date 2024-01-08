
def first(sequence):
	return sequence[0]

def rest(sequence):
	return sequence[1:]

def last(sequence):
	return sequence[-1]

def prepend(atom, sequence):
	sequence.insert(0, atom)

def append(atom, sequence):
	sequence.append(atom)
import random
number = 2 
value = 3 
def fn(x, y):
	print(x)
	print(y)
	return y 
fn(number, (number+value))
fn(number, value)
def is_two(x):
	if x == 2:
		return True
	else: 
		return False
def not_(x):
	if x: return False
	else: return True
print(is_two(number))
print(not_(is_two(number)))
sequence = [1, 2, 3, 4, 5]
print(first(sequence))
print(rest(sequence))
bool_value = not_(True)
print(bool_value)
prepend(0, sequence)
print(sequence)
sequence = []
prepend(1, sequence)
prepend(4, sequence)
append(5, sequence)
append(6, sequence)
print(sequence)
def is_even(value):
	if value % 2 == 0:
		return True
	else: return False
if is_even(first(sequence)): print("It's even")
else: print("it's not even")
print(first(sequence))
for value in sequence:
	print(value)
while True:
	print(sequence)
	break
def sum(sequence):
	value = 0 
	for element in sequence:
		value = ( (value + element))
	return value 
print(sum(sequence))
print(random.randint(0, 9))
