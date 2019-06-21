#!/usr/bin/env python3

import sys
import os.path
import pandas as pd
from hashlib import md5
from random import shuffle


script = sys.argv[0]

if len(sys.argv) < 5 :
	print ("Usage: ", script, " <excel_file> <sheet_name> <cols_to_hash_sep_by_comma> <cols_to_mask_sep_by_comma> [char_map.csv]")
	sys.exit("Expecting at least 4 arguments.")

excel_file = sys.argv[1]
sheet_name = sys.argv[2]
cols_to_hash = []
if sys.argv[3] != '':
	cols_to_hash = sys.argv[3].split(',')
cols_to_mask = []
if sys.argv[4] != '':
	cols_to_mask = sys.argv[4].split(',')

CHAR_MAP_DICT = None

if len(sys.argv) > 5 :
	char_map_csv = sys.argv[5]
	char_map_df = pd.read_csv(char_map_csv, sep="|", dtype=str)
	CHAR_MAP_DICT = char_map_df.to_dict('records')[0]



def read_excel(excel_file, sheet_name):
	if os.path.exists(excel_file) == False:
		error_msg = "ERROR: Excel file not found: {}".format(excel_file)
		sys.exit(error_msg)

	print ()
	print ("Reading excel", excel_file, "...")

	# Read excel file
	df = pd.read_excel(excel_file, sheet_name, dtype=str)

	return df


def write_csv(df, outfile_name):
	outfile = outfile_name + '.csv'

	print ()
	print ("Writing csv file", outfile, "...")

	# Write out a csv file.
	df.to_csv(outfile, compression=None, index=False, sep="|")


def write_excel(df, outfile_name):
	outfile = outfile_name + '.xlsx'

	print ()
	print ("Writing excel file", outfile, "...")

	# Write out a csv file.
	df.to_excel(outfile, index=False)


def digest (x):
	hash = md5()
	# Convert to unicode string
	x = str(x)

	if x.upper() == 'NULL' or x == '' or x is None:
		return "NULL"

	hash.update(x.encode('utf-8'))
	m = hash.hexdigest()

	return m[0:5] + '-' + m[5:10] + '-' + m[-5:]


def generate_char_map ():

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

	return char_map_dict


def remap_char (value):

	value = str(value)

	if value.upper() == 'NULL' or value == '' or value is None:
		return "NULL"

	result = ""
	for i in range(0, len(value)):
		c = value[i]

		if c in CHAR_MAP_DICT:
			result = result + CHAR_MAP_DICT[c]
		else:
			result = result + c

	return result


def anonymize_df(df, selected_cols):

	print ()
	print ("Anonymize columns", selected_cols, "...")

	for i, header_value in enumerate(selected_cols):
		if header_value in df.columns:
			df[header_value] = df[header_value].apply(digest)


def mask_df(df, selected_cols):

	print ()
	print ("Mask columns", selected_cols, "...")

	for i, header_value in enumerate(selected_cols):
		if header_value in df.columns:
			df[header_value] = df[header_value].apply(remap_char)



if __name__ == "__main__":

	script_path = os.path.dirname(os.path.realpath(__file__)) + '/'

	if CHAR_MAP_DICT is None:
		CHAR_MAP_DICT = generate_char_map()

	# Read excel sheet
	df = read_excel(excel_file, sheet_name)

	# Hash some columns
	anonymize_df(df, cols_to_hash)

	# Mask some columns
	mask_df(df, cols_to_mask)

	# Write csv output
	outfile = os.path.basename(excel_file) + '.' + sheet_name
	write_csv(df, outfile)

	write_excel(df, outfile)

	# Write out character mapping used to csv file
	df_char_map = pd.DataFrame(CHAR_MAP_DICT, index=[0])
	write_csv(df_char_map, outfile + '.char_map')

