import os
import csv
from git import Repo
import datetime as dt


# Root directory for the COVID-19 Local repository
root=os.getcwd()


#Defining a case class
class Cases:
	def __init__(self,file_path):
		self.fields=[]#available fields
		self.rows=[]#raw data per country
		self.dict={}#covid 19 numbers
		self.pop={}#country population
		self.loc={}#country coordinates
		with open(file_path) as csv_file:
			reader=csv.reader(csv_file, delimiter=',', lineterminator='\n')
			flag=False
			for row in reader:
				if not flag:
					self.fields=row
					flag=True
				else:
					self.rows.append(row)
					key=row[1]
					sub_dict={}
					for i in range(4,len(row)):
						if key in self.dict.keys():
							if row[0] != '':
								sub_dict=self.dict[key]
								sub_dict[self.fields[i]]+=int(row[i])
							else:
								sub_dict[self.fields[i]]=int(row[i])
						else:
							sub_dict[self.fields[i]]=int(row[i])

					self.dict[key]=sub_dict

					sub_loc_list=[]
					for i in range(2,4):
						sub_loc_list.append(float(row[i]))
					self.loc[key]=sub_loc_list
							


	def obj_to_str(self,date_obj):#for 2020 only
		d=date_obj.strftime("%d")
		if d[0]=="0":
			d=d[1]
		m=date_obj.strftime("%m")
		if m[0]=="0":
			m=m[1]
		date=m+"/"+d+"/20"
		return date

	def str_to_obj(self,date):
		i1=date.index("/")
		i2=date.index("/",i1+1)
		month=int(date[:i1])
		day=int(date[i1+1:i2])
		year=int("2020")
		date_obj=dt.date(year,month,day)
		return date_obj

	def __increment_date(self,date,num=1):
		date_obj=self.str_to_obj(date)
		date_obj+=dt.timedelta(days=num)
		date=self.obj_to_str(date_obj)
		return date

	def cases(self, country, startDate, endDate=None):
		if endDate==None:
			return self.dict[country][startDate]
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.dict[country][startDate])
				startDate=self.__increment_date(startDate)
			return retlist

	def new_cases(self, country, startDate, endDate=None):
		if endDate==None:
			date_obj=self.str_to_obj(startDate)
			prev_date_obj=date_obj-dt.timedelta(days=1)
			prev_date=self.obj_to_str(prev_date_obj)
			if prev_date in self.fields:
				return self.dict[country][startDate]-self.dict[country][prev_date]
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.new_cases(country,startDate))
				startDate=self.__increment_date(startDate)
			return retlist

	def rate(self, country, startDate, endDate=None):
		if endDate==None:
			c=self.new_cases(country,startDate)
			n=self.dict[country][startDate]
			if c!= None and n!=0:
				# n=self.dict[country][startDate]
				return (c/n)*100
			else:
				return 0
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.rate(country,startDate))
				startDate=self.__increment_date(startDate)
			return retlist

	def first_case(self,country):
		for x in self.dict[country].keys():
			if self.dict[country][x]!=0:
				return x

	def latest_date(self):
		return self.fields[-1]

	def global_cases(self, startDate, endDate=None):
		if endDate==None:
			sum=0
			for x in self.dict.keys():
				sum+=self.dict[x][startDate]
			return sum
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.global_cases(startDate))
				startDate=self.__increment_date(startDate)
			return retlist

	def global_rate(self, startDate, endDate=None):
		if endDate==None:
			sum_cases=0
			sum_new_cases=0
			for x in self.dict.keys():
				sum_cases+=self.dict[x][startDate]
				sum_new_cases+=self.new_cases(x,startDate)
			rate=(sum_new_cases/sum_cases)*100
			return rate
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.global_rate(startDate))
				startDate=self.__increment_date(startDate)
			return retlist
	def global_new_cases(self, startDate, endDate=None):
		if endDate==None:
			sum=0
			for x in self.dict.keys():
				sum+=self.new_cases(x,startDate)
			return sum
		else:
			retlist=[]
			endDate=self.__increment_date(endDate)
			while startDate!=endDate:
				retlist.append(self.global_new_cases(startDate))
				startDate=self.__increment_date(startDate)
			return retlist

