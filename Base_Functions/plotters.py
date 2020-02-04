'''This file contains all necessary information for plotting relevant information.
It's used by the respective 'Auswerter'.py'''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 


sns.set(style='whitegrid',font_scale=1.2) ##General setting for plots

def boxplotter(daten,data_month,boxplottitle,printfolder):
	plt.figure(figsize=(15,20))
	ax=sns.boxplot(data=daten,x="val",y="cat")
	ax.set_ylabel('Kategorie',fontweight='bold')
	ax.set_xlabel('Einzelumsätze',fontweight='bold')
	ax.set_title(boxplottitle+f"\n({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold',pad=25)

	plt.savefig('./'+printfolder+'Boxplot_übersicht.jpg',papertype='a4',quality=80,bbox_inches='tight')

def violinplotter(daten,data_month,violintitle,printfolder):
	plt.figure(figsize=(17,20))
	ax=sns.violinplot(data=daten,x="val",y="cat",scale='width',palette='rainbow')
	ax=sns.swarmplot(data=daten,x="val",y="cat",color='black',size=6)
	ax.set_ylabel('Kategorie',fontweight='bold')
	ax.set_xlabel('Einzelumsätze',fontweight='bold')
	ax.set_title(violintitle+f"\n({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold',pad=25)

	plt.savefig('./'+printfolder+'Violinplot_übersicht.jpg',papertype='a4',quality=80,bbox_inches='tight')

def overviewplot(top3,top3_adj,data_month,plotinfo,printfolder):
	title_main,title_left,title_right,savename=plotinfo
	##Main plot configuration
	fig, ax =plt.subplots(figsize=(14,13),nrows=2,ncols=2)
	plt.suptitle(title_main+f"\n ({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold',y=1.03)

	## Definition first Subplot
	ax1 = sns.barplot(x="cat", y="val", data=top3,palette='rainbow',ax=ax[0,0]) ##Definition kind of plot & axis
	ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))##Get y_height

	ax1.set(xlabel='',xticklabels=[])  ##set labels and titles
	ax1.set_ylabel('Gesamtbeträge der Periode in €',fontweight='bold')
	ax1.set_title(title_left,pad=55,fontweight='bold')

	for item in ax1.get_xticklabels(): item.set_rotation(90) #alter plotting of x valuesticks
	for i, v in enumerate(top3["val"].iteritems()):        # add values on top of the plot
	    ax1.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)

	## Definition second Subplot
	ax2 = sns.barplot(x="cat", y="val_month", data=top3,palette='rainbow',ax=ax[1,0])
	ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
	ax2.set_xlabel("Kategorie",fontweight='bold')
	ax2.set_ylabel('Durschschnittliche Monatsbeträge in €',fontweight='bold')

	for item in ax2.get_xticklabels(): item.set_rotation(90)
	for i, v in enumerate(top3["val_month"].iteritems()):
	    ax2.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)

	## Definition third Subplot   
	ax3 = sns.barplot(x="cat", y="val", data=top3_adj,palette='rainbow',ax=ax[0,1])
	ax3.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
	ax3.set(xlabel='',ylabel="",xticklabels=[],yticklabels=[],ylim=ax1.get_ylim())
	ax3.set_title(title_right,pad=55,fontweight='bold')

	for i, v in enumerate(top3_adj["val"].iteritems()):        
	    ax3.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)
	 ## Definition fourth Subplot    
	ax4 = sns.barplot(x="cat", y="val_month", data=top3_adj,palette='rainbow',ax=ax[1,1])
	ax4.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
	ax4.set(ylabel='',yticklabels=[],ylim=ax2.get_ylim())
	ax4.set_xlabel("Kategorie",fontweight='bold')

	for item in ax4.get_xticklabels(): item.set_rotation(90)
	for i, v in enumerate(top3_adj["val_month"].iteritems()):        
	    ax4.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)   
	    
	 
	sns.despine()
	plt.subplots_adjust(left=0.15)
	fig.savefig('./'+printfolder+savename,papertype='a4',quality=70,bbox_inches='tight')

