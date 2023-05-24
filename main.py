import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import urllib.request
from urllib.request import urlopen
from tqdm import tqdm
# task 2 file is imported to merge the previous assignment to this file
from task2 import covid_worldometer_data
import re
import os

print("Pre-Processing is Started!!")

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
headers={'User-Agent':user_agent,} 

valid_dates = []

t_ignore = " \t"

def t_error(t):
	t.lexer.skip(1)

def p_error(t):
	pass

# Extract content from country files
def country_range2(country_complete_data):
    
    country_final_range = []
    
    def t_LCOUNTRYRANGE2(t):
        r'\<h2\>\<span\sclass="mw-headline"\sid=\"'
        return t

    def t_RCOUNTRYRANGE2(t):
        r'">'
        return t

    def t_COUNTRYRANGE2(t):
        r"[A-Za-z0-9e̝\_]+"
        return t

    def p_start8(t):
        '''start8 : countrydaterange2
                '''

    def p_countrydaterange2(t):
        'countrydaterange2 : LCOUNTRYRANGE2 COUNTRYRANGE2 RCOUNTRYRANGE2'
        t[0] = t[2]
        country_final_range.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LCOUNTRYRANGE2',
        'RCOUNTRYRANGE2',
        'COUNTRYRANGE2',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_complete_data))
    
    
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_complete_data)

    return country_final_range

# Extract content from country files
def country_range1(country_complete_data):
    
    country_final_range = []
    
    def t_LCOUNTRYRANGE1(t):
        r'\<h3\>\<span\sclass="mw-headline"\sid=\"'
        return t

    def t_RCOUNTRYRANGE1(t):
        r'">'
        return t

    def t_COUNTRYRANGE1(t):
        r"[A-Za-z0-9e̝\_]+"
        return t

    def p_start7(t):
        '''start7 : countrydaterange1
                '''

    def p_countrydaterange1(t):
        'countrydaterange1 : LCOUNTRYRANGE1 COUNTRYRANGE1 RCOUNTRYRANGE1'
        t[0] = t[2]
        country_final_range.append(t[0])

    import os
    import re
    import sys
    import ply.lex as lex
    import warnings
    warnings.filterwarnings("ignore")

    tokens = [
        'LCOUNTRYRANGE1',
        'RCOUNTRYRANGE1',
        'COUNTRYRANGE1',
        ]  

    lexer = lex.lex()
    lexer.input(str(country_complete_data))
    
    
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.parse(country_complete_data)

    return country_final_range

# dictionary used for month convertion
month_caps = {}
month_caps['01'] = 'January'
month_caps['02'] = 'February'
month_caps['03'] = 'March'
month_caps['04'] = 'April'
month_caps['05'] = 'May'
month_caps['06'] = 'June'
month_caps['07'] = 'July'
month_caps['08'] = 'August'
month_caps['09'] = 'September'
month_caps['10'] = 'October'
month_caps['11'] = 'November'
month_caps['12'] = 'December'

# list storing valid years
year_caps = []
year_caps.append('2019')
year_caps.append('2020')
year_caps.append('2021')
year_caps.append('2022')

# Main URL for timeline
main_url = "https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"

# Dictionary Storing all the data as per date
wiki_timeline = {}

count = 0

# Extracting Data from Timeline files
for year in year_caps:
    for month in month_caps:
        if(year == '2019'):
            continue
        if(year == '2022' and month == '04'):
            break
        url = main_url + '_in_' + month_caps[month] + '_' + year
        
        request = urllib.request.Request(url,None,headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        
        file = open('temp1.html', 'wb')
        file.write(data)
        file.close()
        
        for i in range(1, 32):
            line_flag = 0
            file = open('temp1.html', 'r')
            file_data = ''
            for line in file:
                if(month == '02' and year == '2020' and i > 13):
                    if(line_flag == 2 and (line == '<h3><span class="mw-headline" id="' + str(i+1) + '_' + month_caps[month] + '">' + str(i+1) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+4) + '" title="Edit section: ' + str(i+1) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n') or line == '<h2><span class="mw-headline" id="Summary">Summary</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+4) + '" title="Edit section: Summary">edit</a><span class="mw-editsection-bracket">]</span></span></h2>\n'):
                        line_flag = 0
                        break
                    if(line == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+3) + '" title="Edit section: ' + str(i) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n')):
                        line_flag = 2
                    if(line_flag == 2):
                        file_data = file_data + line
                    
                elif(month == '02' and year == '2020' and i == 13):
                    if(line_flag == 2 and (line == '<h3><span class="mw-headline" id="' + str(i+1) + '_' + month_caps[month] + '">' + str(i+1) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+4) + '" title="Edit section: ' + str(i+1) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n') or line == '<h2><span class="mw-headline" id="Summary">Summary</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+4) + '" title="Edit section: Summary">edit</a><span class="mw-editsection-bracket">]</span></span></h2>\n'):
                        line_flag = 0
                        break
                    if(line == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+2) + '" title="Edit section: ' + str(i) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n')):
                        line_flag = 2
                    if(line_flag == 2):
                        file_data = file_data + line

                elif(month == '01' and year == '2020' and i == 12):
                    if(line_flag == 1 and (line == '<h2><span class="mw-headline" id="Summary">Summary</span></h2>\n' or line == '<h3><span class="mw-headline" id="' + str(i+1) + '_' + month_caps[month] + '">' + str(i+1) + ' ' + month_caps[month] + '</span></h3>\n')):
                        line_flag = 0
                        break
                    if(line == ('<h3><span id="11.E2.80.9312_January"></span><span class="mw-headline" id="11–12_January">11–12 January</span></h3>\n')):
                        line_flag = 1
                    if(line_flag == 1):
                        file_data = file_data + line
                    
                else:
                    if(line_flag == 2 and (line == '<h3><span class="mw-headline" id="' + str(i+1) + '_' + month_caps[month] + '">' + str(i+1) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+3) + '" title="Edit section: ' + str(i+1) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n') or line == '<h2><span class="mw-headline" id="Summary">Summary</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+3) + '" title="Edit section: Summary">edit</a><span class="mw-editsection-bracket">]</span></span></h2>\n'):
                        line_flag = 0
                        break
                    if(line_flag == 1 and (line == '<h2><span class="mw-headline" id="Summary">Summary</span></h2>\n' or line == '<h3><span class="mw-headline" id="' + str(i+1) + '_' + month_caps[month] + '">' + str(i+1) + ' ' + month_caps[month] + '</span></h3>\n')):
                        line_flag = 0
                        break
                    if(line == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span></h3>\n')):
                        line_flag = 1
                    if(line == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Timeline_of_the_COVID-19_pandemic_in_' + month_caps[month] + '_' + year + '&amp;action=edit&amp;section=' + str(i+2) + '" title="Edit section: ' + str(i) + ' ' + month_caps[month] + '">edit</a><span class="mw-editsection-bracket">]</span></span></h3>\n')):
                        line_flag = 2
                    if(line_flag == 1 or line_flag == 2):
                        file_data = file_data + line
                    
            file.close()
            if(i<10):
                wiki_timeline['0'+str(i)+'-'+month+'-'+year] = file_data
            else:
                wiki_timeline[str(i)+'-'+month+'-'+year] = file_data

os.remove("temp1.html")

flag = 0
cflag = 0
coflag = 0

useless_keys = []

# Removing useless charactes from the data of timeline
for timeline in wiki_timeline:
    if(wiki_timeline[timeline] == ''):
        useless_keys.append(timeline)
    else:
        world_data_updated = ""
        
        for i in wiki_timeline[timeline]:
            if(i == '<'):
                flag = 1
            elif(i == '#'):
                coflag = 1
            elif(i == '['):
                cflag = 1
            elif(flag == 0 and coflag == 0 and cflag == 0):
                if(re.findall("[#$\"\'\@\%\!\&\*\/\(\)\=\_\;\:]", i)):
                    i = " "
                world_data_updated += i
            elif(i == ']'):
                cflag = 0
            elif(i == ';'):
                coflag = 0
            elif(i == '>'):
                flag = 0
        
        wiki_timeline[timeline] = world_data_updated

# Removing useless keys (keys having no data)
for i in useless_keys:
    del wiki_timeline[i]

valid_dates = list(wiki_timeline.keys())

# Main URL for Response part
main_response_url = "https://en.wikipedia.org/wiki/Responses_to_the_COVID-19_pandemic_in_"

wiki_response = {}

count = 0

# Extracting Data from Response File
for year in year_caps:
    for month in month_caps:
        if(year == '2019'):
            continue
        if(year == '2022' and month == '04'):
            break
        url = main_response_url + month_caps[month] + '_' + year
        
        request = urllib.request.Request(url,None,headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        
        file = open('temp2.html', 'wb')
        file.write(data)
        file.close()
        
        for i in range(1, 32):
            
            line_flag = 0
            file = open('temp2.html', 'r')
            file_data = ''
            count_response = 1
            for line in file:
                if(line_flag == 1 and (line[:34] == '<h2><span class="mw-headline" id="') or line[:34] == '<h3><span class="mw-headline" id="'):
                    line_flag = 0
                if(count_response <= 1):
                    if(i<10):
                        str_length = 47 + (2*len(month_caps[month]))
                        if(line[:str_length] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span>')):
                            line_flag = 1
                            count_response += 1
                            
                    else:
                        str_length = 49 + (2*len(month_caps[month]))
                        if(line[:str_length] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '">' + str(i) + ' ' + month_caps[month] + '</span>')):
                            line_flag = 1
                            count_response += 1
                            
                else:
                    if(i<10):
                        str_length = 49 + (2*len(month_caps[month]))
                        if(line[:str_length] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '_' + str(count_response) + '">' + str(i) + ' ' + month_caps[month] + '</span>') or line[:66] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '_' + str(count_response) + '">' + str(i) + ' ' + month_caps[month] + '</span>')):
                            line_flag = 1
                            count_response += 1
                            
                    else:
                        str_length = 51 + (2*len(month_caps[month]))
                        if(line[:str_length] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '_' + str(count_response) + '">' + str(i) + ' ' + month_caps[month] + '</span>') or line[:68] == ('<h3><span class="mw-headline" id="' + str(i) + '_' + month_caps[month] + '_' + str(count_response) + '">' + str(i) + ' ' + month_caps[month] + '</span>')):
                            line_flag = 1
                            count_response += 1
                            
                if(line_flag == 1):
                    file_data = file_data + line
            file.close()
            if(i<10):
                wiki_response['0'+str(i)+'-'+month+'-'+year] = file_data
            else:
                wiki_response[str(i)+'-'+month+'-'+year] = file_data
            

