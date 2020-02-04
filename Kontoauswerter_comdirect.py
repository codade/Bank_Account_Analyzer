
'''This is the main file getting all actions accomplished. Little interaction with user is needed and given here.'''


import numpy as np
import pandas as pd
from Base_Functions import data_processer
from Base_Functions import plotters


folder_rawdata=input('Bitte geben Sie den genauen Dateipfad des Ordners an, in dem sich die Rohdaten befinden!')
writer_excel = pd.ExcelWriter('./Ergebnisse/Ergebnisse Comdirect/Auswertungstabelle.xlsx', engine='xlsxwriter')


##Import and process comdirect data

filename1=folder_rawdata+input('Bitte geben Sie den genauen Dateinamen der Girokontodaten inklusive Dateiendung ein!')

while True:
	try:
	    creditcard=input('Sollen auch Kreditkartendaten eingelesen werden?')[0].lower()
	except:
	    print("Sie können nur Ja oder Nein eingeben!")
	else:
	    if not (creditcard=='j' or creditcard=='n'):
	        print("Sie können nur Ja oder Nein eingeben")
	        continue
	    else:
	        break
if creditcard=='j':
	filename2=folder_rawdata+input('Bitte geben Sie den genauen Dateinnamen der Kreditkartendaten inklusive Dateiendung ein!')
else:
	filename2=folder_rawdata+'nichteinlesen'

##Include Data, get raw data
raw_data=data_processer.read_comdirect_account(filename1,filename2,creditcard)

print('Die Rohdaten werden jetzt in eine Excel-Datei ausgegeben')
raw_data.to_excel(writer_excel,sheet_name='Rohdaten',index=False,header=["Buchungstag","Wertstellung (Valuta)","Vorgang","Buchungstext","Umsatz in EUR"])

raw_data['month']=raw_data['time1'].apply(lambda dates: dates.strftime('%b/%Y'))

## process data to use it
dicttype='giro'
basis_data=data_processer.categorize_data(dicttype,raw_data)
data_hol=basis_data.loc[basis_data['cat'].str.contains('Urlaub')]   ## create extra dataframe for holidays to be exported for separate analysis
print('Die kategorisierten Daten werden jetzt in eine Excel-Datei ausgegeben')
data_hol=data_hol.append(basis_data.loc[basis_data['cat']=='DKB-Bargeld'])
basis_data.to_excel(writer_excel,sheet_name='Aufbereitete Daten',index=False,header=["Buchungstag","Wertstellung (Valuta)","Vorgang","Buchungstext","Beträge in EUR","Monat","Kategorie"])
data_hol.to_excel('./Ergebnisse/Ergebnisse Comdirect/Urlaubsausgaben & DKB Bargeld comdirect.xlsx',index=False,header=["Buchungstag","Wertstellung (Valuta)","Vorgang","Buchungstext","Beträge in EUR","Monat","Kategorie"])

##do adjustments to data for better plotting
basis_data.loc[basis_data['cat'].str.contains('Urlaub'),'cat']='Urlaub' ##put holidays together

##Monthly data
data_month=basis_data.groupby('month',sort=False)['val'].sum().reset_index() ##get monthly overview
data_month=data_month.sort_values(['val'],ascending=False) ##sort monthly data



## Get Data based on categories
data_cat,summe_rest=data_processer.makecatdata(basis_data,data_month)
data_cat.to_excel(writer_excel,sheet_name='Übersicht nach Kategorie.xlsx',index=False,header=["Kategorie","Beträge in EUR","Beträge pro Monat"])


writer_excel.save() ##Save Excel file

'''Plotting part'''
printfolder='Ergebnisse/Ergebnisse Comdirect/'
print('Die Plots werden jetzt erstellt und gespeichert!')

#Plot month data
monthtitle='Monatsaufstellung Umsätze Comdirect'
plotters.monthplotter(data_month,monthtitle,printfolder)

##plot the total cost overview 
boxplottitle='Boxplot sämtlicher Umsätze nach Kategorie'
plotters.boxplotter(basis_data,data_month,boxplottitle,printfolder) #Boxplot
violintitle='Detaillierte Übersicht Verteilung Umsätze nach Kategorie'
plotters.violinplotter(basis_data,data_month,violintitle,printfolder) #Violinplot


