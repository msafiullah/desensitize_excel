#!/usr/bin/env python3

import sys
from random import shuffle
import pandas as pd


script = sys.argv[0]


def write_charmap(df, outfile):
	print ()
	print ("Writing character map file", outfile, "...")

	# Write out a csv file.
	df.to_csv(outfile, compression=None, index=False, sep="|")


def read_charmap(infile):
	print ()
	print ("Reading character map file", infile, "...")

	char_map_df = pd.read_csv(infile, sep="|", dtype=str)

	return char_map_df


def flip_charmap(df):
	print ()
	print ("Flipping character map ...")

	r1 = df.columns.tolist()
	r2 = df.loc[0,:].tolist()

	char_map_dict = dict(zip(r2, r1))

	df_flipped = pd.DataFrame(char_map_dict, index=[0])

	return df_flipped


def generate_charmap ():

	print ()
	print ("Generating character map dictionary ...")

	A_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	N_str = "0123456789"

	def str_to_list(value):
		l = []
		for i in range(0, len(value)):
			l.append(value[i])
		return l

	A_list = str_to_list(A_str)
	a_list = [x.lower() for x in A_list]
	N_list = str_to_list(N_str)

	A_list_shuffled = A_list.copy()
	N_list_shuffled = N_list.copy()

	shuffle(A_list_shuffled)
	a_list_shuffled = [x.lower() for x in A_list_shuffled]
	shuffle(N_list_shuffled)

	char_map_dict = dict(zip(A_list + a_list + N_list, A_list_shuffled + a_list_shuffled + N_list_shuffled))

	df_char_map = pd.DataFrame(char_map_dict, index=[0])

	return df_char_map


if __name__ == "__main__":

	# Check arguments
	if len(sys.argv) < 3 :
		print ("Usage: ", script, " <generate|flip> <char_map.csv>")
		sys.exit("Expecting 2 arguments.")

	# Parse arguments
	arg_command = sys.argv[1]
	arg_file = sys.argv[2]


	if arg_command == "generate":
		df = generate_charmap()
		write_charmap(df, arg_file)

	elif arg_command == "flip":
		df = read_charmap(arg_file)
		df_flipped = flip_charmap(df)
		write_charmap(df_flipped, arg_file)

	else:
		sys.exit("Invalid arg", arg_command)

