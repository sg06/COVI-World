import warnings
warnings.filterwarnings("ignore")

# List made from the file given along with assignment, having name of countries and continents
arr = ['Europe:', '--------', 'France', 'UK', 'Russia', 'Italy', 'Germany', 'Spain', 'Poland', 'Netherlands', 'Ukraine', 'Belgium', '', 'North America:', '---------', 'USA', 'Mexico', 'Canada', 'Cuba', 'Costa Rica', 'Panama', '', 'Asia', '---------', 'India', 'Turkey', 'Iran', 'Indonesia', 'Philippines', 'Japan', 'Israel', 'Malaysia', 'Thailand', 'Vietnam', 'Iraq', 'Bangladesh', 'Pakistan', '', 'South America', '---------', 'Brazil', 'Argentina', 'Colombia', 'Peru', 'Chile', 'Bolivia', 'Uruguay', 'Paraguay', 'Venezuela', '', 'Africa', '--------', 'South Africa', 'Morocco', 'Tunisia', 'Ethiopia', 'Libya', 'Egypt', 'Kenya', 'Zambia', 'Algeria', 'Botswana', 'Nigeria', 'Zimbabwe', '', 'Oceania', '--------', 'Australia', 'Fiji', 'Papua New Guinea', 'New Caledonia', 'New Zealand']

# List of Continents
continent = []
# List of Countries
country = []

flag = 1
for x in arr:
	if(flag == 1):
		if(x[-1] == ':'):
			continent.append(x[:-1])
		else:
			continent.append(x)
	else:
		if(x!='' and x[0]!='-'):
			country.append(x.lower())
	if(x == ''):
		flag = 1
	else:
		flag = 0

# List of country_name as per used in the URL
country_modified = []
for i in range(len(country)):
	country_modified.append(country[i].replace(" ", "-"))

import urllib.request
from urllib.request import urlopen
from tqdm import tqdm

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'

print("Please Wait, Downloading is under process!!")

# Files are downloaded
for i in range(len(country)+1):
	temp = "Corona_"
	html = ".html"
	headers={'User-Agent':user_agent,} 
	if(i==0):
		main_url = 'https://www.worldometers.info/coronavirus/'
		url = main_url
		file_name = temp+"world"+html
	elif(country_modified[i-1] == 'usa'):
		main_url = 'https://www.worldometers.info/coronavirus/country/'
		url = main_url+'us'+"/"
		file_name = temp+country_modified[i-1]+html
	elif(country_modified[i-1] == 'vietnam'):
		main_url = 'https://www.worldometers.info/coronavirus/country/'
		url = main_url+'viet-nam'+"/"
		file_name = temp+country_modified[i-1]+html
	else:
		main_url = 'https://www.worldometers.info/coronavirus/country/'
		url = main_url+country_modified[i-1]+"/"
		file_name = temp+country_modified[i-1]+html

	request=urllib.request.Request(url,None,headers)
	response = urllib.request.urlopen(request)
	data = response.read()

	file = open(file_name,'wb')
	file.write(data)
	file.close()

print("All the Files are Downloaded Successfully!!")

del arr
del continent
del country
del country_modified

# List made from the file given along with assignment, having name of countries and continents
arr = ['Europe:', '--------', 'France', 'UK', 'Russia', 'Italy', 'Germany', 'Spain', 'Poland', 'Netherlands', 'Ukraine', 'Belgium', '', 'North America:', '---------', 'USA', 'Mexico', 'Canada', 'Cuba', 'Costa Rica', 'Panama', '', 'Asia', '---------', 'India', 'Turkey', 'Iran', 'Indonesia', 'Philippines', 'Japan', 'Israel', 'Malaysia', 'Thailand', 'Vietnam', 'Iraq', 'Bangladesh', 'Pakistan', '', 'South America', '---------', 'Brazil', 'Argentina', 'Colombia', 'Peru', 'Chile', 'Bolivia', 'Uruguay', 'Paraguay', 'Venezuela', '', 'Africa', '--------', 'South Africa', 'Morocco', 'Tunisia', 'Ethiopia', 'Libya', 'Egypt', 'Kenya', 'Zambia', 'Algeria', 'Botswana', 'Nigeria', 'Zimbabwe', '', 'Oceania', '--------', 'Australia', 'Fiji', 'Papua New Guinea', 'New Caledonia', 'New Zealand']

# List of Continents
continent = []
# List of Countries
country = []

flag = 1
for x in arr:
	if(flag == 1):
		if(x[-1] == ':'):
				continent.append(x[:-1])
		else:
				continent.append(x)
	else:
		if(x!='' and x[0]!='-'):
				country.append(x)
	if(x == ''):
		flag = 1
	else:
		flag = 0

# List of country_name as per used in the URL
country_modified = []
for i in range(len(country)):
	if(country[i] == 'USA'):
		country_modified.append('us')
	elif(country[i] == 'Vietnam'):
		country_modified.append('viet-nam')
	else:
		country_modified.append(country[i].replace(" ", "-").lower())

# Data is extracted from the world file, from the yesterday section
file = open('Corona_world.html', 'r')
flag = 0
text = ""
for line in file:
    if(line == """<table id="main_table_countries_yesterday" class="table table-bordered table-hover main_table_countries" style="width:100%;margin-top: 0px !important;display:none;">\n"""):
        flag=1
    elif(flag==1 and line == "</table>\n"):
        break
    if(flag == 1):
        text = text + line
file.close()

# Details of world extracted from yesterday's data 
world_data = ""
world_flag = 0
for line in text.split("\n"):
    if(line == '<tr class="total_row_world">'):
        world_flag = 1
    if(world_flag == 1):
        world_data = world_data + "\n" + line
    if(world_flag == 1 and line == '<td style="display:none" data-continent="all">All</td>'):
        break
world_data = world_data[1:]

world_arr = []

t_ignore = " \t"

def t_error(t):
	t.lexer.skip(1)

def p_error(t):
	pass

#################################################################################
#################################################################################

nearest_country_recovery = ''
nearest_country_recovery_percent = 0
change_nearest_country_percent_recovery = 1000000000000

# Parser to extract data of New Recovered Case from the countries files
def new_recovered_case_parser(country_new_recovered_case):
    
    new_recovered_case_arr = []
    
    def t_LRECASEDATE(t):
        r'\n\s\s\s\s\s\s\s\s\s\s\s\scategories:\s\['
        return t

    def t_RRECASEDATE(t):
        r'\]\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_LRECASEDATA(t):
        r'5\,\n\s\s\s\s\s\s\s\s\s\s\s\s\n\s\s\s\s\s\s\s\s\s\s\s\sdata:\s\['
        return t

    def t_RECASENAME(t):
        r"[A-Za-z0-9.\-\+\",\s]+"
        return t

    def p_start6(t):
        '''start6 : recasedates
                | recasedata
                '''

    def p_recasedates(t):
        'recasedates : LRECASEDATE RECASENAME'
        t[0] = t[2]
        new_recovered_case_arr.append(t[0])

    def p_recasedata(t):
        'recasedata : LRECASEDATA RECASENAME RRECASEDATE'
        t[0] = t[2]
        new_recovered_case_arr.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LRECASEDATE',
        'RRECASEDATE',
        'LRECASEDATA',
        'RECASENAME',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_new_recovered_case))
    
    
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_new_recovered_case)

    return new_recovered_case_arr

