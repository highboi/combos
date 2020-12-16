#module for reading command line arguments
import argparse

args = ""
iterations = ""

#function for setting up the arguent parser and returning the arguments
def get_args():
	#set up the argument parser for the command line
	parser = argparse.ArgumentParser(description="Produce permutations/combos of a CeWL or other generated file with plain english words.")
	parser.add_argument("-i", "--input", dest="wordlist", help="Input wordlist permutations", type=str, required=True)
	parser.add_argument("-d", "--depth", dest="depth", help="Permutation depth (max words to combine)", type=int, required=True)
	parser.add_argument("-o", "--output", dest="output", help="Output file", type=str, required=True)
	parser.add_argument("-cb", "--charbetween", dest="between", help="Insert a character between each word", type=str, required=False)
	parser.add_argument("-c", "--char", dest="expression", help="Expression for permutations: \"@\" will insert lowercase chars, \",\" will insert uppercase chars, \"%%\" will insert numbers, and \"^\" will insert symbols. Use \"[**]\" to represent each permutation", type=str, required=False)
	#the action="store_true" sets the value to a boolean "True" if the argument is present, do not specify a type
	parser.add_argument("-ex", "--exclude", dest="exclude", help="Exclude permutations/combos that have less words than the specified depth", action="store_true", required=False)

	#set the default value for "exclude" to false, unless the argument is specified
	parser.set_defaults(exclude=False)

	#get the arguments
	args = parser.parse_args()

	#return the arguments
	return args

#recursive function for producing combos
def get_basic_combos(lines, iters, writefile=None, prevlines=None):
	#first, we check to see if we have hit the limit for our combos, meaning that
	#we have produced all of the possible combinations up to <iters> amount of words
	if (iters >= 1):
		#create a nextlines list
		nextlines = []
		#if this is the first iteration in the recursive function, add all of the content
		#from "lines" in here
		if (prevlines is None):
			for line in lines:
				nextlines.append(line.strip() + "\n")
				if (writefile is not None):
					writefile.write(line.strip() + "\n")
		else: #if this is one of the content-generating iterations, produce combos
			#first, add all of the previous combos to the list to maintain the combinations that were previously made
			if (not args.exclude): #check to see if the user has not specified to exclude word depths below the number specified
				for prevline in prevlines:
					combo = prevline.strip() + "\n"
					nextlines.append(combo)
			#loop through the base wordlist content and combine it with the previous combinations of the words
			#to produce a more complex combo
			for line in lines:
				for prevline in prevlines:
					#check for adding a character between the strings
					if (not (args.between == None)):
						combo = line.strip() + args.between + prevline.strip() + "\n"
					else:
						combo = line.strip() + prevline.strip() + "\n"

					#make sure not to add a duplicate
					if (combo not in nextlines):
						nextlines.append(combo)
						if (writefile is not None):
							writefile.write(combo)

		#let the user know that we have passed this depth
		print("Depth Level:", (iterations - iters) + 1, "Completed...")

		#execute, or "return" the recursive function until we reach the base condition
		return get_basic_combos(lines, iters-1, writefile, nextlines)
	else: #the last depth level was passed
		if (writefile is not None):
			#tell the user that we wrote basic combos into the output file WITHOUT the expression
			print("Wrote primitive combos into:", writefile.name, "(no expressions added yet)...")
		#return the complete list of the combos
		return prevlines