##Sort for Top3 and Income
top3=data_cat.iloc[:4].reset_index(drop=True)

##Adjusted TOP3 without invest
top3_adj=data_cat[data_cat['cat'].isin(['Gesamtsumme'])]
lohn_inv=abs(data_cat[data_cat['cat'].isin(['Lohn','Bucheinkünfte'])]['val'].sum()-data_cat[data_cat['cat'].isin(['Aktien-\ngeschäfte','ETFS/Wert-\npapiersparen'])]['val'].sum())
top3_adj=top3_adj.append(pd.DataFrame([['Restliche\nKosten', summe_rest,summe_rest/data_month['month'].nunique()]],columns=list(top3.columns)),ignore_index=True)
top3_adj=top3_adj.append(pd.DataFrame([['Einkünfte\nohne Invest', lohn_inv,lohn_inv/data_month['month'].nunique()]],columns=list(top3.columns)),ignore_index=True)
top3_adj=top3_adj.sort_values(['val'],ascending=False).reset_index(drop=True)

##Sum up costs
cost_notinv=data_cat[data_cat['cat'].isin(['Aktien-\ngeschäfte','Lohn','ETFS / Wert-\npapiersparen','Gesamtsumme','Bucheinkünfte'])==False].reset_index(drop=True)



##plot single plots
plotinfo_overview=('Überblicksübersicht Kosten und Einkünfte','Lohn und TOP3-Kostenblöcke','Einkünfte ohne Invest & Restliche Kosten','TOP3 & Einkünfte ohne Invest.jpg')
plotters.overviewplot(top3,top3_adj,data_month,plotinfo_overview,printfolder)
plotinfo_costs=('Detaillierte Übersicht Kostenkategorien ohne Invest','Einzelkostenübersicht.jpg')
plotters.costplotter(cost_notinv,data_month,plotinfo_costs,printfolder)

## Prepare Pie charts. Group together labels with less than 2% share

##Adjust total cost with holidays grouped together
cost_total=data_cat[data_cat['cat'].isin(['Lohn','Gesamtsumme','Bucheinkünfte'])==False].reset_index(drop=True)

##First pie costs without holidays
cost_intermediate=cost_notinv.assign(ppt=(cost_notinv['val']*100/cost_notinv['val'].sum()).round(2))
cost_intermediate.drop('val_month',axis=1,inplace=True)
cost_pie_nothol=cost_intermediate.loc[cost_intermediate['ppt']>=2.0]
cost_pie_nothol=cost_pie_nothol.append(pd.DataFrame([['Restliche mit <2%',sum(cost_intermediate.loc[cost_intermediate['ppt']<2.0]['val']),sum(cost_intermediate.loc[cost_intermediate['ppt']<2.0]['ppt'])]],columns=list(cost_intermediate.columns)),ignore_index=True)

##Second pie costs with holidays together
cost_intermediate2=cost_total.assign(ppt=(cost_total['val']*100/cost_total['val'].sum()).round(2))
cost_intermediate2.drop('val_month',axis=1,inplace=True)
cost_pie_total_adj=cost_intermediate2.loc[cost_intermediate2['ppt']>=2.0]
cost_pie_total_adj=cost_pie_total_adj.append(pd.DataFrame([['Restliche mit <2%',sum(cost_intermediate2.loc[cost_intermediate2['ppt']<2.0]['val']),sum(cost_intermediate2.loc[cost_intermediate2['ppt']<2.0]['ppt'])]],columns=list(cost_intermediate2.columns)),ignore_index=True)

##Create Plots
data_pie=(cost_pie_total_adj,cost_pie_nothol)

plotinfo_pieplot=('Tortendiagramm Kostenkategorien >2% Anteil','Anteilsübersicht mit Invest','Anteilsübersicht ohne Invest','yes','Kostenanteile Tortendiagramm.jpg')
plotters.pieplotter(data_pie,data_month,plotinfo_pieplot,printfolder)




print('Alles fertig! Das Programm kann jetzt geschlossen werden.')