#################################################################################
#################################################################################

nearest_country_new_death_case = ''
nearest_country_new_death_case_percent = 0
change_nearest_country_percent_new_death_case = 1000000000000

# Parser to extract data of New Death Case from the countries files
def new_death_case_parser(country_new_death_case):

    new_death_case_arr = []

    def t_LNDCASEDATE(t):
        r'\n\s\s\s\s\s\s\s\s\s\s\s\scategories:\s\['
        return t

    def t_RNDCASEDATE(t):
        r'\]\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_LNEWDCASEDATA(t):
        r'false,\n\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\sdata:\s\['
        return t

    def t_RNEWDCASEDATA(t):
        r'\]\s\s\s\s\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_NEWDCASENAME(t):
        r"[A-Za-z0-9.\-\",\s]+"
        return t

    def p_start5(t):
        '''start5 : newdcasedates
                | newdcasedata
                '''

    def p_newdcasedates(t):
        'newdcasedates : LNDCASEDATE NEWDCASENAME RNDCASEDATE'
        t[0] = t[2]
        new_death_case_arr.append(t[0])

    def p_newdcasedata(t):
        'newdcasedata : LNEWDCASEDATA NEWDCASENAME RNEWDCASEDATA'
        t[0] = t[2]
        new_death_case_arr.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LNDCASEDATE',
        'RNDCASEDATE',
        'LNEWDCASEDATA',
        'RNEWDCASEDATA',
        'NEWDCASENAME',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_new_death_case))
    
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_new_death_case)

    return new_death_case_arr


##################################################################################
##################################################################################

nearest_country_new_case = ''
nearest_country_new_case_percent = 0
change_nearest_country_percent_new_case = 1000000000000

# Parser to extract data of New Case from the countries files
def new_case_parser(country_new_case):
    
    newcase_arr = []
    
    def t_LNCASEDATE(t):
        r'\n\s\s\s\s\s\s\s\s\s\s\s\scategories:\s\['
        return t

    def t_RNCASEDATE(t):
        r'\]\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_LNEWCASEDATA(t):
        r'false,\n\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\sdata:\s\['
        return t

    def t_RNEWCASEDATA(t):
        r'\]\s\s\s\s\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_NEWCASENAME(t):
        r"[A-Za-z0-9.\-\",\s]+"
        return t

    def p_start4(t):
        '''start4 : newcasedates
                | newcasedata
                '''

    def p_newcasedates(t):
        'newcasedates : LNCASEDATE NEWCASENAME RNCASEDATE'
        t[0] = t[2]
        newcase_arr.append(t[0])

    def p_newcasedata(t):
        'newcasedata : LNEWCASEDATA NEWCASENAME RNEWCASEDATA'
        t[0] = t[2]
        newcase_arr.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LNCASEDATE',
        'RNCASEDATE',
        'LNEWCASEDATA',
        'RNEWCASEDATA',
        'NEWCASENAME',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_new_case))
        
        
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_new_case)

    return newcase_arr

##################################################################################
##################################################################################


nearest_country_active = ''
nearest_country_active_percent = 0
change_nearest_country_percent_active = 1000000000000

import warnings
warnings.filterwarnings("ignore")

# Parser to extract data of New Active Case from the countries files
def active_case_parser(country_active_case):

    activecase_arr = []

    def t_LACASEDATE(t):
        r'\n\s\s\s\s\s\s\s\s\s\s\s\scategories:\s\['
        return t

    def t_RACASEDATE(t):
        r'\]\s\s\s\s\s\s\s\s\}\,'
        return t

    def t_LACASEDATA(t):
        r'5,\n\s\s\s\s\s\s\s\s\s\s\s\sdata:\s\['
        return t

    def t_RACASEDATA(t):
        r'\]\s\s\s\s\s\s\s\s\}\n'
        return t

    def t_ACASENAME(t):
        r"[A-Za-z0-9.\-\",\s]+"
        return t

    def p_start3(t):
        '''start3 : acasedates
                | acasedata
                '''

    def p_acasedates(t):
        'acasedates : LACASEDATE ACASENAME RACASEDATE'
        t[0] = t[2]
        activecase_arr.append(t[0])

    def p_acasedata(t):
        'acasedata : LACASEDATA ACASENAME RACASEDATA'
        t[0] = t[2]
        activecase_arr.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LACASEDATE',
        'RACASEDATE',
        'LACASEDATA',
        'RACASEDATA',
        'ACASENAME',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_active_case))
    
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_active_case)

    return activecase_arr

#####################################################################################
#####################################################################################

# Parser to extract data of Country from the Yesterday's data
def country_parser(country_data_update):
	
	ans = []
	
	def t_LCOUNTRY(t):
		r'<td\sstyle="font-weight:\sbold;\sfont-size:15px;\stext-align:left;"><a\sclass="mt_a"\shref="country/(.|n)*?>'
		return t

	def t_RCOUNTRY(t):
		r'\<\/a\></td>\n'
		return t

	def t_LPOP(t):
		r'<td\sstyle=\"font\-weight:\sbold;\stext\-align:right\"><a\shref=\"/world\-population\/[a-z\-]*\-population\/\">'
		return t

	def t_LTCASE(t):
		r'<td\sstyle="font\-weight\:\sbold;\stext\-align\:right">'
		return t

	def t_RTCASE(t):
		r'\<\/td\>'
		return t

	def t_LNCASE(t):
		r'<td\sstyle="font-weight:\sbold;\stext-align:right;background-color:(.|n)*?>'
		return t

	def t_LTDEATH(t):
		r'<td\sstyle="font-weight:\sbold;\stext-align:right;">'
		return t

	def t_LACASE(t):
		r'<td\sstyle="text-align:right;font-weight:bold;">'
		return t

	def t_LNDEATH(t):
		r'<td\sstyle="font-weight:\sbold;\s\n\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\stext-align:right[a-zA-Z0-9\s\-\:\;]+">'
		return t

	def t_NAME(t):
		r"[A-Za-z0-9':.\+\-\_()\s,]+"
		return t

	def p_start(t):
		'''start : country
				| pop
				| tcase
				| ncase
				| acase
				| tdeath
				| ndeath
				| cwaste
				'''

	def p_country(t):
		'country : LCOUNTRY NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_pop(t):
		'pop : LPOP NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_tcase(t):
		'tcase : LTCASE NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_ncase(t):
		'ncase : LNCASE NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_acase(t):
		'acase : LACASE NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_tdeath(t):
		'tdeath : LTDEATH NAME'
		t[0] = t[2]
		ans.append(t[0])

	def p_ndeath(t):
		'ndeath : LNDEATH NAME'
		t[0] = t[2]
		ans.append(t[0])
	
	def p_cwaste(t):
		'cwaste : RCOUNTRY LCOUNTRY LCOUNTRY RTCASE'
		t[0] = t[2]


	import os
	import re
	import sys
	import ply.lex as lex
	import warnings
	warnings.filterwarnings("ignore")
	tokens = [
		'LPOP',
		'LCOUNTRY',
		'RCOUNTRY',
		'NAME',
		'LTCASE',
		'RTCASE',
		'LNCASE',
		'LTDEATH',
		'LACASE',
		'LNDEATH',
		]  

	lexer = lex.lex()
	lexer.input(str(country_data_update))
		
	import ply.yacc as yacc
	parser = yacc.yacc()
	parser.parse(country_data_update)

	return ans

