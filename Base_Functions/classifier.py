
'''This file contains the list (dictionary) necessary for categorizing all booking entries. This dictionary is work in progress.
Feel free to adapt it to your needs '''

import numpy as np
import pandas as pd
import datetime
import re

dict_giro=pd.read_excel('Zuordnungstabelle.xlsx',sheet_name='Girokonto',index_col=0)['Kategorie'].to_dict()
dict_dkb=pd.read_excel('Zuordnungstabelle.xlsx',sheet_name='DKB-Kredit',index_col=0)['Kategorie'].to_dict()



def categorizer(dicttype,string):
	if dicttype=='credit':
		dictuse=dict_dkb
	else:
		dictuse=dict_giro

	for key in dictuse.keys():
		if re.findall(key,string):
			return dictuse[key]
	else:
		return 'Sonstiges'