os.remove("temp2.html")

flag = 0
cflag = 0
coflag = 0

# Set containing all the stop words
stop_words = set(stopwords.words('english'))

# Storing covid words input list and dictionary
covid_word_list = []
covid_word_dict = {}
file = open('covid_word_dictionary.txt', 'r')
covid_data_list = file.read()
for line in covid_data_list.split('\n'):
    for word in line.split():
        if word.lower() not in stop_words:
            covid_word_list.append(word)
            if word in covid_word_dict:
                covid_word_dict[word] += 1
            else:
                covid_word_dict[word] = 1

file.close()

useless_keys = []

# Removing useless characters from response data
for response in wiki_response:
    if(wiki_response[response] == ''):
        useless_keys.append(response)
    else:
        world_data_updated = ""
        
        for i in wiki_response[response]:
            if(i == '<'):
                flag = 1
            elif(i == '#'):
                coflag = 1
            elif(i == '['):
                cflag = 1
            elif(flag == 0 and coflag == 0 and cflag == 0):
                if(re.findall("[#$\"\'\@\%\!\&\*\/\(\)\=\_\;\:]", i)):
                    i = " "
                world_data_updated += i
            elif(i == ']'):
                cflag = 0
            elif(i == ';'):
                coflag = 0
            elif(i == '>'):
                flag = 0

        wiki_response[response] = world_data_updated