#####################################################################################
#####################################################################################

# Parser to extract data of Continent from the Yesterday's data
def continent_parser(continent_data):

	continent_arr = []

	def t_LCONTI(t):
		r'<nobr>'
		return t

	def t_RCONTI(t):
		r'</nobr>'
		return t

	def t_LCDATA(t):
		r'<td>'
		return t

	def t_RCDATA(t):
		r'</td>'
		return t

	def t_CONAME(t):
		r"[A-Za-z0-9':,.\s\+\-]+"
		return t

	def p_start2(t):
		'''start2 : conname
				| condata
				'''

	def p_conname(t):
		'conname : LCONTI CONAME'
		t[0] = t[2]
		continent_arr.append(t[0])

	def p_condata(t):
		'condata : LCDATA CONAME'
		t[0] = t[2]
		continent_arr.append(t[0])

	import os
	import re
	import sys
	import ply.lex as lex
	import warnings
	warnings.filterwarnings("ignore")

	tokens = [
		'LCONTI',
		'RCONTI',
		'LCDATA',
		'RCDATA',
		'CONAME',
		]  

	lexer = lex.lex()
	lexer.input(str(continent_data))
	
	import ply.yacc as yacc
	parser = yacc.yacc()
	parser.parse(continent_data)

	return continent_arr

#####################################################################################
#####################################################################################

# Parser to extract data of World from the Yesterday's data
def world_parser():
	def t_LNAME(t):
		r'<td\sstyle="text\-align:left\;\">'
		return t

	def t_RNAME(t):
		r'</td>'
		return t

	def t_LDATA(t):
		r'<td>'
		return t

	def t_WNAME(t):
		r"[A-Za-z0-9':,.\+\-]+"
		return t

	def p_start1(t):
		'''start1 : tname
				| wdata
				| wwaste
				'''

	def p_tname(t):
		'tname : LNAME WNAME'
		t[0] = t[2]
		world_arr.append(t[0])

	def p_wdata(t):
		'wdata : LDATA WNAME'
		t[0] = t[2]
		world_arr.append(t[0])
	
	def p_wwaste(t):
		'wwaste : RNAME LNAME RNAME LNAME'
		t[0] = t[2]

	import os
	import re
	import sys
	import ply.lex as lex
	import warnings
	warnings.filterwarnings("ignore")
	tokens = [
		'LNAME',
		'RNAME',
		'LDATA',
		'WNAME',
		]  

	lexer = lex.lex()
	lexer.input(str(world_data))

	import ply.yacc as yacc
	parser = yacc.yacc()
	parser.parse(world_data)

world_parser()