def costplotter(costs,data_month,plotinfo,printfolder):
	costtitle,savename=plotinfo
	##Main plot configuration
	fig, ax =plt.subplots(figsize=(15,15),nrows=2,sharex=True)
	plt.suptitle(costtitle+f"\n({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold',y=1.01)

	## Definition first Subplot
	ax1 = sns.barplot(x="cat", y="val", data=costs,palette='rainbow',ax=ax[0]) ##Definition kind of plot & axis
	ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))##Get y_height

	 ##set labels and titles
	ax1.set_xlabel("")
	ax1.set_ylabel('Gesamtbeträge der Periode in €',fontweight='bold')

	for item in ax1.get_xticklabels(): item.set_rotation(90) #alter plotting of x valuesticks
	for i, v in enumerate(costs["val"].iteritems()):        # add values on top of the plot
	    ax1.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)

	## Definition second Subplot
	ax2 = sns.barplot(x="cat", y="val_month", data=costs,palette='rainbow',ax=ax[1])
	ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

	ax2.set_xlabel("Kategorie",fontweight='bold')
	ax2.set_ylabel('Durschschnittliche Monatsbeträge in €',fontweight='bold')
	for item in ax2.get_xticklabels(): item.set_rotation(90)
	for i, v in enumerate(costs["val_month"].iteritems()):        
	    ax2.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)

	   
	sns.despine()
	plt.subplots_adjust(left=0.15)
	fig.savefig('./'+printfolder+savename,papertype='a4',quality=70,bbox_inches='tight')

def monthplotter(data_month,monthtitle,printfolder):
	plt.figure(figsize=(15,13))

	##Main title

	plt.suptitle("Huhn", fontsize=18, fontweight='bold',y=1.01)


	## Definition Plot
	ax1 = sns.barplot(x="month", y="val", data=data_month,palette='rainbow') ##Definition kind of plot & axis
	ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))##Get y_height

	 ##set labels and titles
	ax1.set_ylabel('Gesamtbeträge der Periode in €',fontweight='bold')
	ax1.set_xlabel('Monate',fontweight='bold')
	ax1.set_title(monthtitle+f"\n({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold',pad=15)
	for item in ax1.get_xticklabels(): item.set_rotation(90) #alter plotting of x valuesticks
	for i, v in enumerate(data_month["val"].iteritems()):        # add values on top of the plot
	    ax1.text(i ,v[1], "{:,.2f} €".format(v[1]), color='black', va ='bottom', rotation=45)
	sns.despine()
	plt.savefig('./'+printfolder+'Monatsauswertung.jpg',papertype='a4',quality=80,bbox_inches='tight')


def pieplotter(pie_data,data_month,plotinfo,printfolder):
	data_left,data_right=pie_data

	maintitle,left_title,right_title,explode_opt,savename=plotinfo

	pie_label_l=list(data_left['cat'])
	pie_size_l=list(data_left['ppt'])

	if explode_opt=='yes':

		exploder1=[1]*len(data_left)
		for i in range(0,len(data_left)):
			if data_left['ppt'][i]<10:
				exploder1[i]=0.2
			else:  
				exploder1[i]=0.02

		exploder2=[1]*len(data_right)
		for i in range(0,len(data_right)):
			if data_right['ppt'][i]<10:
				exploder2[i]=0.2
			else:  
				exploder2[i]=0.02
	else:
		exploder1=[0]*len(data_left)
		exploder2=[0]*len(data_right)



	pie_label_r=list(data_right['cat'])
	pie_size_r=list(data_right['ppt'])

	##Plot details
	fig, axes = plt.subplots(1, 2, figsize=(15, 10))
	plt.suptitle(maintitle+f"\n({data_month.loc[len(data_month)-1][0]} bis {data_month.loc[0][0]})", fontsize=18, fontweight='bold')
	##Left plot
	ax2=axes[0].pie(pie_size_l, labels=pie_label_l, explode=exploder1, autopct='%1.1f%%',shadow=True, startangle=90)# Equal aspect ratio ensures that pie is drawn as a circle
	axes[0].set_title(left_title,pad=30, fontweight='bold')

	##Right plot
	ax2=axes[1].pie(pie_size_r, labels=pie_label_r, explode=exploder2, autopct='%1.1f%%',shadow=True, startangle=90)# Equal aspect ratio ensures that pie is drawn as a circle
	axes[1].set_title(right_title,pad=30, fontweight='bold')

	plt.savefig('./'+printfolder+savename,papertype='a4',quality=80,bbox_inches='tight')