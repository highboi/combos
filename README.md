# combos.py

--- Combos.py ---
combos.py is a program to create permutations("combos") of words in a wordlist for password cracking shennanigans.
I came up with this whenever I had trouble creating permutations of a CeWL generated wordlist from the "crunch" tool.
The problem with using crunch for this task is that it produces EVERY possible permutation from a wordlist, meaning
that for a wordlist that is, for example, 1000 words/lines long, crunch will produce 1000 factorial combinations with
permutations being 1000 words long. The reason that crunch does this is because in the man page it says:

       -p charset OR -p word1 word2 ...
              Tells crunch to generate words that don't have repeating characters.   By  default  crunch  will  generate  a  wordlist  size  of  #of_chars_in_charset  ^
              max_length.   This  option will instead generate #of_chars_in_charset!.  The ! stands for factorial.  For example say the charset is abc and max length is
              4..  Crunch will by default generate 3^4 = 81 words.  This option will instead generate 3! = 3x2x1 = 6 words (abc, acb, bac, bca, cab, cba).  THIS MUST BE
              THE LAST OPTION!  This option CANNOT be used with -s and it ignores min and max length however you must still specify two numbers.

Note specifically "This option (...) ignores min and max length...", which is why it produces [wordlist length]!
combinations (! meaning factorial). This program attempts to solve this problem by allowing you to specify a "permutation depth"
or "combo depth", where you specify the amount of words you want to combine (do you want to combine maximum 2 words?) instead of
letting the program produce unreasonably long amounts of words. In the future I hope to add features to the mix by, for example,
allowing you to include permutations where letters are replaced with special characters (i.e a --> @ and s --> $) as well as
allowing for numbers and character permutations (similar to crunch with @ for lowercase chars, % for numbers, etc.).