def covid_worldometer_data():

	print("###################################################################")
	print("###################################################################")
	print("########################### COVID Data ############################")
	print("###################################################################")
	print("###################################################################")
	print()

	Field_requested = ['Total Cases', 'Active Cases', 'Total Deaths', 'Total Recovered', 'Total Tests', 'Deaths per Million', 'Tests per Million', 'New Cases', 'New Deaths', 'New Recovered', 'Change in Active Cases', 'Change in Daily Death', 'Change in New Recovered Cases', 'Change in New Cases']

	while(1):
		print("###################################################################")
		print()
		print("Get COVID Related information about world in following forms:")
		print("0: World")
		print("1: Continents")
		print("2: Countries")
		print("(Please enter number written before the given option)")
		print("Insert -1 if you want to exit")
		print()
		place_type = input()
		if(place_type == '0'):
			# World
			print("############################ World ################################")
			print()
			while(1):
				print("###################################################################")
				print()
				print("You Selected the: ",end="")
				print(world_arr[0])
				print()
				print("Select the any field for the information (insert index of the field):")
				print()
				print("0: Total Cases")
				print("1: Active Cases")
				print("2: Total Deaths")
				print("3: Total Recovered")
				print("4: Total Tests")
				print("5: Deaths per Million")
				print("6: Tests per Million")
				print("7: New Cases")
				print("8: New Deaths")
				print("9: New Recovered")
				print()
				print("Insert -1 to exit from this country!!")
				print()
				field_type = input()
				if(field_type == '0'):
					print("Total Number of Cases in this country are: ",end="")
					if(world_arr[1] == 'Data_Unavailable' or world_arr[1] == 'N' or world_arr[1] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[1])
						
						
				elif(field_type == '1'):
					print("Number of Active Cases in this country are: ",end="")
					if(world_arr[7] == 'Data_Unavailable' or world_arr[7] == 'N' or world_arr[7] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[7])
						
						
				elif(field_type == '2'):
					print("Total Number of Deaths in this country are: ",end="")
					if(world_arr[3] == 'Data_Unavailable' or world_arr[3] == 'N' or world_arr[3] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[3])
						
						
				elif(field_type == '3'):
					print("Total Number of Recovered Patients in this country are: ",end="")
					if(world_arr[5] == 'Data_Unavailable' or world_arr[5] == 'N' or world_arr[5] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[5])
						
						
				elif(field_type == '4'):
					print("Total Number Tests conducted in this country are: ",end="")
					print("This information is not available")
					
					
				elif(field_type == '5'):
					print("Deaths per 1 Million people in this country are: ",end="")
					if(world_arr[10] == 'Data_Unavailable' or world_arr[10] == 'N' or world_arr[10] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[10])
						
						
				elif(field_type == '6'):
					print("Tests per 1 Million people in this country are: ",end="")
					print("This information is not available")
					
					
				elif(field_type == '7'):
					print("New Cases in this country are: ",end="")
					if(world_arr[2] == 'Data_Unavailable' or world_arr[2] == 'N' or world_arr[2] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[2])
						
						
				elif(field_type == '8'):
					print("New Deaths in this country are: ",end="")
					if(world_arr[4] == 'Data_Unavailable' or world_arr[4] == 'N' or world_arr[4] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[4])
						
						
				elif(field_type == '9'):
					print("New Recovered Cases in this country are: ",end="")
					if(world_arr[6] == 'Data_Unavailable' or world_arr[6] == 'N' or world_arr[6] == 'td'):
						print("Data is not available")
						
						
					else:
						print(world_arr[6])
						
						
				elif(field_type == '-1'):
					break
				else:
					print("Wrong Input!!")
				print()
		elif(place_type == '1'):
			# Continent
			print("########################## Continents #############################")
			print()
			while(1):
				print("###################################################################")
				print()
				print("Select any of the continent for the information (insert index of the field):")
				print()
				print("0: Europe")
				print("1: North America")
				print("2: Asia")
				print("3: South America")
				print("4: Africa")
				print("5: Oceania or Australia")
				print()
				print("Insert -1 to go back from this continent tab!!")
				print()
				continent_selected = input()
				con_correct = 0
				if(continent_selected == '-1'):
					break
				elif(continent_selected.isdigit()):
					continent_selected = int(continent_selected)
					if(continent_selected < 6 and continent_selected >= 0):
						con_correct = 1
					else:
						print("Input is Out of Range")
				else:
					print("Wrong Input")

				while(con_correct == 1):
					continent_data = ""
					continent_flag = 0
					temp_cont_aus = 'Australia/Oceania'
					if(continent[continent_selected] == 'Oceania'):
						start_continent = '<tr class="total_row_world row_continent" data-continent="'+ temp_cont_aus +'" style="display: none">'
						end_continent = '<td style="display:none;" data-continent="'+ temp_cont_aus + '">'+ temp_cont_aus +'</td>'
					else:
						start_continent = '<tr class="total_row_world row_continent" data-continent="'+ continent[continent_selected] +'" style="display: none">'
						end_continent = '<td style="display:none;" data-continent="'+ continent[continent_selected] + '">'+ continent[continent_selected] +'</td>'
					for line in text.split("\n"):
						if(line == start_continent):
							continent_flag = 1
						if(continent_flag == 1):
							continent_data = continent_data + "\n" + line
						if(continent_flag == 1 and line == end_continent):
							break
					continent_data = continent_data[1:]
					# print(continent_data)

					continent_arr = continent_parser(continent_data)

					# print(continent_arr)
					print("###################################################################")
					print()
					print("You Selected the continent: ",end="")
					print(continent_arr[0])
					print()
					print("Select the any field for the information (insert index of the field):")
					print()
					print("0: Total Cases")
					print("1: Active Cases")
					print("2: Total Deaths")
					print("3: Total Recovered")
					print("4: Total Tests")
					print("5: Deaths per Million")
					print("6: Tests per Million")
					print("7: New Cases")
					print("8: New Deaths")
					print("9: New Recovered")
					print()
					print("Insert -1 to exit from this country!!")
					print()
					field_type = input()
					if(field_type == '0'):
						print("Total Number of Cases in this country are: ",end="")
						if(continent_arr[1] == 'Data_Unavailable' or continent_arr[1] == 'N' or continent_arr[1] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[1])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[1].replace(",", ""))
							den1 = float(world_arr[1].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total cases')
							
							
					elif(field_type == '1'):
						print("Number of Active Cases in this country are: ",end="")
						if(continent_arr[7] == 'Data_Unavailable' or continent_arr[7] == 'N' or continent_arr[7] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[7])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[7].replace(",", ""))
							den1 = float(world_arr[7].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world active cases')
							
							
					elif(field_type == '2'):
						print("Total Number of Deaths in this country are: ",end="")
						if(continent_arr[3] == 'Data_Unavailable' or continent_arr[3] == 'N' or continent_arr[3] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[3])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[3].replace(",", ""))
							den1 = float(world_arr[3].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total deaths')
							
							
					elif(field_type == '3'):
						print("Total Number of Recovered Patients in this country are: ",end="")
						if(continent_arr[5] == 'Data_Unavailable' or continent_arr[5] == 'N' or continent_arr[5] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[5])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[5].replace(",", ""))
							den1 = float(world_arr[5].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total recovered patients')
							
							
					elif(field_type == '4'):
						print("Total Number Tests conducted in this country are: ",end="")
						print("Data is not available")
						
						
					elif(field_type == '5'):
						print("Deaths per 1 Million people in this country are: ",end="")
						print("Data is not available")
						
						
					elif(field_type == '6'):
						print("Tests per 1 Million people in this country are: ",end="")
						print("Data is not available")
						
						
					elif(field_type == '7'):
						print("New Cases in this country are: ",end="")
						if(continent_arr[2] == 'Data_Unavailable' or continent_arr[2] == 'N' or continent_arr[2] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[2])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[2].replace(",", ""))
							den1 = float(world_arr[2].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new cases")
							
							
					elif(field_type == '8'):
						print("New Deaths in this country are: ",end="")
						if(continent_arr[4] == 'Data_Unavailable' or continent_arr[4] == 'N' or continent_arr[4] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[4])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[4].replace(",", ""))
							den1 = float(world_arr[4].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new deaths")
							
							
					elif(field_type == '9'):
						print("New Recovered Cases in this country are: ",end="")
						if(continent_arr[6] == 'Data_Unavailable' or continent_arr[6] == 'N' or continent_arr[6] == 'td'):
							print("Data is not available")
							
							
						else:
							print(continent_arr[6])
							print("It is equivalent to ", end="")
							num1 = float(continent_arr[6].replace(",", ""))
							den1 = float(world_arr[6].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new recovered cases")
							
							
					elif(field_type == '-1'):
						break
					else:
						print("Wrong Input!!")
					print()

		elif(place_type == '2'):
			# Countries
			print("########################## Countries ##############################")
			print()
			while(1):
				for i in range(len(country)):
					print(i, country[i], end="")
					if(i%4 == 3):
						print()
					else:
						print("\t", end="")
				print()

				print("\nSelect any country from above (Please enter the serial number written before the country name):")
				print()
				print("Insert -1 to go back from this country tab!!")
				print()
				country_selected = input()
				correct = 0
				if(country_selected == '-1'):
					break
				elif(country_selected.isdigit()):
					country_selected = int(country_selected)
					if(country_selected < 55 and country_selected >= 0):
						correct = 1
					else:
						print("Input is Out of Range")
				else:
					print("Wrong Input")

				while(correct == 1):
					flag_country = 0
					country_data = ""
					start_country = '<td style="font-weight: bold; font-size:15px; text-align:left;"><a class="mt_a" href="country/' + country_modified[country_selected] + '/">' + country[country_selected] + '</a></td>'
					end_country = '</tr>'
					for line in text.split('\n'):
						if(line == start_country):
							flag_country = 1
						if(flag_country == 1):
							country_data = country_data + "\n" + line
						if(flag_country == 1  and end_country == line):
							break

					flag = 0
					country_data_update = ""
					for line in country_data.split("\n"):
						if(line[-6:] == '></td>'):
							if('></a></td>' == line[-10:]):
								line = line[:-9] + 'Data_Unavailable' + line[-9:]
							elif('> </a></td>' == line[-11:]):
								line = line[:-10] + 'Data_Unavailable' + line[-9:]
							elif('</a></td>' == line[-9:]):
								flag = 0
							else:
								line = line[:-5] + 'Data_Unavailable' + line[-5:]
						elif('> </td>' == line[-7:]):
							if('></a> </td>' == line[-11:]):
								line = line[:-10] + 'Data_Unavailable' + line[-10:]
							elif('> </a> </td>' == line[-12:]):
								line = line[:-11] + 'Data_Unavailable' + line[-10:]
							elif('</a> </td>' == line[-10:]):
								flag = 0
							else:
								line = line[:-6] + 'Data_Unavailable' + line[-5:]
						country_data_update = country_data_update + "\n" + line

					country_data_update = country_data_update[2:]

					# Array Storing result of countries
					ans = country_parser(country_data_update)

					print("###################################################################")
					print()
					print("You Selected the Country: ",end="")
					print(ans[0])
					print()
					print("Select the any field for the information (insert index of the field):")
					print()
					print("0: Total Cases")
					print("1: Active Cases")
					print("2: Total Deaths")
					print("3: Total Recovered")
					print("4: Total Tests")
					print("5: Deaths per Million")
					print("6: Tests per Million")
					print("7: New Cases")
					print("8: New Deaths")
					print("9: New Recovered")
					print("10: Change in Active Cases")
					print("11: Change in Daily Death")
					print("12: Change in New Recovered Cases")
					print("13: Change in New Cases")
					print()
					print("Insert -1 to exit from this country!!")
					print()
					field_type = input()
					
					if(field_type == '0'):
						print("Total Number of Cases in this country are: ",end="")
						if(ans[1] == 'Data_Unavailable' or ans[1] == 'N' or ans[1] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[1])
							print("It is equivalent to ", end="")
							num1 = float(ans[1].replace(",", ""))
							den1 = float(world_arr[1].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total cases')
							
							
					
					elif(field_type == '1'):
						print("Number of Active Cases in this country are: ",end="")
						if(ans[7] == 'Data_Unavailable' or ans[7] == 'N' or ans[7] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[7])
							print("It is equivalent to ", end="")
							num1 = float(ans[7].replace(",", ""))
							den1 = float(world_arr[7].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world active cases')
							
							
					
					elif(field_type == '2'):
						print("Total Number of Deaths in this country are: ",end="")
						if(ans[3] == 'Data_Unavailable' or ans[3] == 'N' or ans[3] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[3])
							print("It is equivalent to ", end="")
							num1 = float(ans[3].replace(",", ""))
							den1 = float(world_arr[3].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total deaths')
							
							
					
					elif(field_type == '3'):
						print("Total Number of Recovered Patients in this country are: ",end="")
						if(ans[5] == 'Data_Unavailable' or ans[5] == 'N' or ans[5] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[5])
							print("It is equivalent to ", end="")
							num1 = float(ans[5].replace(",", ""))
							den1 = float(world_arr[5].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print('% of world total recovered patients')
							
							
					
					elif(field_type == '4'):
						print("Total Number Tests conducted in this country are: ",end="")
						if(ans[11] == 'Data_Unavailable' or ans[11] == 'N' or ans[11] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[11])
							
							
					
					elif(field_type == '5'):
						print("Deaths per 1 Million people in this country are: ",end="")
						if(ans[10] == 'Data_Unavailable' or ans[10] == 'N' or ans[10] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[10])
							print("It is equivalent to ", end="")
							num1 = float(ans[10].replace(",", ""))
							den1 = float(world_arr[10].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's deaths per 1 million people")
							
							
					
					elif(field_type == '6'):
						print("Tests per 1 Million people in this country are: ",end="")
						if(ans[12] == 'Data_Unavailable' or ans[12] == 'N' or ans[12] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[12])
							
							
					
					elif(field_type == '7'):
						print("New Cases in this country are: ",end="")
						if(ans[2] == 'Data_Unavailable' or ans[2] == 'N' or ans[2] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[2])
							print("It is equivalent to ", end="")
							num1 = float(ans[2].replace(",", ""))
							den1 = float(world_arr[2].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new cases")
							
							
					
					elif(field_type == '8'):
						print("New Deaths in this country are: ",end="")
						if(ans[4] == 'Data_Unavailable' or ans[4] == 'N' or ans[4] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[4])
							print("It is equivalent to ", end="")
							num1 = float(ans[4].replace(",", ""))
							den1 = float(world_arr[4].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new deaths")
							
							
					
					elif(field_type == '9'):
						print("New Recovered Cases in this country are: ",end="")
						if(ans[6] == 'Data_Unavailable' or ans[6] == 'N' or ans[6] == 'td'):
							print("Data is not available")
							
							
						else:
							print(ans[6])
							print("It is equivalent to ", end="")
							num1 = float(ans[6].replace(",", ""))
							den1 = float(world_arr[6].replace(",",""))
							print(round(((num1/den1)*100), 4), end="")
							print("% of world's new recovered cases")
							
							
					
					elif(field_type == '10'):
						if(country_modified[country_selected] == 'us'):
							selected_country = 'Corona_usa.html'
						elif(country_modified[country_selected] == 'viet-nam'):
							selected_country = 'Corona_vietnam.html'
						else:
							selected_country = 'Corona_' + country_modified[country_selected] + '.html'

						file = open(selected_country, 'r')
						flag = 0
						country_active_case = ""
						for line in file:
							if(line == """            text: 'Active Cases'\n"""):
								flag=1
							elif(flag==1 and line == """        responsive: {\n"""):
								break
							if(flag == 1):
								country_active_case = country_active_case + line
						file.close()

						if(country_active_case == ""):
							print("Data of Active Cases is not available")
							
							

						else:
							warnings.filterwarnings("ignore")
							activecase_arr = active_case_parser(country_active_case)
							warnings.filterwarnings("ignore")
							activecase_arr[0] = activecase_arr[0].replace(", ", " ")
							
							activecase_arr[0] = activecase_arr[0].replace("Jan", "01")
							activecase_arr[0] = activecase_arr[0].replace("Feb", "02")
							activecase_arr[0] = activecase_arr[0].replace("Mar", "03")
							activecase_arr[0] = activecase_arr[0].replace("Apr", "04")
							activecase_arr[0] = activecase_arr[0].replace("May", "05")
							activecase_arr[0] = activecase_arr[0].replace("Jun", "06")
							activecase_arr[0] = activecase_arr[0].replace("Jul", "07")
							activecase_arr[0] = activecase_arr[0].replace("Aug", "08")
							activecase_arr[0] = activecase_arr[0].replace("Sep", "09")
							activecase_arr[0] = activecase_arr[0].replace("Oct", "10")
							activecase_arr[0] = activecase_arr[0].replace("Nov", "11")
							activecase_arr[0] = activecase_arr[0].replace("Dec", "12")

							dates = []
							for date in activecase_arr[0].split(','):
								date = date.replace('"', '')
								date = date.replace(' ', '-')
								dates.append(date)
							datas = []
							for data in activecase_arr[1].split(','):
								datas.append(data)
							warnings.filterwarnings("ignore")
							print("Please Enter the Start Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							start_date = input()
							print("Please Enter the End Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							end_date = input()
							print()
							flag_active_case = 0
							for i in range(len(dates)):
								if(start_date == dates[i]):
									ind_start_date = i
									flag_active_case = flag_active_case + 1
								if(end_date == dates[i]):
									ind_end_date = i
									flag_active_case = flag_active_case + 1
							if(flag_active_case < 2):
								print("There is error in the given date (invalid)!!")
								
								
							else:
								if(datas[ind_start_date]=='null' and datas[ind_end_date]=='null'):
									print("Data of the given dates are not available!!")
									
									
								elif(datas[ind_start_date]=='null'):
									print('Data of the start date is not available, and Active Cases on end date are ', end="")
									print(datas[ind_end_date])
									
									
								elif(datas[ind_end_date]=='null'):
									print('Data of the end date is not available, and Active Cases on start date are ', end="")
									print(datas[ind_start_date])
									
									
								else:
									if(ind_start_date >= ind_end_date):
										print("Start Date should be less than the End Date in the given range!!")
										
										
									else:
										if(float(datas[ind_end_date]) < 0 and float(datas[ind_start_date]) < 0):
											print("Data of the given dates are is incorrect (Data is negative, and that is not possible)!!")
											
											
										elif(float(datas[ind_start_date]) < 0):
											print('Data of the start date is negative, and Active Cases on end date are ', end="")
											print(datas[ind_end_date])
											
											
										elif(float(datas[ind_end_date]) < 0):
											print('Data of the end date is negative, and Active Cases on start date are ', end="")
											print(datas[ind_start_date])
											
											
										else:
											change_active = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
											print('Change in Active Cases:', round(change_active, 4), '%')
											
											other_country_data_available = 0
											change_nearest_country_percent_active = 1000000000000
											for desh in range(len(country)):
												if(desh != country_selected):

													if(country_modified[desh] == 'us'):
														unselected_country = 'Corona_usa.html'
													elif(country_modified[desh] == 'viet-nam'):
														unselected_country = 'Corona_vietnam.html'
													else:
														unselected_country = 'Corona_' + country_modified[desh] + '.html'

													import warnings
													warnings.filterwarnings("ignore")
													file = open(unselected_country, 'r')
													flag = 0
													un_country_active_case = ""
													for line in file:
														if(line == """            text: 'Active Cases'\n"""):
															flag=1
														elif(flag==1 and line == """        responsive: {\n"""):
															break
														if(flag == 1):
															un_country_active_case = un_country_active_case + line
													file.close()
													if(un_country_active_case != ""):
														un_activecase_arr = active_case_parser(un_country_active_case)

														un_activecase_arr[0] = un_activecase_arr[0].replace(", ", " ")
														
														un_activecase_arr[0] = un_activecase_arr[0].replace("Jan", "01")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Feb", "02")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Mar", "03")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Apr", "04")
														un_activecase_arr[0] = un_activecase_arr[0].replace("May", "05")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Jun", "06")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Jul", "07")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Aug", "08")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Sep", "09")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Oct", "10")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Nov", "11")
														un_activecase_arr[0] = un_activecase_arr[0].replace("Dec", "12")

														dates = []
														for date in un_activecase_arr[0].split(','):
															date = date.replace('"', '')
															date = date.replace(' ', '-')
															dates.append(date)
														datas = []
														for data in un_activecase_arr[1].split(','):
															datas.append(data)
														

														if(datas[ind_start_date]!='null' and datas[ind_end_date]!='null'):
															un_change_active = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
															if(abs(change_active - un_change_active) < change_nearest_country_percent_active):
																other_country_data_available = 1
																change_nearest_country_percent_active = abs(change_active - un_change_active)
																nearest_country_active_percent = un_change_active
																nearest_country_active = country[desh]
											if(other_country_data_available == 1):
												print("-----------------------------------")
												print('Country having Nearest Change in Active Cases:', nearest_country_active, ", and it's Change Percentage is:", round(nearest_country_active_percent, 4),"%")
												print('The difference of change in Active Cases between both the countries is:', round(change_nearest_country_percent_active, 4), '%')
												print()
												
												
											else:
												print("No other country has valid data for these dates!!")
												print()
												
												

					elif(field_type == '11'):
						
						if(country_modified[country_selected] == 'us'):
							selected_country = 'Corona_usa.html'
						elif(country_modified[country_selected] == 'viet-nam'):
							selected_country = 'Corona_vietnam.html'
						else:
							selected_country = 'Corona_' + country_modified[country_selected] + '.html'

						file = open(selected_country, 'r')
						flag = 0
						country_new_death_case = ""
						for line in file:
							if(line == """            text: 'Daily Deaths'\n"""):
								flag=1
							elif(flag==1 and line == """                name: '3-day moving average',\n"""):
								break
							if(flag == 1):
								country_new_death_case = country_new_death_case + line
						file.close()

						if(country_new_death_case == ""):
							print("Data of New Death Cases is not available")

							

						else:
							warnings.filterwarnings("ignore")
							new_death_case_arr = new_death_case_parser(country_new_death_case)
							warnings.filterwarnings("ignore")
							
							new_death_case_arr[0] = new_death_case_arr[0].replace(", ", " ")
							
							new_death_case_arr[0] = new_death_case_arr[0].replace("Jan", "01")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Feb", "02")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Mar", "03")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Apr", "04")
							new_death_case_arr[0] = new_death_case_arr[0].replace("May", "05")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Jun", "06")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Jul", "07")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Aug", "08")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Sep", "09")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Oct", "10")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Nov", "11")
							new_death_case_arr[0] = new_death_case_arr[0].replace("Dec", "12")

							dates = []
							for date in new_death_case_arr[0].split(','):
								date = date.replace('"', '')
								date = date.replace(' ', '-')
								dates.append(date)
							
							datas = []
							for data in new_death_case_arr[1].split(','):
								datas.append(data)
							
							warnings.filterwarnings("ignore")
							print("Please Enter the Start Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							start_date = input()
							print("Please Enter the End Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							end_date = input()
							print()
							flag_new_death_case = 0
							for i in range(len(dates)):
								if(start_date == dates[i]):
									ind_start_date = i
									flag_new_death_case = flag_new_death_case + 1
								if(end_date == dates[i]):
									ind_end_date = i
									flag_new_death_case = flag_new_death_case + 1
							if(flag_new_death_case < 2):
								print("There is error in the given date (invalid)!!")

								
							else:
								if(datas[ind_start_date]=='null' and datas[ind_end_date]=='null'):
									print("Data of the given dates are not available!!")

									
								elif(datas[ind_start_date]=='null'):
									print('Data of the start date is not available, and New Deaths on end date are ', end="")
									print(datas[ind_end_date])

									
								elif(datas[ind_end_date]=='null'):
									print('Data of the end date is not available, and New Deaths on start date are ', end="")
									print(datas[ind_start_date])

									
								else:
									if(ind_start_date >= ind_end_date):
										print("Start Date should be less than the End Date in the given range!!")

										
									else:
										if(float(datas[ind_end_date]) < 0 and float(datas[ind_start_date]) < 0):
											print("Data of the given dates are is incorrect (Data is negative, and that is not possible)!!")
											
											
										elif(float(datas[ind_start_date]) < 0):
											print('Data of the start date is negative, and New Deaths on end date are ', end="")
											print(datas[ind_end_date])

											
										elif(float(datas[ind_end_date]) < 0):
											print('Data of the end date is negative, and New Deaths on start date are ', end="")
											print(datas[ind_start_date])

											
										else:
											change_new_death_case = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
											print('Change in New Deaths:', round(change_new_death_case, 4), '%')
											
											other_country_data_available = 0
											change_nearest_country_percent_new_death_case = 1000000000000
											for desh in range(len(country)):
												if(desh != country_selected):

													if(country_modified[desh] == 'us'):
														unselected_country = 'Corona_usa.html'
													elif(country_modified[desh] == 'viet-nam'):
														unselected_country = 'Corona_vietnam.html'
													else:
														unselected_country = 'Corona_' + country_modified[desh] + '.html'

													import warnings
													warnings.filterwarnings("ignore")

													file = open(unselected_country, 'r')
													flag = 0
													un_country_new_death_case = ""
													for line in file:
														if(line == """            text: 'Daily Deaths'\n"""):
															flag=1
														elif(flag==1 and line == """                name: '3-day moving average',\n"""):
															break
														if(flag == 1):
															un_country_new_death_case = un_country_new_death_case + line
													file.close()
													# print(un_country_active_case)
													if(un_country_new_death_case != ""):
														un_new_death_case_arr = new_death_case_parser(un_country_new_death_case)

														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace(", ", " ")
														
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Jan", "01")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Feb", "02")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Mar", "03")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Apr", "04")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("May", "05")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Jun", "06")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Jul", "07")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Aug", "08")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Sep", "09")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Oct", "10")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Nov", "11")
														un_new_death_case_arr[0] = un_new_death_case_arr[0].replace("Dec", "12")

														dates = []
														for date in un_new_death_case_arr[0].split(','):
															date = date.replace('"', '')
															date = date.replace(' ', '-')
															dates.append(date)
														# print(dates)
														datas = []
														for data in un_new_death_case_arr[1].split(','):
															datas.append(data)
														

														if(datas[ind_start_date]!='null' and datas[ind_end_date]!='null' and float(datas[ind_end_date]) >= 0 and float(datas[ind_start_date]) >= 0):
															un_change_new_death_case = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
															# print(country[desh])
															if(abs(change_new_death_case - un_change_new_death_case) < change_nearest_country_percent_new_death_case):
																other_country_data_available = 1
																change_nearest_country_percent_new_death_case = abs(change_new_death_case - un_change_new_death_case)
																nearest_country_new_death_case_percent = un_change_new_death_case
																nearest_country_new_death_case = country[desh]
											if(other_country_data_available == 1):
												print("-----------------------------------")
												print('Country having Nearest Change in Death Cases:', nearest_country_new_death_case, ", and it's Change Percentage is:", round(nearest_country_new_death_case_percent, 4),"%")
												print('The difference of change in Death Cases between both the countries is:', round(change_nearest_country_percent_new_death_case, 4), '%')
												print()

												
											else:
												print("No other country has valid data for these dates!!")
												print()

												

					elif(field_type == '12'):
						
						if(country_modified[country_selected] == 'us'):
							selected_country = 'Corona_usa.html'
						elif(country_modified[country_selected] == 'viet-nam'):
							selected_country = 'Corona_vietnam.html'
						else:
							selected_country = 'Corona_' + country_modified[country_selected] + '.html'
						file = open(selected_country, 'r')
						flag = 0
						country_new_recovered_case = ""
						for line in file:
							if(line == """            text: 'New Cases vs. New Recoveries'\n"""):
								flag=1
							elif(flag==1 and line == """            name: 'New Cases',\n"""):
								break
							if(flag == 1):
								country_new_recovered_case = country_new_recovered_case + line
						file.close()

						if(country_new_recovered_case == ""):
							# print(selected_country)
							print("Data of Recovery is not available")

							

						else:
							new_recovered_case_arr = new_recovered_case_parser(country_new_recovered_case)
							
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace(", ", " ")

							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Jan", "01")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Feb", "02")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Mar", "03")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Apr", "04")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("May", "05")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Jun", "06")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Jul", "07")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Aug", "08")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Sep", "09")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Oct", "10")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Nov", "11")
							new_recovered_case_arr[0] = new_recovered_case_arr[0].replace("Dec", "12")

							dates = []
							for date in new_recovered_case_arr[0].split(','):
								date = date.replace('"', '')
								date = date.replace(' ', '-')
								dates.append(date)
							
							datas = []
							for data in new_recovered_case_arr[1].split(','):
								datas.append(data)
							
							warnings.filterwarnings("ignore")
							print("Please Enter the Start Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							start_date = input()
							print("Please Enter the End Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							end_date = input()
							print()

							flag_re_case = 0
							for i in range(len(dates)):
								if(start_date == dates[i]):
									ind_start_date = i
									flag_re_case = flag_re_case + 1
								if(end_date == dates[i]):
									ind_end_date = i
									flag_re_case = flag_re_case + 1
							if(flag_re_case < 2):
								print("One or both of the given date is invalid!!")

								
							else:
								if(datas[ind_start_date]=='null' and datas[ind_end_date]=='null'):
									print("Data of the given dates are not available!!")

									
								elif(datas[ind_start_date]=='null'):
									print('Data of the start date is not available, and Patients Recovered on end date are ', end="")
									print(datas[ind_end_date])

									
								elif(datas[ind_end_date]=='null'):
									print('Data of the end date is not available, and Patients Recovered on start date are ', end="")
									print(datas[ind_start_date])

									
								else:
									if(ind_start_date >= ind_end_date):
										print("Start Date should be less than the End Date in the given range!!")

										
									else:
										if(float(datas[ind_end_date]) < 0 and float(datas[ind_start_date]) < 0):
											print("Data of the given dates are is incorrect (Data is negative, and that is not possible)!!")

											
										elif(float(datas[ind_start_date]) < 0):
											print('Data of the start date is negative, and Patients Recovered on end date are ', end="")
											print(datas[ind_end_date])

											
										elif(float(datas[ind_end_date]) < 0):
											print('Data of the end date is negative, and Patients Recovered on start date are ', end="")
											print(datas[ind_start_date])

											
										else:
											change_re = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
											print('Change in Recovery of Patients:', round(change_re, 4), '%')
											
											other_country_data_available = 0
											change_nearest_country_percent_recovery = 1000000000000

											for desh in range(len(country)):
												if(desh != country_selected):
													if(country_modified[desh] == 'us'):
														unselected_country = 'Corona_usa.html'
													elif(country_modified[desh] == 'viet-nam'):
														unselected_country = 'Corona_vietnam.html'
													else:
														unselected_country = 'Corona_' + country_modified[desh] + '.html'

													import warnings
													warnings.filterwarnings("ignore")

													file = open(unselected_country, 'r')
													flag = 0
													un_country_new_recovered_case = ""
													for line in file:
														if(line == """            text: 'New Cases vs. New Recoveries'\n"""):
															flag=1
														elif(flag==1 and line == """            name: 'New Cases',\n"""):
															break
														if(flag == 1):
															un_country_new_recovered_case = un_country_new_recovered_case + line
													file.close()

													if(un_country_new_recovered_case != ""):
														un_new_recovered_case_arr = new_recovered_case_parser(un_country_new_recovered_case)

														# print(un_new_recovered_case_arr)
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace(", ", " ")
														
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Jan", "01")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Feb", "02")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Mar", "03")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Apr", "04")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("May", "05")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Jun", "06")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Jul", "07")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Aug", "08")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Sep", "09")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Oct", "10")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Nov", "11")
														un_new_recovered_case_arr[0] = un_new_recovered_case_arr[0].replace("Dec", "12")

														# print(un_new_recovered_case_arr)
														dates = []
														for date in un_new_recovered_case_arr[0].split(','):
															date = date.replace('"', '')
															date = date.replace(' ', '-')
															dates.append(date)
														# print(dates)
														datas = []
														for data in un_new_recovered_case_arr[1].split(','):
															datas.append(data)
														
														if(datas[ind_start_date]!='null' and datas[ind_end_date]!='null' and float(datas[ind_end_date]) >= 0 and float(datas[ind_start_date]) >= 0):
															un_change_re = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
															if(abs(change_re-un_change_re) < change_nearest_country_percent_recovery):
																other_country_data_available = 1
																change_nearest_country_percent_recovery = abs(change_re-un_change_re)
																nearest_country_recovery_percent = un_change_re
																nearest_country_recovery = country[desh]

											if(other_country_data_available == 1):
												print("-----------------------------------")
												print('Country having Nearest Change in Recovery Cases:', nearest_country_recovery, ", and it's Change Percentage is:", round(nearest_country_recovery_percent, 4),"%")
												print('The difference of change in Recovery Cases between both the countries is:', round(change_nearest_country_percent_recovery, 4), '%')
												print()

												
											else:
												print("No other country has valid data for these dates!!")
												print()

												

					elif(field_type == '13'):
						if(country_modified[country_selected] == 'us'):
							selected_country = 'Corona_usa.html'
						elif(country_modified[country_selected] == 'viet-nam'):
							selected_country = 'Corona_vietnam.html'
						else:
							selected_country = 'Corona_' + country_modified[country_selected] + '.html'

						import warnings
						warnings.filterwarnings("ignore")
						file = open(selected_country, 'r')
						flag = 0
						country_new_case = ""
						for line in file:
							if(line == """            text: 'Daily New Cases'\n"""):
								flag=1
							elif(flag==1 and line == """                name: '3-day moving average',\n"""):
								break
							if(flag == 1):
								country_new_case = country_new_case + line
						file.close()


						if(country_new_case == ""):
							print("Data of New Cases is not available")

							

						else:
							warnings.filterwarnings("ignore")
							newcase_arr = new_case_parser(country_new_case)
							warnings.filterwarnings("ignore")

							newcase_arr[0] = newcase_arr[0].replace(", ", " ")
							
							newcase_arr[0] = newcase_arr[0].replace("Jan", "01")
							newcase_arr[0] = newcase_arr[0].replace("Feb", "02")
							newcase_arr[0] = newcase_arr[0].replace("Mar", "03")
							newcase_arr[0] = newcase_arr[0].replace("Apr", "04")
							newcase_arr[0] = newcase_arr[0].replace("May", "05")
							newcase_arr[0] = newcase_arr[0].replace("Jun", "06")
							newcase_arr[0] = newcase_arr[0].replace("Jul", "07")
							newcase_arr[0] = newcase_arr[0].replace("Aug", "08")
							newcase_arr[0] = newcase_arr[0].replace("Sep", "09")
							newcase_arr[0] = newcase_arr[0].replace("Oct", "10")
							newcase_arr[0] = newcase_arr[0].replace("Nov", "11")
							newcase_arr[0] = newcase_arr[0].replace("Dec", "12")

							dates = []
							for date in newcase_arr[0].split(','):
								date = date.replace('"', '')
								date = date.replace(' ', '-')
								dates.append(date)

							datas = []
							for data in newcase_arr[1].split(','):
								datas.append(data)

							print("Please Enter the Start Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							start_date = input()
							print("Please Enter the End Date in the format mm-dd-yyyy:")
							print("For example: May 06, 2021 should be written as 05-06-2021")
							end_date = input()
							print()
							flag_new_case = 0
							for i in range(len(dates)):
								if(start_date == dates[i]):
									ind_start_date = i
									flag_new_case = flag_new_case + 1
								if(end_date == dates[i]):
									ind_end_date = i
									flag_new_case = flag_new_case + 1
							if(flag_new_case < 2):
								print("There is error in the given date (invalid)!!")

								
							else:
								if(datas[ind_start_date]=='null' and datas[ind_end_date]=='null'):
									print("Data of the given dates are not available!!")

									
								elif(datas[ind_start_date]=='null'):
									print('Data of the start date is not available, and New Cases on end date are ', end="")
									print(datas[ind_end_date])

									
								elif(datas[ind_end_date]=='null'):
									print('Data of the end date is not available, and New Cases on start date are ', end="")
									print(datas[ind_start_date])

									
								else:
									if(ind_start_date >= ind_end_date):
										print("Start Date should be less than the End Date in the given range!!")

										
									else:
										if(float(datas[ind_end_date]) < 0 and float(datas[ind_start_date]) < 0):
											print("Data of the given dates are is incorrect (Data is negative, and that is not possible)!!")

											
										elif(float(datas[ind_start_date]) < 0):
											print('Data of the start date is negative, and New Cases on end date are ', end="")
											print(datas[ind_end_date])

											
										elif(float(datas[ind_end_date]) < 0):
											print('Data of the end date is negative, and New Cases on start date are ', end="")
											print(datas[ind_start_date])

											
										else:
											change_new_case = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
											print('Change in New Cases:', round(change_new_case, 4), '%')
											
											other_country_data_available = 0
											change_nearest_country_percent_new_case = 1000000000000
											for desh in range(len(country)):
												if(desh != country_selected):

													if(country_modified[desh] == 'us'):
														unselected_country = 'Corona_usa.html'
													elif(country_modified[desh] == 'viet-nam'):
														unselected_country = 'Corona_vietnam.html'
													else:
														unselected_country = 'Corona_' + country_modified[desh] + '.html'

													import warnings
													warnings.filterwarnings("ignore")

													file = open(unselected_country, 'r')
													flag = 0
													un_country_new_case = ""
													for line in file:
														if(line == """            text: 'Daily New Cases'\n"""):
															flag=1
														elif(flag==1 and line == """                name: '3-day moving average',\n"""):
															break
														if(flag == 1):
															un_country_new_case = un_country_new_case + line
													file.close()
													# print(un_country_active_case)
													if(un_country_new_case != ""):
														un_newcase_arr = new_case_parser(un_country_new_case)

														un_newcase_arr[0] = un_newcase_arr[0].replace(", ", " ")
														
														un_newcase_arr[0] = un_newcase_arr[0].replace("Jan", "01")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Feb", "02")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Mar", "03")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Apr", "04")
														un_newcase_arr[0] = un_newcase_arr[0].replace("May", "05")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Jun", "06")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Jul", "07")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Aug", "08")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Sep", "09")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Oct", "10")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Nov", "11")
														un_newcase_arr[0] = un_newcase_arr[0].replace("Dec", "12")

														dates = []
														for date in un_newcase_arr[0].split(','):
															date = date.replace('"', '')
															date = date.replace(' ', '-')
															dates.append(date)
														# print(dates)
														datas = []
														for data in un_newcase_arr[1].split(','):
															datas.append(data)
														

														if(datas[ind_start_date]!='null' and datas[ind_end_date]!='null' and float(datas[ind_end_date]) >= 0 and float(datas[ind_start_date]) >= 0):
															un_change_new_case = (((float(datas[ind_end_date])-float(datas[ind_start_date]))/(float(datas[ind_start_date])+0.0001))*100)
															# print(country[desh])
															if(abs(change_new_case - un_change_new_case) < change_nearest_country_percent_new_case):
																other_country_data_available = 1
																change_nearest_country_percent_new_case = abs(change_new_case - un_change_new_case)
																nearest_country_new_case_percent = un_change_new_case
																nearest_country_new_case = country[desh]
											if(other_country_data_available == 1):
												print("-----------------------------------")
												print('Country having Nearest Change in New Cases:', nearest_country_new_case, ", and it's Change Percentage is:", round(nearest_country_new_case_percent, 4),"%")
												print('The difference of change in New Cases between both the countries is:', round(change_nearest_country_percent_new_case, 4), '%')
												print()

												
											else:
												print("No other country has valid data for these dates!!")
												print()

												

					elif(field_type == '-1'):
						break
					else:
						print("Wrong Input!!")
					print()

		elif(place_type == '-1'):
			break
		else:
			print("Wrong Selection!!!")