
'''This file holds all relevant functions necessary for starting the data analysis. Raw data is imported,
and processed so that it can be used for plotting. If desired credit data is also integrated. 
Currently it is only working for comdirect bank data. Further work towards integrating other banks will be done. Excel file is exported at the end exported.'''


from Base_Functions import classifier

print('Import der benötigten Module erfolgreich!')
import numpy as np
import pandas as pd
import datetime
import locale
import re


locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
mydateparser = lambda x: pd.datetime.strptime(x, "%d.%m.%Y")


def read_comdirect_account(name1,name2,creditcard):
	data_account=pd.read_csv(name1,sep=";",encoding="iso8859_15",skiprows=4,index_col=5,thousands='.',decimal=',',skipfooter=2,engine='python',parse_dates=[0,1],date_parser=mydateparser,).reset_index(drop=True)
	data_account.columns=["time1","time2","act","text","val"]

	if creditcard=='j':
		data_credit=pd.read_csv(name2,sep=";",encoding="iso8859_15",skiprows=4,index_col=6,thousands='.',decimal=',',skipfooter=2,engine='python',parse_dates=[0,1],date_parser=mydateparser,).reset_index(drop=True)
		data_credit.columns=["time1","time2","act","ref","text","val"]
		data_credit.drop("ref",axis=1,inplace=True)
		raw_data=pd.concat([data_account,data_credit],ignore_index=True)
	else:
		raw_data=data_account

	return raw_data

def categorize_data(dicttype,data):
	data["lowtext"]=data['text'].apply(lambda text: ''.join(text.lower().split()))	## create auxiliary column with scanable text
	data["cat"]=data['lowtext'].apply(lambda text: classifier.categorizer(dicttype,text))	## do categorization
	data.drop("lowtext",axis=1,inplace=True)										## get rid of auxiliary column
	
	return data

def makecatdata(data2,data_month):
	data_cat=data2.groupby('cat')['val'].sum().reset_index()
	summe_rest=abs(data_cat[(data_cat['cat'].isin(['Aktien-\ngeschäfte','Lohn','ETFS/Wert-\npapiersparen','Bucheinkünfte','Einzahlungen','Miete'])==False)&(data_cat['val']<0)]['val'].sum())
	hilfs=pd.DataFrame([['Gesamtsumme', sum(data2['val'])]],columns=list(data_cat.columns))
	data_cat['val']=data_cat['val'].abs()
	data_cat=data_cat.sort_values(['val'],ascending=False).reset_index(drop=True)
	data_cat=data_cat.append(hilfs,ignore_index=True)
	data_cat['val_month']=data_cat['val']/data_month['month'].nunique()
	data_transfer=(data_cat,summe_rest)

	return data_transfer

def read_dkb_credit(name1,name2,writer_excel,holiday):

	dicttype='credit'
	dkb_credit=pd.read_csv(name1,sep=";",encoding="iso8859_15",skiprows=6,skipfooter=1,index_col=6,thousands='.',decimal=',',engine='python',parse_dates=[1,2],date_parser=mydateparser).reset_index(drop=True)
	dkb_credit.drop(dkb_credit.columns[0],axis=1,inplace=True)
	dkb_credit.insert(2,'act',pd.Series())
	dkb_credit.columns=["time2","time1","act","text","val","primary"]
	dkb_credit=dkb_credit.reindex(columns=dkb_credit.columns[[1,0,2,3,4,5]])
	dkb_credit.to_excel(writer_excel,sheet_name='Rohdaten KK & Urlaub',index=False,header=["Buchungstag","Wertstellung (Valuta)","Vorgang","Buchungstext","Umsatz in EUR","Ursprünglicher Betrag"])
	dkb_credit['month']=dkb_credit['time1'].apply(lambda dates: dates.strftime('%b/%Y'))
	dkb_credit["lowtext"]=dkb_credit['text'].apply(lambda text: ''.join(text.lower().split()))	## create auxiliary column with scanable text
	dkb_credit["cat"]=dkb_credit['lowtext'].apply(lambda text: classifier.categorizer(dicttype,text))	## do categorization
	dkb_credit.drop("lowtext",axis=1,inplace=True)
	
	##Integrate Holiday data if selected
	if holiday=='j':
		data_hol=pd.read_excel(name2,names=["time1","time2","act","text","val","month","cat"])
		data_hol.insert(5,'primary',pd.Series())
		data_hol.loc[data_hol['cat'].str.contains('Bargeld'),'cat']='Einzahlung\ncomdirect'
		data_hol.loc[data_hol['cat'].str.contains('Einzahlung\ncomdirect'),'val']=data_hol['val'].abs()
		basis_data_dkb=pd.concat([dkb_credit,data_hol],ignore_index=True)
		basis_data_dkb.drop(basis_data_dkb.index[(basis_data_dkb['cat']=='Einzahlung')&(basis_data_dkb['val']>90)],inplace=True)
		basis_data_dkb.reset_index(drop=True)
		basis_data_dkb.loc[basis_data_dkb['cat']=='Einzahlung','cat']='Andere\nEinzahlung'
	else:
		basis_data_dkb=dkb_credit

	return basis_data_dkb

def makecatdkbdata(data3,data_month1):
	data_cat_dkb=data3.groupby('cat')['val'].sum().reset_index()
	data_cat_dkb=data_cat_dkb.sort_values(['val'],ascending=False).reset_index(drop=True)
	data_cat_dkb['val']=data_cat_dkb['val'].abs()
	cost_dkb_kk=data_cat_dkb.loc[2:].sort_values(['val'],ascending=False)
	data_cat_dkb.drop(data_cat_dkb.index[2:],inplace=True)
	data_cat_dkb=data_cat_dkb.append(cost_dkb_kk,ignore_index=True)
	data_cat_dkb['val_month']=data_cat_dkb['val']/data_month1['month'].nunique()
	
	return data_cat_dkb

def processdkbgiro(dicttype,dkb_account):
	dkb_account['text'] = dkb_account[dkb_account.columns[3:6]].apply(lambda x: ' '.join(x.dropna()),axis=1)
	dkb_account.drop(dkb_account.columns[[3,4,5,6]],axis=1,inplace=True)
	dkb_account=dkb_account.reindex(columns=dkb_account.columns[[0,1,2,4,3]])
	dkb_account['month']=dkb_account['Buchungstag'].apply(lambda dates: dates.strftime('%b/%Y'))
	dkb_account.columns=["time1","time2","act","text","val",'month']
	basis_dkb_account=categorize_data(dicttype,dkb_account)

	return basis_dkb_account