# Clone Repo if not already cloned, otherwise pull new data



# if os.path.isdir(root+"/COVID-19"):
root="COVID-19"
# repo=Repo(root)
# git=repo.git
# try:
# 	git.pull()
# except:
# 	print("Network Error! Repository may be outdated!")
# else:
# 	root+="/COVID-19"
	# os.system("git clone https://github.com/CSSEGISandData/COVID-19.git")



#Creating objects
Confirmed=Cases(root+"/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
Deaths=Cases(root+"/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
Recovered=Cases(root+"/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")


#Combinational functions

def closed_death_rate(country, startDate, endDate=None):
    if endDate==None:
        rate=-1
        dead=Deaths.cases(country,startDate)
        recov=Recovered.cases(country,startDate)
        if dead!=0 and recov!=0:
            rate=(dead/(dead+recov))*100
        return rate
    else:
        retlist=[]
        dead=Deaths.cases(country,startDate,endDate)
        recov=Recovered.cases(country,startDate,endDate)
        for i in range(len(dead)):
            if dead[i]!=0 and recov[i]!=0:
                retlist.append((dead[i]/(dead[i]+recov[i]))*100)
            else:
                retlist.append(-1)
        return retlist

def death_rate(country, startDate, endDate=None):
    if endDate==None:
        rate=-1
        dead=Deaths.cases(country,startDate)
        conf=Confirmed.cases(country,startDate)
        if conf!=0:
            rate=(dead/conf)*100
        return rate
    else:
        retlist=[]
        dead=Deaths.cases(country,startDate,endDate)
        conf=Confirmed.cases(country,startDate,endDate)
        for i in range(len(dead)):
            if conf[i]!=0:
                retlist.append((dead[i]/conf[i])*100)
            else:
                retlist.append(-1)
        return retlist
def recovered_rate(country, startDate, endDate=None):
	if endDate==None:
		rate=death_rate(country, startDate)
		return 100-rate
	else:
		rate=death_rate(country, startDate, endDate)
		retlist=[]
		for x in rate:
			retlist.append(100-x)
		return retlist
def closed_recovered_rate(country, startDate, endDate=None):
	if endDate==None:
		rate=closed_death_rate(country, startDate)
		return 100-rate
	else:
		rate=closed_death_rate(country, startDate, endDate)
		retlist=[]
		for x in rate:
			retlist.append(100-x)
		return retlist


def global_death_rate(startDate, endDate=None):
    if endDate==None:
        rate=-1
        dead=Deaths.global_cases(startDate)
        conf=Confirmed.global_cases(startDate)
        if conf!=0:
            rate=(dead/conf)*100
        return rate
    else:
        retlist=[]
        dead=Deaths.global_cases(startDate,endDate)
        conf=Confirmed.global_cases(startDate,endDate)
        for i in range(len(dead)):
            if conf[i]!=0:
                retlist.append((dead[i]/conf[i])*100)
            else:
                retlist.append(-1)
        return retlist


def global_closed_death_rate(startDate, endDate=None):
    if endDate==None:
        rate=-1
        dead=Deaths.global_cases(startDate)
        recov=Recovered.global_cases(startDate)
        if dead!=0 and recov!=0:
            rate=(dead/(dead+recov))*100
        return rate
    else:
        retlist=[]
        dead=Deaths.global_cases(startDate,endDate)
        recov=Recovered.global_cases(startDate,endDate)
        for i in range(len(dead)):
            if dead[i]!=0 and recov[i]!=0:
                retlist.append((dead[i]/(dead[i]+recov[i]))*100)
            else:
                retlist.append(-1)
        return retlist

def global_recovered_rate(startDate, endDate=None):
	if endDate==None:
		rate=global_death_rate(startDate)
		return 100-rate
	else:
		rate=global_death_rate(startDate, endDate)
		retlist=[]
		for x in rate:
			retlist.append(100-x)
		return retlist




# print(Deaths.loc["Australia"])