#this is a function for getting the expression portions of the words
def get_expressions(combos, expression):
	#get the parts of the expression with the word divider
	expparts = expression.split("[**]")

	#get the alphabet in lower and upper cases, numbers, and symbols
	alphabet = [char for char in "abcdefghijklmnopqrstuvwxyz"]
	alphabetupper = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
	numbers = [num for num in "1234567890"]
	symbols = [sym for sym in "!@#$%&*()_-+=/?~"]

	#store the expressions in this list
	explist = []

	#loop through the expression parts
	for exp in expparts:
		#set a "final" list for the generated expressions for this expression portion
		final = []
		#loop through all the characters in this expression portion
		for char in exp:
			#create a temporary list to store the items
			temp = []

			#check for lowercase chars
			if (char == "@" and len(final) > 0): #if the "final" list has items in it, then loop through the "final" list and replace chars there
				for item in final:
					for letter in alphabet:
						temp.append(item.replace("@", letter, 1))
				final = temp
			elif (char == "@"): #if the "final" list is empty, add items to the list
				for letter in alphabet:
					final.append(exp.replace("@", letter, 1))

			#check for uppercase expressions, with the same behavior as the above
			if (char == "," and len(final) > 0):
				for item in final:
					for upper in alphabetupper:
						temp.append(item.replace(",", upper, 1))
				final = temp
			elif (char == ","):
				for upper in alphabetupper:
					final.append(exp.replace(",", upper, 1))

			#check for numberical expressions
			if (char == "%" and len(final) > 0):
				for item in final:
					for num in numbers:
						temp.append(item.replace("%", num, 1))
				final = temp
			elif (char == "%"):
				for num in numbers:
					final.append(exp.replace("%", num, 1))

			#check for symbol expressions
			if (char == "^" and len(final) > 0):
				for item in final:
					for sym in symbols:
						temp.append(item.replace("^", sym, 1))
				final = temp
			elif(char == "^"):
				for sym in symbols:
					final.append(exp.replace("^", sym, 1))

			#add the expression if it does not contain any characters
			if (char not in ["@", ",", "%", "^"]):
				final.append(exp)

		#add this final list of expressions to the newlist list
		explist.append(final)

	#return the total list of expressions
	return explist

#this is a function to get all of the permutations using expressions and basic combinations
def get_exp_combos(combos, expressions, writefile):
	#check to see if we do not need to combine expressions with combos
	if (expressions[0] == [] and expressions[1] == []):
		#write the original combos to the file
		for combo in combos:
			writefile.write(combo)
		#return the original combos list, as there are no expressions to add
		return combos

	#store the final list of combos combined with the expressions specified by the user
	final = []

	#loop through the combos
	for combo in combos:
		#check to see if the first part of the expressions list is not blank
		if (expressions[0] != []):
			#loop through the first part of the expressions list
			for exp1 in expressions[0]:
				#if there is a second part of the expressions list to be added to the string combos
				if (expressions[1] != []):
					#loop through the second part of the expressions list
					for exp2 in expressions[1]:
						#append the string to a list and write the string to the file
						finalstring = exp1 + combo.strip() + exp2 + "\n"
						final.append(finalstring)
						writefile.write(finalstring)
				else: #if there is no second part to the expressions list
					#add the first part to the string combo and write it to the file
					finalstring = exp1 + combo.strip() + "\n"
					final.append(finalstring)
					writefile.write(finalstring)
		elif (expressions[1] != []): #check to see that the second part of the expressions list is not blank, if the first one is
			#loop through the second part of the expressions, as there is no first portion to be iterated through and added
			for exp2 in expressions[1]:
				#add the string to the file
				finalstring = combo.strip() + exp2 + "\n"
				final.append(finalstring)
				writefile.write(finalstring)

	#return the permutation list
	return final

#the function to get all of the combinations and handle all the logic pertaining to combinations
def get_combos(lines, iters, writefile):
	#check for if we need to add expressions to our permutations/combos
	if (args.expression is None):
		#get the basic combos and write them to the file
		get_basic_combos(lines, iters, writefile)
	elif (args.expression is not None):
		#get the basic permutations
		basic_combos = get_basic_combos(lines, iters)
		#get the expressions based on the user's expression
		exps = get_expressions(basic_combos, args.expression)
		#produce the final product of combos combined with expressions and write to the file
		get_exp_combos(basic_combos, exps, writefile)

#the main function
def main():
	#set up the argument parser and get the arguments from the command line
	global args
	args = get_args()

	#read the contents of the file provided by the user
	wordlist = open(args.wordlist, 'r')
	wordlistlines = []
	for line in wordlist.readlines():
		wordlistlines.append(line)

	#get the amount of words to combine (combine 3 words max, for example)
	global iterations
	iterations = args.depth

	#the output file to write to
	output = open(args.output, 'w')

	#get the basic combinations
	get_combos(wordlistlines, iterations, output)


#execute the main function
if __name__ == "__main__":
	main()