# Dictionary containing all the valid URL's of the country
url_dictionary = {
                    'Argentina':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Argentina'], 
                    'Australia':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(January%E2%80%93June_2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(July%E2%80%93December_2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2022)'], 
                    'Bangladesh':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Bangladesh'], 
                    'Brazil':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Brazil'], 
                    'Canada':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Canada'], 
                    'Ghana':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Ghana_(March%E2%80%93July_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Ghana_(August%E2%80%93December_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Ghana_(2021)'], 
                    'India':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(January%E2%80%93May_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(June%E2%80%93December_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_India_(2021)'], 
                    'Indonesia':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Indonesia_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Indonesia_(2021)'], 
                    'Ireland':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(January%E2%80%93June_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(July%E2%80%93December_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(January%E2%80%93June_2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(July%E2%80%93December_2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Republic_of_Ireland_(2022)'], 
                    'Malaysia':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2022)'], 
                    'Mexico':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Mexico'], 
                    'New Zealand':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_New_Zealand_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_New_Zealand_(2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_New_Zealand_(2022)'], 
                    'Nigeria':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nigeria_(February%E2%80%93June_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nigeria_(July%E2%80%93December_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Nigeria_(January%E2%80%93June_2021)'], 
                    'Pakistan':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Pakistan'], 
                    'Philippines':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Philippines_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Philippines_(2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_Philippines_(2022)'], 
                    'Russia':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Russia_(January%E2%80%93June_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Russia_(July%E2%80%93December_2020)'], 
                    'Singapore':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore_(2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore_(2022)'], 
                    'South Africa':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_South_Africa'], 
                    'Spain':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Spain'], 
                    'Turkey':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Turkey'], 
                    'England':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(January%E2%80%93June_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(July%E2%80%93December_2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(2021)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_England_(2022)'], 
                    'United States':['https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_United_States_(2020)', 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_the_United_States_(2021)']
                }

# List of country
country_news_list = ['Argentina', 'Australia', 'Bangladesh', 'Brazil', 'Canada', 'Ghana', 'India', 'Indonesia', 'Ireland', 'Malaysia', 'Mexico', 'New Zealand', 'Nigeria', 'Pakistan', 'Philippines', 'Russia', 'Singapore', 'South Africa', 'Spain', 'Turkey', 'England', 'United States']

# Downloading all the country files
for country in country_news_list:
    count_url = 0
    country_final_range = []
    for url in url_dictionary[country]:
        country_up = country.replace(" ", "_")

        request=urllib.request.Request(url,None,headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        file = open('wiki_'+ country_up+ '_' + str(count_url) +'.html','wb')
        file.write(data)
        file.close()

        count_url += 1

# Refining data of all the country files, to reduce the execution time
for country in country_news_list:
    count_url = 0
    country_final_range = []
    country_complete_final_data = ""
    for url in url_dictionary[country]:
        country_up = country.replace(" ", "_")
        file = open('wiki_'+ country_up+ '_' + str(count_url) +'.html', 'r')
        country_complete_data = file.read()
        file.close()

        if(country_up == 'Australia' or country_up == 'Brazil' or country_up == 'India' or country_up == 'Indonesia' or country_up == 'Mexico' or country_up == 'Pakistan' or country_up == 'Spain' or country_up == 'Turkey'):
            final_data_flag = 0
            for line in country_complete_data.split('\n'):
                if(line[:34] == '<h2><span class="mw-headline" id="'):
                    final_data_flag = 1
                if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                    final_data_flag = 0
                    break
                if(final_data_flag == 1):
                    country_complete_final_data = country_complete_final_data + '\n' + line
        
        elif(country_up == 'Canada'):
            final_data_flag = 0
            for line in country_complete_data.split('\n'):
                if(line[:42] == '<h2><span class="mw-headline" id="Graphs">'):
                    final_data_flag = 1
                if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                    final_data_flag = 0
                    break
                if(final_data_flag == 1):
                    country_complete_final_data = country_complete_final_data + '\n' + line
        
        elif(country_up == 'Singapore'):
            final_data_flag = 0
            if(count_url == 2):
                for line in country_complete_data.split('\n'):
                    if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                        final_data_flag = 0
                        break
                    if(line[:34] == '<h2><span class="mw-headline" id="'):
                        line = line.replace('<h2><span class="mw-headline" id="', '<h3><span class="mw-headline" id="')
                        final_data_flag = 1
                    if(final_data_flag == 1):
                        country_complete_final_data = country_complete_final_data + '\n' + line
            else:
                for line in country_complete_data.split('\n'):
                    if(line[:34] == '<h3><span class="mw-headline" id="'):
                        final_data_flag = 1
                    if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                        final_data_flag = 0
                        break
                    if(final_data_flag == 1):
                        country_complete_final_data = country_complete_final_data + '\n' + line
        
        elif(country_up == 'United_States'):
            final_data_flag = 0
            if(count_url == 0):
                for line in country_complete_data.split('\n'):
                    if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                        final_data_flag = 0
                        break
                    if(line[:51] == '<h3><span id="January_1.E2.80.9320.2C_2020"></span>'):
                        final_data_flag = 1
                    if(final_data_flag == 1):
                        country_complete_final_data = country_complete_final_data + '\n' + line
            else:
                for line in country_complete_data.split('\n'):
                    if(line[:34] == '<h3><span class="mw-headline" id="'):
                        final_data_flag = 1
                    if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                        final_data_flag = 0
                        break
                    if(final_data_flag == 1):
                        country_complete_final_data = country_complete_final_data + '\n' + line

        elif(country_up == 'New_Zealand'):
            final_data_flag = 0
            for line in country_complete_data.split('\n'):
                if(line[:34] == '<h3><span class="mw-headline" id="' or line[:38] == '</p><h3><span class="mw-headline" id="'):
                    final_data_flag = 1
                if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                    final_data_flag = 0
                    break
                if(final_data_flag == 1):
                    country_complete_final_data = country_complete_final_data + '\n' + line
        
        elif(country_up == 'Russia'):
            final_data_flag = 0
            for line in country_complete_data.split('\n'):
                if(line[:34] == '<h3><span class="mw-headline" id="' or line[:105] == '<h3><span id="January.E2.80.93February_2020"></span><span class="mw-headline" id="January–February_2020">'):
                    final_data_flag = 1
                if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                    final_data_flag = 0
                    break
                if(final_data_flag == 1):
                    country_complete_final_data = country_complete_final_data + '\n' + line
        
        else:
            
            final_data_flag = 0
            for line in country_complete_data.split('\n'):
                if(line[:34] == '<h3><span class="mw-headline" id="'):
                    final_data_flag = 1
                if(line[:63] == '<h2><span class="mw-headline" id="References">References</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>' or line[:59] == '<h2><span class="mw-headline" id="See_also">See also</span>' or line[:53] == '<h2><span class="mw-headline" id="Notes">Notes</span>'):
                    final_data_flag = 0
                    break
                if(final_data_flag == 1):
                    country_complete_final_data = country_complete_final_data + '\n' + line

        count_url += 1
        file = open('wiki_'+ country_up +'.html', 'w')
        file.write(country_complete_final_data[1:])
        file.close()

# Valid Range of NEWS for all the countries
country_news_range = {}

# Formining Dictionary to store the Valid Ranges of Country
for country in country_news_list:
    count_url = 0
    country_final_range = []
    country_up = country.replace(" ", "_")
    file = open('wiki_'+ country_up +'.html', 'r')
    country_complete_data = file.read()
    file.close()

    if(country_up == 'Australia' or country_up == 'Brazil' or country_up == 'India' or country_up == 'Indonesia' or country_up == 'Mexico' or country_up == 'Pakistan' or country_up == 'Spain' or country_up == 'Turkey'):
        country_semi_final_range = country_range2(country_complete_data)
    else:
        country_semi_final_range = country_range1(country_complete_data)
    
    country_final_range = country_final_range + country_semi_final_range
    
    country_news_range[country] = []
    if(country == 'United States'):
        country_news_range[country].append('January' + '_2020')
        country_news_range[country].append(country_final_range[-1] + '_2021')
    elif(country == 'Russia'):
        country_news_range[country].append('January' + '_2020')
        country_news_range[country].append(country_final_range[-4])
    elif(country == 'Canada'):
        country_news_range[country].append(country_final_range[0] + '_2019')
        country_news_range[country].append(country_final_range[-1] + '021')
    else:
        if(country == 'Australia' or country == 'New Zealand'):
            country_news_range[country].append(country_final_range[0])
            country_news_range[country].append(country_final_range[-1] + '_2022')
        elif(country == 'Bangladesh' or country == 'Spain'):
            country_news_range[country].append(country_final_range[0] + '_2020')
            country_news_range[country].append(country_final_range[-1] + '_2020')
        elif(country == 'India' or country == 'Indonesia' or country == 'Nigeria'):
            country_news_range[country].append(country_final_range[0] + '_2020')
            country_news_range[country].append(country_final_range[-1] + '_2021')
        elif(country == 'Malaysia' or country == 'Philippines' or country == 'Singapore'):
            country_news_range[country].append(country_final_range[0] + '_2020')
            country_news_range[country].append(country_final_range[-1] + '_2022')
        else:
            country_news_range[country].append(country_final_range[0])
            country_news_range[country].append(country_final_range[-1])

year_year = ['2019', '2020', '2021', '2022']
month_to_month = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
mon_to_mon = {'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}

# Extracting Data of all the countries from there files
all_country_news = {}
for country in country_news_list:
    country_up = country.replace(" ", "_")
    indi_country_news = {}
    if(country == 'Argentina'):
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        date_flag = 0
        news_flag = 0
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            if(line[:6] == '<p>On ' or line[:7] == '<li><b>' or line[:11] == '<ul><li><b>'):
                date_flag = 1
                news_flag = 1
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        # indi_country_news[date] = ''
                        break
                    elif(i == '<'):
                        date_flag = 0
                    elif(i == '>'):
                        date_flag = 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i

            if(line == '</p>' or line[-20:] == '</a></sup></li></ul>' or line[-15:] == '</a></sup></li>'):
                news_flag = 0
                if(date == ''):
                    continue
                if(date[:3] == 'On '):
                    date = date[3:]
                
                day, month = date.split(' ')
                if(day == 'February'):
                    day, month = month, day
                if(len(day) == 1):
                    day = '0' + day
                if(month in month_to_month):
                    month = month_to_month[month]
                if(month == '01'):
                    date = day+'-'+month+'-2021'
                else:
                    date = day+'-'+month+'-2020'
                if(date in indi_country_news):
                    indi_country_news[date] += news
                else:
                    indi_country_news[date] = news
                date = ''
                news = ''
        all_country_news[country] = indi_country_news
    
    elif(country == 'Australia'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("<\/p><p>By\s[0-9\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                space_count = 0
                # print(date)
                if(date == '2January'):
                    date = '2 January'
                elif(date == '29January 2021'):
                    date = '29 January'
                elif(date[:9] == '29April a'):
                    date = '29 April'
                elif(date[:11] == '2829 August'):
                    date = '28 August'
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                # print(date)
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if(month == '01' and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                # print(date, prev_date)
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
        
    elif(country == 'Bangladesh'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 ' 
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("<\/p><p>By\s[0-9\s]+", line) or re.findall("<ul><li>As\sof\s", line)  or re.findall("<h4><span\sclass=\"mw-headline\"\sid=\"[0-9]+", line)):
                
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                elif(date[:6] == 'As of '):
                    date = date[6:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                    if(len(day) == 1):
                        day = '0' + day
                    
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if(month == '01' and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]

                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Brazil'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("<\/p><p>By\s[0-9\s]+", line) or re.findall("<ul><li><b>[0-9\s]+", line) or re.findall("<li><b>[0-9\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        indi_country_news['26-02-2021'] += ' ' + indi_country_news['26-02-2021_2']
        del indi_country_news['26-02-2021_2']
        all_country_news[country] = indi_country_news
    
    elif(country == 'Canada'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[A-Za-z\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[A-Za-z\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                # print(date)
                if(date != ''):
                    day, month = date.split(' ')

                    if(re.findall("[A-Za-z]+", day) and re.findall("[0-9]+", month)):
                        day, month = month, day
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                # print(date, prev_date)
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Ghana'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<li>On\s<b>[0-9\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news

    
    elif(country == 'India'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<ul><li><b>On\s[0-9\s]+", line) or re.findall("<li><b>On\s[0-9\s]+", line) or re.findall('<h3><span\sclass="mw-headline"\sid="', line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                # print(date)
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h2><span class="mw-headline" id="'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Indonesia'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<li>On\s<b>[0-9\s]+", line) or re.findall("<li>[0-9\s]+[JFMASOND][a-z]+", line) or re.findall("<ul><li>[0-9\s]+[JFMASOND][a-z]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news

    elif(country == 'Ireland'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<li>On\s<b>[0-9\s]+", line) or re.findall("<li>[0-9\s]+[JFMASOND][a-z]+", line) or re.findall("<ul><li>[0-9\s]+[JFMASOND][a-z]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Malaysia'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 ' 
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("<\/p><p>By\s[0-9\s]+", line) or re.findall("<ul><li>As\sof\s", line)  or re.findall("<h4><span\sclass=\"mw-headline\"\sid=\"[0-9]+", line)):
                
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                elif(date[:6] == 'As of '):
                    date = date[6:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                    if(len(day) == 1):
                        day = '0' + day
                    
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month == '02') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]

                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[:6] == '<table'):
                    date_flag = 0
                else:
                    for i in line:
                        if(i == ',' or i == ':'):
                            date_flag = 0
                            break
                        elif(i == '<'):
                            date_flag -= 1
                        elif(i == '>'):
                            date_flag += 1
                        else:
                            if(date_flag == 1):
                                if(re.findall("[a-zA-Z0-9\s]+", i)):
                                    date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Mexico'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 ' 
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>On\s[A-Za-z\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[A-Za-z\s]+", line) or re.findall("<ul><li>As\sof\s", line)):
                
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                elif(date[:6] == 'As of '):
                    date = date[6:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                    
                    if(day in month_to_month):
                        day, month = month, day
                    
                    if(len(day) == 1):
                        day = '0' + day
                    
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month == '02') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]

                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1
            
            if(date_flag == 1):
                if(line[:6] == '<table'):
                    date_flag = 0
                else:
                    for i in line:
                        if(i == ',' or i == ':'):
                            date_flag = 0
                            break
                        elif(i == '<'):
                            date_flag -= 1
                        elif(i == '>'):
                            date_flag += 1
                        else:
                            if(date_flag == 1):
                                if(re.findall("[a-zA-Z0-9\s]+", i)):
                                    date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'New Zealand'):
        start_year = country_news_range[country][0][-4:]
        end_year = country_news_range[country][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 ' 
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<p>By\s[0-9\s]+", line) or re.findall("\<\/p\>\<p\>On\s[0-9\s]+", line) or re.findall("<\/p><p>By\s[0-9\s]+", line) or re.findall("<ul><li>As\sof\s", line)  or re.findall("<h4><span\sclass=\"mw-headline\"\sid=\"[0-9]+", line)):
                
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                elif(date[:6] == 'As of '):
                    date = date[6:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                    if(len(day) == 1):
                        day = '0' + day
                    
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month == '02') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]

                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[:6] == '<table'):
                    date_flag = 0
                else:
                    for i in line:
                        if(i == ',' or i == ':'):
                            date_flag = 0
                            break
                        elif(i == '<'):
                            date_flag -= 1
                        elif(i == '>'):
                            date_flag += 1
                        else:
                            if(date_flag == 1):
                                if(re.findall("[a-zA-Z0-9\s]+", i)):
                                    date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Nigeria'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<li>On\s<b>[0-9\s]+", line) or re.findall("<li>[0-9\s]+[JFMASOND][a-z]+", line) or re.findall("<ul><li>[0-9\s]+[JFMASOND][a-z]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Pakistan'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>Onn 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>Onn\s[0-9\s]+", line) or re.findall("<h3><span\sclass=\"mw-headline\"\sid=\"", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Philippines'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            # print(line)
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<li>On\s<b>[A-Za-z\s]+", line) or re.findall("<li>Oc[a-z]+\s[0-9]+\s", line) or re.findall("<li>[JFMASND][a-z]+\s[0-9]+\s", line) or re.findall("<ul><li>[JFMASOND][a-z]+\s[0-9]+\s", line)):
                # print(line)
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1
            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Russia'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("</p><p>On\s[0-9\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1
            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h3><span class="mw-headline" id="'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news

    elif(country == 'Singapore'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<ul><li><b>[0-9\s]+", line) or re.findall("<li><b>[0-9\s]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                # print(date)
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1
            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h2><span class="mw-headline" id="' or line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'South Africa'):
        start_year = country_news_range[country][0][-4:]
        end_year = country_news_range[country][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("</p><p>As\sof\s[0-9\s]+", line) or re.findall("</p><p>By\s[0-9\s]+", line) or re.findall("</p><p>On\s[0-9\s]+", line) or re.findall("<p>On\sthe\s[0-9\s]+", line)):
                # print(date)
                if(date[:7] == 'On the '):
                    date = date[7:]
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                if(date[:6] == 'As of '):
                    date = date[6:]
                # print(date)
                if(re.findall("[0-9][0-9]th", date) or re.findall("[0-9][0-9]st", date)):
                    if(date[:2] == '31'):
                        date = date[:2] + ' ' + '01'
                    else:
                        date = date[:2] + ' ' + prev_date[3:5]
                # print(date)
                # print()

                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                # print(date)
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1
            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h2><span class="mw-headline" id="' or line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Spain'):
        start_year = country_news_range[country][0][-4:]
        end_year = country_news_range[country][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("</p><p>On\s[0-9\s]+", line) or re.findall("<p>On\sthe\s[0-9\s]+", line) or re.findall("<dl><dt>", line) or re.findall("<p><b>", line)):
                if(date[:7] == 'On the '):
                    date = date[7:]
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                if(date[:6] == 'As of '):
                    date = date[6:]

                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h2><span class="mw-headline" id="' or line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'Turkey'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>Onn 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>Onn\s[0-9\s]+", line) or re.findall("<h3><span\sclass=\"mw-headline\"\sid=\"", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')

                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            
            if(date_flag == 1):
                if(line[0] == ' '):
                    date_flag = 0
                    break
                for i in line:
                    if(i == ',' or i == ':' or i == '–'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                for i in line:
                    if(i == '<'):
                        news_flag -= 1
                    elif(i == '>'):
                        news_flag += 1
                    else:
                        if(news_flag == 1):
                            if(i == '[' or i == ']'):
                                news = news + ' '
                            else:
                                news = news + i
        
        all_country_news[country] = indi_country_news
    
    elif(country == 'England'):
        start_year = country_news_range[country_up][0][-4:]
        end_year = country_news_range[country_up][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("<ul><li>[0-9\s]+[A-Z][a-z]+", line) or re.findall("<li>[0-9\-\s]+[A-Z][a-z]+", line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                if(date[:10] == '1013 March'):
                    date = '10 March'
                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h3><span class="mw-headline" id="' or line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        indi_country_news['30-11-2021'] += indi_country_news['30-11-2021_2']
        del indi_country_news['30-11-2021_2']
        all_country_news[country] = indi_country_news
    
    elif(country == 'United States'):
        start_year = country_news_range[country][0][-4:]
        end_year = country_news_range[country][1][-4:]
        start_year_ind = year_year.index(start_year)
        end_year_ind = year_year.index(end_year)
        index_of_year = start_year_ind
        temp_year_flag = 0
        
        file = open('wiki_' + country_up + '.html', 'r')
        country_complete_data = file.read()
        file.close()
        garbage_list = re.findall('&#[0-9]+;[0-9]+&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        garbage_list = re.findall('&#[0-9]+;', country_complete_data)
        for i in garbage_list:
            country_complete_data = country_complete_data.replace(i, '')
        del garbage_list
        country_complete_data = country_complete_data.replace('\n', ' \n')
        country_complete_data = country_complete_data + '\n<p>On 00 '
        date_flag = 0
        news_flag = 0
        prev_date = ''
        date = ''
        news = ''
        for line in country_complete_data.split('\n'):
            
            if(re.findall("<p>On\s[0-9\s]+", line) or re.findall("</p><p>On\s[JFMASOND][a-z]+\s[0-9]+", line) or re.findall("</p><p>By\s[JFMASOND][a-z]+\s[0-9]+", line) or re.findall("<p>On\s[JFMASOND][a-z]+\s[0-9]+", line) or re.findall("</p><p>As\sof\s[JFMASOND][a-z]+\s[0-9]+", line) or re.findall('<h4><span\sclass="mw-headline"\sid="[JFMASOND][a-z]+\_[0-9]+', line)):
                if(date[:3] == 'On ' or date[:3] == 'By '):
                    date = date[3:]
                
                if(date[:6] == 'As of '):
                    date = date[6:]

                space_count = 0
                
                if(date != ''):
                    for i in range(len(date)):
                        if(date[i] == ' '):
                            space_count += 1
                            if(space_count >= 2):
                                date = date[:i]
                                break
                
                if(date != ''):
                    day, month = date.split(' ')
                    if(day in month_to_month):
                        day, month = month, day
                    if(len(day) == 1):
                        day = '0' + day
                    if(month in month_to_month):
                        month = month_to_month[month]
                    if((month == '01' or month=='02' or month=='03') and temp_year_flag == 1):
                        index_of_year += 1
                        temp_year_flag = 0
                    if(month == '08' or month == '09' or month == '10' or month == '11' or month == '12'):
                        temp_year_flag = 1
                    
                    date = day+'-'+month+'-'+year_year[index_of_year]
                
                if(date == prev_date and date != ''):
                    same_date_flag = 1
                    if(date != ''):
                        for i in range(9, 1, -1):
                            date = date + '_' + str(i)
                            if(date in indi_country_news):
                                indi_country_news[date] += ' ' + news
                                same_date_flag = 0
                                break
                            else:
                                date = date[:-2]
                        if(same_date_flag == 1):
                            indi_country_news[date] += ' ' + news
                elif(date in indi_country_news):
                    for i in range(2,10):
                        date = date + '_' + str(i)
                        if(date not in indi_country_news):
                            indi_country_news[date] = news
                            break
                        else:
                            date = date[:-2]
                else:
                    if(date != ''):
                        indi_country_news[date] = news
                if('_' in date):
                    prev_date = date[:-2]
                else:
                    prev_date = date
                date = ''
                news = ''
                date_flag = 1
                news_flag = 1

            if(date_flag == 1):
                for i in line:
                    if(i == ',' or i == ':'):
                        date_flag = 0
                        break
                    elif(i == '<'):
                        date_flag -= 1
                    elif(i == '>'):
                        date_flag += 1
                    else:
                        if(date_flag == 1):
                            if(re.findall("[a-zA-Z0-9\s]+", i)):
                                date = date + i
                    
                    
            if(news_flag == 1):
                if(line[:34] == '<h3><span class="mw-headline" id="' or line[:6] == '<table'):
                    news_flag = 0
                else:
                    for i in line:
                        if(i == '<'):
                            news_flag -= 1
                        elif(i == '>'):
                            news_flag += 1
                        else:
                            if(news_flag == 1):
                                if(i == '[' or i == ']'):
                                    news = news + ' '
                                else:
                                    news = news + i
        
        all_country_news[country] = indi_country_news

print("Pre-Processing is completed!!")
print()

# Menu is created here, to access all the extracted data (Follow Instructions Written in print command)

print("################################################################################")
print("################################################################################")
print("######################## COVID Information Portal ##############################")
print("################################################################################")
print("################################################################################")

while(1):
    print()
    print("################################################################################")
    print()
    print("Please Insert the index, of the given options:")
    print("0: Data Regarding COVID-19")
    print("1: NEWS Regarding COVID-19")
    print()
    print("Insert -1 to exit")
    print()

    try:
        covid_type = int(input())
    except ValueError:
        print('Please give valid input!!')
        print()
        continue

    if(covid_type == 0):
        # print("Assignment 4 add here")
        covid_worldometer_data()
    elif(covid_type == 1):
        print("################################################################################")
        print("################################################################################")
        print("############################### COVID  NEWS ####################################")
        print("################################################################################")
        print("################################################################################")
        print()
        while(1):
            print("################################################################################")
            print()
            print("COVID-19 Related NEWS!!")
            print()
            print("Please Select the News type:")
            print("0: Timeline")
            print("1: Responses")
            print("2: Country wise NEWS")
            print()
            print("Insert -1 to go back")
            print()

            try:
                news_type = int(input())
            except ValueError:
                print('Please give valid input!!')
                print()
                continue

            if(news_type == 0):
                while(1):
                    print()
                    print("################################################################################")
                    print()
                    print("Timeline!!")
                    print()
                    print("Please Select the Options from Timeline type:")
                    print("0: Get NEWS of given Timeline")
                    print("1: Compare 2 Timelines")
                    print()
                    print("Insert -1 to go back")
                    print()

                    try:
                        timeline_type = int(input())
                    except ValueError:
                        print('Please give valid input!!')
                        print()
                        continue

                    if(timeline_type == 0):
                        print('Please Insert Start Date (in dd-mm-yyyy format):')
                        start_date_timeline = input()
                        print('Please Insert End Date (in dd-mm-yyyy format):')
                        end_date_timeline = input()
                        print()
                        total_timeline_data = ''
                        try:
                            start_date_timeline_index = valid_dates.index(start_date_timeline)
                        except ValueError:
                            print('Start Date is Not Valid')
                            continue
                        try:
                            end_date_timeline_index = valid_dates.index(end_date_timeline)
                        except ValueError:
                            print('End Date is Not Valid')
                            continue
                        if(start_date_timeline_index == end_date_timeline_index):
                            print('Please Enter Different Dates')
                        elif(start_date_timeline_index > end_date_timeline_index):
                            print('Start date should come before End date')
                        else:
                            for i in range(start_date_timeline_index, end_date_timeline_index+1):
                                if(wiki_timeline[valid_dates[i]] != ''):
                                    total_timeline_data = total_timeline_data + wiki_timeline[valid_dates[i]]

                            word_tokens_timeline = word_tokenize(total_timeline_data)
                            filtered_sentence_timeline = {}
                            
                            if(len(total_timeline_data) == 0):
                                print("Insufficient Data to Display")
                            else:
                                print(total_timeline_data)
                            
                            world_final_timeline = []
                            for w in word_tokens_timeline:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_timeline):
                                            filtered_sentence_timeline[w] += 1
                                        else:
                                            filtered_sentence_timeline[w] = 1
                                        world_final_timeline.append(w)
                            
                            print("Word Cloud of timeline for given range:")

                            if(len(filtered_sentence_timeline) == 0):
                                print("Insufficient Data to plot a word cloud")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(filtered_sentence_timeline)

                            plt.figure(figsize = (8, 8), facecolor = None)
                            plt.imshow(wordcloud)
                            plt.axis("off")
                            plt.tight_layout(pad = 0)
                            plt.show()
                            
                    elif(timeline_type == 1):
                        print()
                        print('Please Insert Start Date for Range 1 (in dd-mm-yyyy format):')
                        start_date_timeline_r1 = input()
                        print('Please Insert End Date for Range 1 (in dd-mm-yyyy format):')
                        end_date_timeline_r1 = input()
                        print('Please Insert Start Date for Range 2 (in dd-mm-yyyy format):')
                        start_date_timeline_r2 = input()
                        print('Please Insert End Date for Range 2 (in dd-mm-yyyy format):')
                        end_date_timeline_r2 = input()
                        print()
                        total_timeline_data_r1 = ''
                        total_timeline_data_r2 = ''
                        try:
                            start_date_timeline_index_r1 = valid_dates.index(start_date_timeline_r1)
                        except ValueError:
                            print('Start Date of range 1 is Not Valid')
                            continue
                        try:
                            end_date_timeline_index_r1 = valid_dates.index(end_date_timeline_r1)
                        except ValueError:
                            print('End Date of range 1 is Not Valid')
                            continue
                        try:
                            start_date_timeline_index_r2 = valid_dates.index(start_date_timeline_r2)
                        except ValueError:
                            print('Start Date of range 2 is Not Valid')
                            continue
                        try:
                            end_date_timeline_index_r2 = valid_dates.index(end_date_timeline_r2)
                        except ValueError:
                            print('End Date of range 2 is Not Valid')
                            continue
                        if(start_date_timeline_index_r1 == end_date_timeline_index_r1):
                            print('Please Enter Different Dates in range 1')
                        elif(start_date_timeline_index_r1 > end_date_timeline_index_r1):
                            print('Start date should come before End date for range 1')
                        elif(start_date_timeline_index_r2 == end_date_timeline_index_r2):
                            print('Please Enter Different Dates in range 2')
                        elif(start_date_timeline_index_r2 > end_date_timeline_index_r2):
                            print('Start date should come before End date for range 2')
                        elif(end_date_timeline_index_r1 > start_date_timeline_index_r2 and start_date_timeline_index_r1 < start_date_timeline_index_r2):
                            print("Given ranges are Overlapping!!")
                        elif(end_date_timeline_index_r2 > start_date_timeline_index_r1 and start_date_timeline_index_r2 < start_date_timeline_index_r1):
                            print("Given ranges are Overlapping!!")
                        else:
                            for i in range(start_date_timeline_index_r1, end_date_timeline_index_r1+1):
                                total_timeline_data_r1 = total_timeline_data_r1 + ' ' +wiki_timeline[valid_dates[i]]
                            total_timeline_data_r1 = total_timeline_data_r1.lower()

                            for i in range(start_date_timeline_index_r2, end_date_timeline_index_r2+1):
                                total_timeline_data_r2 = total_timeline_data_r2 + ' ' + wiki_timeline[valid_dates[i]]
                            total_timeline_data_r2 = total_timeline_data_r2.lower()

                            word_tokens_timeline_r1 = word_tokenize(total_timeline_data_r1)
                            filtered_sentence_timeline_r1 = {}

                            word_tokens_timeline_r2 = word_tokenize(total_timeline_data_r2)
                            filtered_sentence_timeline_r2 = {}

                            world_final_timeline_r1 = []
                            world_final_timeline_r2 = []

                            for w in word_tokens_timeline_r1:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_timeline_r1):
                                            filtered_sentence_timeline_r1[w] += 1
                                        else:
                                            filtered_sentence_timeline_r1[w] = 1
                                        world_final_timeline_r1.append(w)
                            
                            for w in word_tokens_timeline_r2:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_timeline_r2):
                                            filtered_sentence_timeline_r2[w] += 1
                                        else:
                                            filtered_sentence_timeline_r2[w] = 1
                                        world_final_timeline_r2.append(w)
                            
                            common_words_time_line = []
                            common_words_time_line_dict = {}
                            covid_common_words_time_line = []
                            covid_common_words_time_line_dict = {}

                            common_words_time_line = list(set(world_final_timeline_r1) & set(world_final_timeline_r2))
                            covid_common_words_time_line = list(set(common_words_time_line) & set(covid_word_list))
                            
                            for i in common_words_time_line:
                                if(filtered_sentence_timeline_r1[i] < filtered_sentence_timeline_r2[i]):
                                    common_words_time_line_dict[i] = filtered_sentence_timeline_r1[i]
                                else:
                                    common_words_time_line_dict[i] = filtered_sentence_timeline_r2[i]

                            for i in covid_common_words_time_line:
                                if(common_words_time_line_dict[i] < covid_word_dict[i]):
                                    covid_common_words_time_line_dict[i] = common_words_time_line_dict[i]
                                else:
                                    covid_common_words_time_line_dict[i] = covid_word_dict[i]

                            print()
                            print("Percentage of covid related words in common words:", ((len(list(set(covid_common_words_time_line)))/(len(list(set(common_words_time_line))) + 0.0001))*100))
                            print()
                            print('Word Cloud for ALL the common words:')
                            
                            if(len(common_words_time_line) == 0):
                                print("Insufficiant Data to plot a word cloud!!")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(common_words_time_line_dict)

                                plt.figure(figsize = (8, 8), facecolor = None)
                                plt.imshow(wordcloud)
                                plt.title('All Common Words')
                                # plt.axis("off")
                                plt.tight_layout(pad = 0)
                                plt.show()

                            print()
                            print('Word Cloud for ONLY Covid related common words:')

                            if(len(covid_common_words_time_line) == 0):
                                print("Insufficiant Data to plot a word cloud!!")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(covid_common_words_time_line_dict)

                                plt.figure(figsize = (8, 8), facecolor = None)
                                plt.imshow(wordcloud)
                                plt.title('Covid Related Common Words')
                                # plt.axis("off")
                                plt.tight_layout(pad = 0)
                                plt.show()
                            
                            print()
                            print('Top common words in this range are:')
                            sorted_all_common_timeline = sorted(common_words_time_line_dict.items(), key = lambda kv:(kv[1], kv[0]))

                            if(len(sorted_all_common_timeline) >= 20):
                                for i in range(-1, -21, -1):
                                    print(sorted_all_common_timeline[i][0])
                            elif(len(sorted_all_common_timeline) == 0):
                                print("Insufficient Data!!")
                            else:
                                for i in range(-1, ((len(sorted_all_common_timeline) + 1)*(-1)), -1):
                                    print(sorted_all_common_timeline[i][0])
                            print()
                            print('Top covid related common words in this range are:')
                            sorted_covid_common_timeline = sorted(covid_common_words_time_line_dict.items(), key = lambda kv:(kv[1], kv[0]))

                            if(len(sorted_covid_common_timeline) >= 20):
                                for i in range(-1, -21, -1):
                                    print(sorted_covid_common_timeline[i][0])
                            elif(len(sorted_covid_common_timeline) == 0):
                                print("Insufficient Data!!")
                            else:
                                for i in range(-1, ((len(sorted_covid_common_timeline) + 1)*(-1)), -1):
                                    print(sorted_covid_common_timeline[i][0])
                    
                    elif(timeline_type == -1):
                        break
                    else:
                        print("Input Out of Bound!!")

            elif(news_type == 1):

                while(1):
                    print()
                    print("################################################################################")
                    print()
                    print("Response!!")
                    print()
                    print("Please Select the Options from Response type:")
                    print("0: Get NEWS of given range of response")
                    print("1: Compare 2 range of responses")
                    print()
                    print("Insert -1 to go back")
                    print()

                    try:
                        response_type = int(input())
                    except ValueError:
                        print('Please give valid input!!')
                        print()
                        continue
                    
                    if(response_type == 0):
                        print('Please Insert Start Date (in dd-mm-yyyy format):')
                        start_date_response = input()
                        print('Please Insert End Date (in dd-mm-yyyy format):')
                        end_date_response = input()
                        print()
                        total_response_data = ''
                        try:
                            start_date_response_index = valid_dates.index(start_date_response)
                        except ValueError:
                            print('Start Date is Not Valid')
                            continue
                        try:
                            end_date_response_index = valid_dates.index(end_date_response)
                        except ValueError:
                            print('End Date is Not Valid')
                            continue
                        if(start_date_response_index == end_date_response_index):
                            print('Please Enter Different Dates')
                        elif(start_date_response_index > end_date_response_index):
                            print('Start date should come before End date')
                        else:
                            for i in range(start_date_response_index, end_date_response_index+1):
                                if(wiki_response[valid_dates[i]] != ''):
                                    total_response_data = total_response_data +  wiki_response[valid_dates[i]]

                            word_tokens_response = word_tokenize(total_response_data)
                            filtered_sentence_response = {}
                            
                            if(len(total_response_data) == 0):
                                print("Insufficient Data to display!!")
                            else:
                                print(total_response_data)
                            
                            world_final_response = []
                            for w in word_tokens_response:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_response):
                                            filtered_sentence_response[w] += 1
                                        else:
                                            filtered_sentence_response[w] = 1
                                        world_final_response.append(w)
                            
                            print("Word Cloud of Responses for given range:")

                            if(len(filtered_sentence_response) == 0):
                                print("Insufficient Data to Plot the Word Cloud!!")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(filtered_sentence_response)

                            plt.figure(figsize = (8, 8), facecolor = None)
                            plt.imshow(wordcloud)
                            plt.axis("off")
                            plt.tight_layout(pad = 0)
                            plt.show()
                        
                    elif(response_type == 1):
                        print()
                        print('Please Insert Start Date for Range 1 (in dd-mm-yyyy format):')
                        start_date_response_r1 = input()
                        print('Please Insert End Date for Range 1 (in dd-mm-yyyy format):')
                        end_date_response_r1 = input()
                        print('Please Insert Start Date for Range 2 (in dd-mm-yyyy format):')
                        start_date_response_r2 = input()
                        print('Please Insert End Date for Range 2 (in dd-mm-yyyy format):')
                        end_date_response_r2 = input()
                        print()
                        total_response_data_r1 = ''
                        total_response_data_r2 = ''
                        try:
                            start_date_response_index_r1 = valid_dates.index(start_date_response_r1)
                        except ValueError:
                            print('Start Date of range 1 is Not Valid')
                            continue
                        try:
                            end_date_response_index_r1 = valid_dates.index(end_date_response_r1)
                        except ValueError:
                            print('End Date of range 1 is Not Valid')
                            continue
                        try:
                            start_date_response_index_r2 = valid_dates.index(start_date_response_r2)
                        except ValueError:
                            print('Start Date of range 2 is Not Valid')
                            continue
                        try:
                            end_date_response_index_r2 = valid_dates.index(end_date_response_r2)
                        except ValueError:
                            print('End Date of range 2 is Not Valid')
                            continue
                        if(start_date_response_index_r1 == end_date_response_index_r1):
                            print('Please Enter Different Dates in range 1')
                        elif(start_date_response_index_r1 > end_date_response_index_r1):
                            print('Start date should come before End date for range 1')
                        elif(start_date_response_index_r2 == end_date_response_index_r2):
                            print('Please Enter Different Dates in range 2')
                        elif(start_date_response_index_r2 > end_date_response_index_r2):
                            print('Start date should come before End date for range 2')
                        elif(end_date_response_index_r1 > start_date_response_index_r2 and start_date_response_index_r1 < start_date_response_index_r2):
                            print("Given ranges are Overlapping!!")
                        elif(end_date_response_index_r2 > start_date_response_index_r1 and start_date_response_index_r2 < start_date_response_index_r1):
                            print("Given ranges are Overlapping!!")
                        else:
                            for i in range(start_date_response_index_r1, end_date_response_index_r1+1):
                                total_response_data_r1 = total_response_data_r1 + ' ' + wiki_response[valid_dates[i]]
                            total_response_data_r1 = total_response_data_r1.lower()

                            for i in range(start_date_response_index_r2, end_date_response_index_r2+1):
                                total_response_data_r2 = total_response_data_r2 + ' ' + wiki_response[valid_dates[i]]
                            total_response_data_r2 = total_response_data_r2.lower()

                            word_tokens_response_r1 = word_tokenize(total_response_data_r1)
                            filtered_sentence_response_r1 = {}

                            word_tokens_response_r2 = word_tokenize(total_response_data_r2)
                            filtered_sentence_response_r2 = {}

                            world_final_response_r1 = []
                            world_final_response_r2 = []

                            for w in word_tokens_response_r1:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_response_r1):
                                            filtered_sentence_response_r1[w] += 1
                                        else:
                                            filtered_sentence_response_r1[w] = 1
                                        world_final_response_r1.append(w)
                            
                            for w in word_tokens_response_r2:
                                if w.lower() not in stop_words:
                                    if(len(w) > 2):
                                        if(w in filtered_sentence_response_r2):
                                            filtered_sentence_response_r2[w] += 1
                                        else:
                                            filtered_sentence_response_r2[w] = 1
                                        world_final_response_r2.append(w)
                            
                            common_words_response = []
                            common_words_response_dict = {}
                            covid_common_words_response = []
                            covid_common_words_response_dict = {}

                            common_words_response = list(set(world_final_response_r1) & set(world_final_response_r2))
                            covid_common_words_response = list(set(common_words_response) & set(covid_word_list))
                            
                            for i in common_words_response:
                                if(filtered_sentence_response_r1[i] < filtered_sentence_response_r2[i]):
                                    common_words_response_dict[i] = filtered_sentence_response_r1[i]
                                else:
                                    common_words_response_dict[i] = filtered_sentence_response_r2[i]

                            for i in covid_common_words_response:
                                if(common_words_response_dict[i] < covid_word_dict[i]):
                                    covid_common_words_response_dict[i] = common_words_response_dict[i]
                                else:
                                    covid_common_words_response_dict[i] = covid_word_dict[i]
                            
                            print()
                            print("Percentage of covid related words in common words:", ((len(list(set(covid_common_words_response)))/(len(list(set(common_words_response))) + 0.0001 ))*100))
                            print()
                            print('Word Cloud for ALL the common words:')
                            
                            if(len(common_words_response) == 0):
                                print("Insufficiant Word to plot a word cloud!!")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(common_words_response_dict)

                                plt.figure(figsize = (8, 8), facecolor = None)
                                plt.imshow(wordcloud)
                                plt.title('All Common Words')
                                # plt.axis("off")
                                plt.tight_layout(pad = 0)
                                plt.show()

                            print()
                            print('Word Cloud for ONLY Covid related common words:')

                            if(len(covid_common_words_response) == 0):
                                print("Insufficiant Word to plot a word cloud!!")
                            else:
                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(covid_common_words_response_dict)

                                plt.figure(figsize = (8, 8), facecolor = None)
                                plt.imshow(wordcloud)
                                plt.title('Covid Related Common Words')
                                # plt.axis("off")
                                plt.tight_layout(pad = 0)
                                plt.show()
                            
                            print()
                            print('Top common words in this range are:')
                            sorted_all_common_response = sorted(common_words_response_dict.items(), key = lambda kv:(kv[1], kv[0]))

                            if(len(sorted_all_common_response) >= 20):
                                for i in range(-1, -21, -1):
                                    print(sorted_all_common_response[i][0])
                            elif(len(sorted_all_common_response) == 0):
                                print("Insufficient Data!!")
                            else:
                                for i in range(-1, ((len(sorted_all_common_response) + 1)*(-1)), -1):
                                    print(sorted_all_common_response[i][0])
                            print()
                            print('Top covid related common words in this range are:')
                            sorted_covid_common_response = sorted(covid_common_words_response_dict.items(), key = lambda kv:(kv[1], kv[0]))

                            if(len(sorted_covid_common_response) >= 20):
                                for i in range(-1, -21, -1):
                                    print(sorted_covid_common_response[i][0])
                            elif(len(sorted_covid_common_response) == 0):
                                print("Insufficient Data!!")
                            else:
                                for i in range(-1, ((len(sorted_covid_common_response) + 1)*(-1)), -1):
                                    print(sorted_covid_common_response[i][0])
                    
                    elif(response_type == -1):
                        break
                    else:
                        print("Input Out of Bound!!")
            
            elif(news_type == 2):
                valid_dates = ['01-12-2019', '02-12-2019', '03-12-2019', '04-12-2019', '05-12-2019', '06-12-2019', '07-12-2019', '08-12-2019', '09-12-2019', '10-12-2019', '11-12-2019', '12-12-2019', '13-12-2019', '14-12-2019', '15-12-2019', '16-12-2019', '17-12-2019', '18-12-2019', '19-12-2019', '20-12-2019', '21-12-2019', '22-12-2019', '23-12-2019', '24-12-2019', '25-12-2019', '26-12-2019', '27-12-2019', '28-12-2019', '29-12-2019', '30-12-2019', '31-12-2019', '01-01-2020', '02-01-2020', '03-01-2020', '04-01-2020', '05-01-2020', '06-01-2020', '07-01-2020', '08-01-2020', '09-01-2020', '10-01-2020', '11-01-2020', '12-01-2020', '13-01-2020', '14-01-2020', '15-01-2020', '16-01-2020', '17-01-2020', '18-01-2020', '19-01-2020', '20-01-2020', '21-01-2020', '22-01-2020', '23-01-2020', '24-01-2020', '25-01-2020', '26-01-2020', '27-01-2020', '28-01-2020', '29-01-2020', '30-01-2020', '31-01-2020', '01-02-2020', '02-02-2020', '03-02-2020', '04-02-2020', '05-02-2020', '06-02-2020', '07-02-2020', '08-02-2020', '09-02-2020', '10-02-2020', '11-02-2020', '12-02-2020', '13-02-2020', '14-02-2020', '15-02-2020', '16-02-2020', '17-02-2020', '18-02-2020', '19-02-2020', '20-02-2020', '21-02-2020', '22-02-2020', '23-02-2020', '24-02-2020', '25-02-2020', '26-02-2020', '27-02-2020', '28-02-2020', '29-02-2020', '01-03-2020', '02-03-2020', '03-03-2020', '04-03-2020', '05-03-2020', '06-03-2020', '07-03-2020', '08-03-2020', '09-03-2020', '10-03-2020', '11-03-2020', '12-03-2020', '13-03-2020', '14-03-2020', '15-03-2020', '16-03-2020', '17-03-2020', '18-03-2020', '19-03-2020', '20-03-2020', '21-03-2020', '22-03-2020', '23-03-2020', '24-03-2020', '25-03-2020', '26-03-2020', '27-03-2020', '28-03-2020', '29-03-2020', '30-03-2020', '31-03-2020', '01-04-2020', '02-04-2020', '03-04-2020', '04-04-2020', '05-04-2020', '06-04-2020', '07-04-2020', '08-04-2020', '09-04-2020', '10-04-2020', '11-04-2020', '12-04-2020', '13-04-2020', '14-04-2020', '15-04-2020', '16-04-2020', '17-04-2020', '18-04-2020', '19-04-2020', '20-04-2020', '21-04-2020', '22-04-2020', '23-04-2020', '24-04-2020', '25-04-2020', '26-04-2020', '27-04-2020', '28-04-2020', '29-04-2020', '30-04-2020', '01-05-2020', '02-05-2020', '03-05-2020', '04-05-2020', '05-05-2020', '06-05-2020', '07-05-2020', '08-05-2020', '09-05-2020', '10-05-2020', '11-05-2020', '12-05-2020', '13-05-2020', '14-05-2020', '15-05-2020', '16-05-2020', '17-05-2020', '18-05-2020', '19-05-2020', '20-05-2020', '21-05-2020', '22-05-2020', '23-05-2020', '24-05-2020', '25-05-2020', '26-05-2020', '27-05-2020', '28-05-2020', '29-05-2020', '30-05-2020', '31-05-2020', '01-06-2020', '02-06-2020', '03-06-2020', '04-06-2020', '05-06-2020', '06-06-2020', '07-06-2020', '08-06-2020', '09-06-2020', '10-06-2020', '11-06-2020', '12-06-2020', '13-06-2020', '14-06-2020', '15-06-2020', '16-06-2020', '17-06-2020', '18-06-2020', '19-06-2020', '20-06-2020', '21-06-2020', '22-06-2020', '23-06-2020', '24-06-2020', '25-06-2020', '26-06-2020', '27-06-2020', '28-06-2020', '29-06-2020', '30-06-2020', '01-07-2020', '02-07-2020', '03-07-2020', '04-07-2020', '05-07-2020', '06-07-2020', '07-07-2020', '08-07-2020', '09-07-2020', '10-07-2020', '11-07-2020', '12-07-2020', '13-07-2020', '14-07-2020', '15-07-2020', '16-07-2020', '17-07-2020', '18-07-2020', '19-07-2020', '20-07-2020', '21-07-2020', '22-07-2020', '23-07-2020', '24-07-2020', '25-07-2020', '26-07-2020', '27-07-2020', '28-07-2020', '29-07-2020', '30-07-2020', '31-07-2020', '01-08-2020', '02-08-2020', '03-08-2020', '04-08-2020', '05-08-2020', '06-08-2020', '07-08-2020', '08-08-2020', '09-08-2020', '10-08-2020', '11-08-2020', '12-08-2020', '13-08-2020', '14-08-2020', '15-08-2020', '16-08-2020', '17-08-2020', '18-08-2020', '19-08-2020', '20-08-2020', '21-08-2020', '22-08-2020', '23-08-2020', '24-08-2020', '25-08-2020', '26-08-2020', '27-08-2020', '28-08-2020', '29-08-2020', '30-08-2020', '31-08-2020', '01-09-2020', '02-09-2020', '03-09-2020', '04-09-2020', '05-09-2020', '06-09-2020', '07-09-2020', '08-09-2020', '09-09-2020', '10-09-2020', '11-09-2020', '12-09-2020', '13-09-2020', '14-09-2020', '15-09-2020', '16-09-2020', '17-09-2020', '18-09-2020', '19-09-2020', '20-09-2020', '21-09-2020', '22-09-2020', '23-09-2020', '24-09-2020', '25-09-2020', '26-09-2020', '27-09-2020', '28-09-2020', '29-09-2020', '30-09-2020', '01-10-2020', '02-10-2020', '03-10-2020', '04-10-2020', '05-10-2020', '06-10-2020', '07-10-2020', '08-10-2020', '09-10-2020', '10-10-2020', '11-10-2020', '12-10-2020', '13-10-2020', '14-10-2020', '15-10-2020', '16-10-2020', '17-10-2020', '18-10-2020', '19-10-2020', '20-10-2020', '21-10-2020', '22-10-2020', '23-10-2020', '24-10-2020', '25-10-2020', '26-10-2020', '27-10-2020', '28-10-2020', '29-10-2020', '30-10-2020', '31-10-2020', '01-11-2020', '02-11-2020', '03-11-2020', '04-11-2020', '05-11-2020', '06-11-2020', '07-11-2020', '08-11-2020', '09-11-2020', '10-11-2020', '11-11-2020', '12-11-2020', '13-11-2020', '14-11-2020', '15-11-2020', '16-11-2020', '17-11-2020', '18-11-2020', '19-11-2020', '20-11-2020', '21-11-2020', '22-11-2020', '23-11-2020', '24-11-2020', '25-11-2020', '26-11-2020', '27-11-2020', '28-11-2020', '29-11-2020', '30-11-2020', '01-12-2020', '02-12-2020', '03-12-2020', '04-12-2020', '05-12-2020', '06-12-2020', '07-12-2020', '08-12-2020', '09-12-2020', '10-12-2020', '11-12-2020', '12-12-2020', '13-12-2020', '14-12-2020', '15-12-2020', '16-12-2020', '17-12-2020', '18-12-2020', '19-12-2020', '20-12-2020', '21-12-2020', '22-12-2020', '23-12-2020', '24-12-2020', '25-12-2020', '26-12-2020', '27-12-2020', '28-12-2020', '29-12-2020', '30-12-2020', '31-12-2020', '01-01-2021', '02-01-2021', '03-01-2021', '04-01-2021', '05-01-2021', '06-01-2021', '07-01-2021', '08-01-2021', '09-01-2021', '10-01-2021', '11-01-2021', '12-01-2021', '13-01-2021', '14-01-2021', '15-01-2021', '16-01-2021', '17-01-2021', '18-01-2021', '19-01-2021', '20-01-2021', '21-01-2021', '22-01-2021', '23-01-2021', '24-01-2021', '25-01-2021', '26-01-2021', '27-01-2021', '28-01-2021', '29-01-2021', '30-01-2021', '31-01-2021', '01-02-2021', '02-02-2021', '03-02-2021', '04-02-2021', '05-02-2021', '06-02-2021', '07-02-2021', '08-02-2021', '09-02-2021', '10-02-2021', '11-02-2021', '12-02-2021', '13-02-2021', '14-02-2021', '15-02-2021', '16-02-2021', '17-02-2021', '18-02-2021', '19-02-2021', '20-02-2021', '21-02-2021', '22-02-2021', '23-02-2021', '24-02-2021', '25-02-2021', '26-02-2021', '27-02-2021', '28-02-2021', '01-03-2021', '02-03-2021', '03-03-2021', '04-03-2021', '05-03-2021', '06-03-2021', '07-03-2021', '08-03-2021', '09-03-2021', '10-03-2021', '11-03-2021', '12-03-2021', '13-03-2021', '14-03-2021', '15-03-2021', '16-03-2021', '17-03-2021', '18-03-2021', '19-03-2021', '20-03-2021', '21-03-2021', '22-03-2021', '23-03-2021', '24-03-2021', '25-03-2021', '26-03-2021', '27-03-2021', '28-03-2021', '29-03-2021', '30-03-2021', '31-03-2021', '01-04-2021', '02-04-2021', '03-04-2021', '04-04-2021', '05-04-2021', '06-04-2021', '07-04-2021', '08-04-2021', '09-04-2021', '10-04-2021', '11-04-2021', '12-04-2021', '13-04-2021', '14-04-2021', '15-04-2021', '16-04-2021', '17-04-2021', '18-04-2021', '19-04-2021', '20-04-2021', '21-04-2021', '22-04-2021', '23-04-2021', '24-04-2021', '25-04-2021', '26-04-2021', '27-04-2021', '28-04-2021', '29-04-2021', '30-04-2021', '01-05-2021', '02-05-2021', '03-05-2021', '04-05-2021', '05-05-2021', '06-05-2021', '07-05-2021', '08-05-2021', '09-05-2021', '10-05-2021', '11-05-2021', '12-05-2021', '13-05-2021', '14-05-2021', '15-05-2021', '16-05-2021', '17-05-2021', '18-05-2021', '19-05-2021', '20-05-2021', '21-05-2021', '22-05-2021', '23-05-2021', '24-05-2021', '25-05-2021', '26-05-2021', '27-05-2021', '28-05-2021', '29-05-2021', '30-05-2021', '31-05-2021', '01-06-2021', '02-06-2021', '03-06-2021', '04-06-2021', '05-06-2021', '06-06-2021', '07-06-2021', '08-06-2021', '09-06-2021', '10-06-2021', '11-06-2021', '12-06-2021', '13-06-2021', '14-06-2021', '15-06-2021', '16-06-2021', '17-06-2021', '18-06-2021', '19-06-2021', '20-06-2021', '21-06-2021', '22-06-2021', '23-06-2021', '24-06-2021', '25-06-2021', '26-06-2021', '27-06-2021', '28-06-2021', '29-06-2021', '30-06-2021', '01-07-2021', '02-07-2021', '03-07-2021', '04-07-2021', '05-07-2021', '06-07-2021', '07-07-2021', '08-07-2021', '09-07-2021', '10-07-2021', '11-07-2021', '12-07-2021', '13-07-2021', '14-07-2021', '15-07-2021', '16-07-2021', '17-07-2021', '18-07-2021', '19-07-2021', '20-07-2021', '21-07-2021', '22-07-2021', '23-07-2021', '24-07-2021', '25-07-2021', '26-07-2021', '27-07-2021', '28-07-2021', '29-07-2021', '30-07-2021', '31-07-2021', '01-08-2021', '02-08-2021', '03-08-2021', '04-08-2021', '05-08-2021', '06-08-2021', '07-08-2021', '08-08-2021', '09-08-2021', '10-08-2021', '11-08-2021', '12-08-2021', '13-08-2021', '14-08-2021', '15-08-2021', '16-08-2021', '17-08-2021', '18-08-2021', '19-08-2021', '20-08-2021', '21-08-2021', '22-08-2021', '23-08-2021', '24-08-2021', '25-08-2021', '26-08-2021', '27-08-2021', '28-08-2021', '29-08-2021', '30-08-2021', '31-08-2021', '01-09-2021', '02-09-2021', '03-09-2021', '04-09-2021', '05-09-2021', '06-09-2021', '07-09-2021', '08-09-2021', '09-09-2021', '10-09-2021', '11-09-2021', '12-09-2021', '13-09-2021', '14-09-2021', '15-09-2021', '16-09-2021', '17-09-2021', '18-09-2021', '19-09-2021', '20-09-2021', '21-09-2021', '22-09-2021', '23-09-2021', '24-09-2021', '25-09-2021', '26-09-2021', '27-09-2021', '28-09-2021', '29-09-2021', '30-09-2021', '01-10-2021', '02-10-2021', '03-10-2021', '04-10-2021', '05-10-2021', '06-10-2021', '07-10-2021', '08-10-2021', '09-10-2021', '10-10-2021', '11-10-2021', '12-10-2021', '13-10-2021', '14-10-2021', '15-10-2021', '16-10-2021', '17-10-2021', '18-10-2021', '19-10-2021', '20-10-2021', '21-10-2021', '22-10-2021', '23-10-2021', '24-10-2021', '25-10-2021', '26-10-2021', '27-10-2021', '28-10-2021', '29-10-2021', '30-10-2021', '31-10-2021', '01-11-2021', '02-11-2021', '03-11-2021', '04-11-2021', '05-11-2021', '06-11-2021', '07-11-2021', '08-11-2021', '09-11-2021', '10-11-2021', '11-11-2021', '12-11-2021', '13-11-2021', '14-11-2021', '15-11-2021', '16-11-2021', '17-11-2021', '18-11-2021', '19-11-2021', '20-11-2021', '21-11-2021', '22-11-2021', '23-11-2021', '24-11-2021', '25-11-2021', '26-11-2021', '27-11-2021', '28-11-2021', '29-11-2021', '30-11-2021', '01-12-2021', '02-12-2021', '03-12-2021', '04-12-2021', '05-12-2021', '06-12-2021', '07-12-2021', '08-12-2021', '09-12-2021', '10-12-2021', '11-12-2021', '12-12-2021', '13-12-2021', '14-12-2021', '15-12-2021', '16-12-2021', '17-12-2021', '18-12-2021', '19-12-2021', '20-12-2021', '21-12-2021', '22-12-2021', '23-12-2021', '24-12-2021', '25-12-2021', '26-12-2021', '27-12-2021', '28-12-2021', '29-12-2021', '30-12-2021', '31-12-2021', '01-01-2022', '02-01-2022', '03-01-2022', '04-01-2022', '05-01-2022', '06-01-2022', '07-01-2022', '08-01-2022', '09-01-2022', '10-01-2022', '11-01-2022', '12-01-2022', '13-01-2022', '14-01-2022', '15-01-2022', '16-01-2022', '17-01-2022', '18-01-2022', '19-01-2022', '20-01-2022', '21-01-2022', '22-01-2022', '23-01-2022', '24-01-2022', '25-01-2022', '26-01-2022', '27-01-2022', '28-01-2022', '29-01-2022', '30-01-2022', '31-01-2022', '01-02-2022', '02-02-2022', '03-02-2022', '04-02-2022', '05-02-2022', '06-02-2022', '07-02-2022', '08-02-2022', '09-02-2022', '10-02-2022', '11-02-2022', '12-02-2022', '13-02-2022', '14-02-2022', '15-02-2022', '16-02-2022', '17-02-2022', '18-02-2022', '19-02-2022', '20-02-2022', '21-02-2022', '22-02-2022', '23-02-2022', '24-02-2022', '25-02-2022', '26-02-2022', '27-02-2022', '28-02-2022', '01-03-2022', '02-03-2022', '03-03-2022', '04-03-2022', '05-03-2022', '06-03-2022', '07-03-2022', '08-03-2022', '09-03-2022', '10-03-2022', '11-03-2022']
                while(1):
                    print()
                    print('########################################################################')
                    print()
                    print('Country Section!!')
                    print()
                    print("Please Select any of the below country:")
                    print()
                    print("Insert -1 to go back")
                    for i in range(len(country_news_list)):
                        print(i,':',country_news_list[i])
                    print()
                    try:
                        country_selected = int(input())
                    except ValueError:
                        print('Please give valid input!!')
                        print()
                        continue
                    print()
                    if(country_selected == -1):
                        break
                    else:
                        if(country_selected >=0 and country_selected < len(country_news_list)):
                            print('Selected Country is:',country_news_list[country_selected])
                            print('########################################################################')
                            print("Range of the Valid News for", country_news_list[country_selected], 'is:')
                            print(country_news_range[country_news_list[country_selected]][0].replace('_', ' '), 'to', country_news_range[country_news_list[country_selected]][1].replace('_', ' '))

                            while(1):
                                print()
                                print('########################################################################')
                                print()
                                print('Insert -1 : To go back')
                                print('Insert 0 : To extract NEWS of certain range')
                                print('Insert 1 : To Plot word cloud for any valid given range')
                                print('Insert 2 : To know top 3 closest country, according to Jaccard Similarity (considering all the words)')
                                print('Insert 3 : To know top 3 closest country, according to Jaccard Similarity (considering only covid words)')
                                print()
                                
                                try:
                                    country_sub_select = int(input())
                                except ValueError:
                                    print('Please give valid input!!')
                                    print()
                                    continue
                                if(country_sub_select == -1):
                                    break
                                elif(country_sub_select >= 0 and country_sub_select <= 3):
                                    country_data_of_range = ''
                                    filtered_country_data_of_range = ''
                                    all_jac_sim = {}
                                    cov_jac_sim = {}
                                    
                                    print()
                                    print('Please Insert Start Date (in dd-mm-yyyy format):')
                                    start_date_country = input()
                                    print('Please Insert End Date (in dd-mm-yyyy format):')
                                    end_date_country = input()
                                    print()
                                    try:
                                        start_date_country_index = valid_dates.index(start_date_country)
                                    except ValueError:
                                        print('Start Date is Not Valid')
                                        continue
                                    try:
                                        end_date_country_index = valid_dates.index(end_date_country)
                                    except ValueError:
                                        print('End Date is Not Valid')
                                        continue
                                    if(start_date_country_index == end_date_country_index):
                                        print('Please Enter Different Dates')
                                    elif(start_date_country_index > end_date_country_index):
                                        print('Start date should come before End date')
                                    else:
                                        for i in range(start_date_country_index, end_date_country_index+1):
                                            if(valid_dates[i] in all_country_news[country_news_list[country_selected]]):
                                                country_data_of_range += '\n' + all_country_news[country_news_list[country_selected]][valid_dates[i]]
                                        
                                        country_data_of_range = country_data_of_range.replace('.', '. ')
                                        country_data_of_range = country_data_of_range.replace(':', ' : ')
                                        
                                        country_data_of_range_list = []
                                        word_tokens = word_tokenize(country_data_of_range)
                                        filtered_sentence = {}
                                        for w in word_tokens:
                                            if w.lower() not in stop_words:
                                                if(len(w) > 2):
                                                    country_data_of_range_list.append(w)
                                                    if(w in filtered_sentence):
                                                        filtered_sentence[w] += 1
                                                    else:
                                                        filtered_sentence[w] = 1
                                        
                                        for c in range(len(country_news_list)):
                                            tmp_country_data_of_range = ''
                                            if(c!=country_selected):
                                                for i in range(start_date_country_index, end_date_country_index+1):
                                                    if(valid_dates[i] in all_country_news[country_news_list[c]]):
                                                        tmp_country_data_of_range += '\n' + all_country_news[country_news_list[c]][valid_dates[i]]
                                                temp_country_data_of_range_list = []
                                                temp_word_tokens = word_tokenize(tmp_country_data_of_range)
                                                for w in temp_word_tokens:
                                                    if w.lower() not in stop_words:
                                                        if(len(w) > 2):
                                                            temp_country_data_of_range_list.append(w)
                                                jacc_val_all = len((set(country_data_of_range_list) & set(temp_country_data_of_range_list))) / (len((set(country_data_of_range_list) | set(temp_country_data_of_range_list))) + 0.00001)
                                                jacc_val_cov = len((set(country_data_of_range_list) & set(temp_country_data_of_range_list)) & set(covid_word_list)) / len((set(country_data_of_range_list) | set(temp_country_data_of_range_list)) | set(covid_word_list))

                                                all_jac_sim[country_news_list[c]] = jacc_val_all
                                                cov_jac_sim[country_news_list[c]] = jacc_val_cov
                                        sort_dict_all = sorted(all_jac_sim.items(), key = lambda kv:(kv[1], kv[0]))
                                        sort_dict_cov = sorted(cov_jac_sim.items(), key = lambda kv:(kv[1], kv[0]))

                                        if(country_sub_select == 0):
                                            if(len(country_data_of_range) == 0):
                                                print("Insufficient Data to display!!")
                                            else:
                                                print(country_data_of_range)
                                            print()
                                        elif(country_sub_select == 2):
                                            print('########################################################################')
                                            print()
                                            print('Top 3 closest countries according to jaccard similarity (considering all words) are:')
                                            print(sort_dict_all[-1][0],':', sort_dict_all[-1][1])
                                            print(sort_dict_all[-2][0], ':', sort_dict_all[-2][1])
                                            print(sort_dict_all[-3][0], ':', sort_dict_all[-3][1])
                                            print()
                                            print('########################################################################')
                                        elif(country_sub_select == 3):
                                            print('########################################################################')
                                            print()
                                            print('Top 3 closest countries according to jaccard similarity (considering only covid words) are:')
                                            print(sort_dict_cov[-1][0],':', sort_dict_cov[-1][1])
                                            print(sort_dict_cov[-2][0], ':', sort_dict_cov[-2][1])
                                            print(sort_dict_cov[-3][0], ':', sort_dict_cov[-3][1])
                                            print()
                                            print('########################################################################')

                                        else:
                                            if(len(filtered_sentence) == 0):
                                                print("Insufficient Data to plot the Word Cloud!!")
                                            else:
                                                wordcloud = WordCloud(background_color="white",width=1000,height=1000, stopwords = stop_words, min_font_size = 10).generate_from_frequencies(filtered_sentence)

                                            plt.figure(figsize = (8, 8), facecolor = None)
                                            plt.imshow(wordcloud)
                                            plt.axis("off")
                                            plt.tight_layout(pad = 0)

                                            plt.show()
                                else:
                                    print('Inserted Value is out of range!!')
                                    print()
                        else:
                            print('Inserted Value is out of range!!')
                            print()

            elif(news_type == -1):
                break
            else:
                print("Input Out of Bound!!")
    elif(covid_type == -1):
        break
    else:
        print("Input Out of Bound!!")