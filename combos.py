#module for reading command line arguments
import argparse

#set up the argument parser for the command line
parser = argparse.ArgumentParser(description="Produce permutations/combos of a CeWL or other generated file with plain english words.")
parser.add_argument("-i", "--input", dest="wordlist", help="Input wordlist permutations", type=str, required=True)
parser.add_argument("-d", "--depth", dest="depth", help="Permutation depth (max words to combine)", type=int, required=True)
parser.add_argument("-o", "--output", dest="output", help="Output file", type=str, required=True)
parser.add_argument("-c", "--charbetween", dest="between", help="Insert a character between each word", type=str, required=False)
#the action="store_true" sets the value to a boolean "True" if the argument is present, do not specify a type
parser.add_argument("-ex", "--exclude", dest="exclude", help="Exclude permutations/combos that have less words than the specified depth", action="store_true", required=False)

#set the default value for "exclude" to false, unless the argument is specified
parser.set_defaults(exclude=False)

#get the arguments
args = parser.parse_args()

#read the contents of the file provided by the user
wordlist = open(args.wordlist, 'r')
wordlistlines = []
for line in wordlist.readlines():
	wordlistlines.append(line)

#get the amount of words to combine (combine 3 words max, for example)
iterations = args.depth

#the output file
output = open(args.output, 'w')

#recursive function for producing combos
def get_combos(lines, iters, prevlines=None):
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
				output.write(line.strip() + "\n")
		else: #if this is one of the content-generating iterations, produce comboss
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
						output.write(combo)
						nextlines.append(combo)

		#let the user know that we have passed this depth
		print("Depth Level:", (iterations - iters) + 1, "Completed...")

		#execute, or "return" the recursive function until we reach the base condition
		return get_combos(lines, iters-1, nextlines)
	else: #the last depth level was passed
		#close the file
		output.close()
		#return the complete list of the combos
		return prevlines

combos = get_combos(wordlistlines, iterations)

print(len(combos))
