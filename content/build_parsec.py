#!/usr/bin/env python3

import datetime
import hashlib
import os.path
#import time
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import requests
from dateutil.parser import parse as parsedate

# Just for debugging purposes, to time the run time
#st = time.time()

# files needed for initial raw data import from upstream
FILE_PADS = "sites.tsv"
FILE_TEMP2 = "sites.tmp"
FILE_DATA = "launchdata.tsv"
FILE_TEMP = "launchdata.tmp"

# hardcoding countries with orbital launch attempts
country = ["SUA", "Rusia", "China", "Europa", "Japonia", "India", "Iran", "Israel", "Coreea de Sud", "Coreea de Nord", "Brazilia"]

# hardcoding active rockets, as dict
active_rockets = {'Falcon 9' : 'falcon9',
'Falcon Heavy' : 'falconh',
'Ariane 5' : 'ariane5',
'Vega' : 'vegac',
'Atlas V' : 'atlasv',
'Delta 4M' : 'delta4',
'Delta 4H' : 'delta4h',
'Electron' : 'electron',
'Firefly' : 'fireflya',
'LauncherOne' : 'launcherone',
'Astra' : 'astra',
'Antares' : 'antares',
'Minotaur' :'minotaur',
'Pegasus' : 'pegasus',
'H-II' : 'hii',
'Epsilon' : 'epsilon',
'Chang Zheng 2C' : 'cz2c',
'Chang Zheng 2D' : 'cz2d',
'Chang Zheng 2F' : 'cz2f',
'Chang Zheng 3B' : 'cz3b',
'Chang Zheng 3C' : 'cz3c',
'Chang Zheng 4B' : 'cz4b',
'Chang Zheng 4C' : 'cz4',
'Chang Zheng 5' : 'cz5',
'Chang Zheng 6' : 'cz6',
'Chang Zheng 7' : 'cz7',
'Chang Zheng 8' : 'cz8',
'Chang Zheng 11' : 'cz11',
'Kuaizhou-1A' :'kz1a',
'Kuaizhou-11' : 'kz11',
'Gushenxing' : 'gushenxing',
'Lijian-1' : 'lijian',
'Shuang Quxian' : 'sq1',
'Jielong' : 'jielong',
'OS-M1' : 'osm1',
'Zhuque-1' : 'zhuque1',
'KT-2' : 'kt2',
'Soyuz-2.1' : 'soyuz21',
'Soyuz-2.1v' : 'soyuz21v',
'Angara-1.2' : 'angara12',
'Angara A5' : 'angaraa5',
'Proton-M' : 'protonm',
'Kwangmyongsong' : 'kwangmyongsong',
'Safir' : 'safir',
'Simorgh' : 'simorgh',
'Qased' : 'qased',
'Shavit' : 'shavit',
'Nuri' : 'nuri',
'GSLV Mk III' : 'gslvmk3',
'GSLV Mk II' : 'gslvmk2',
'PSLV' : 'pslv',
'SSLV' : 'sslv'}
list_active_rockets = list(active_rockets.keys())

# getting the current year in a variable
today = datetime.date.today()
curr_year = today.year

def update_GCAT():
	
	if os.path.isfile(FILE_TEMP): os.remove(FILE_TEMP)
	
	print('Checking for GCAT update...')
	url = 'https://planet4589.org/space/gcat/tsv/launch/launch.tsv'
	response = requests.get(url, allow_redirects=True)
	open(FILE_TEMP,"wb").write(response.content)

	r = requests.head(url)
	url_time = r.headers['last-modified']
	url_date = parsedate(url_time)

	md5_hash = hashlib.md5
	with open(FILE_TEMP,"rb") as f:
		bytes = f.read()
		readable_hash = hashlib.md5(bytes).hexdigest()

	if os.path.isfile(FILE_DATA):
		with open(FILE_DATA,"rb") as g:
			bytes = g.read()
			readable_hash2 = hashlib.md5(bytes).hexdigest()
			if readable_hash == readable_hash2: 
				os.remove(FILE_TEMP)
				print ("No updates found!")
			else: 
				os.remove(FILE_DATA)
				os.rename(FILE_TEMP,FILE_DATA)
				print ("New GCAT version installed, date:",url_date)
	else:
		os.rename(FILE_TEMP,FILE_DATA)
		print ("No old GCAT found, fetched latest version from date",url_date)
		
def update_PADS():

	if os.path.isfile(FILE_TEMP2): os.remove(FILE_TEMP2)

	print('Checking for PADS update...')
	url = 'https://planet4589.org/space/gcat/tsv/tables/sites.tsv'
	response = requests.get(url, allow_redirects=True)
	open(FILE_TEMP2,"wb").write(response.content)


	r = requests.head(url)
	url_time = r.headers['last-modified']
	url_date = parsedate(url_time)

	md5_hash = hashlib.md5
	with open(FILE_TEMP2,"rb") as f:
		bytes = f.read()
		readable_hash = hashlib.md5(bytes).hexdigest()

	if os.path.isfile(FILE_PADS):
		with open(FILE_PADS,"rb") as g:
			bytes = g.read()
			readable_hash2 = hashlib.md5(bytes).hexdigest()
			if readable_hash == readable_hash2: 
				os.remove(FILE_TEMP2)
				print ("No updates found!")
			else: 
				os.remove(FILE_PADS)
				os.rename(FILE_TEMP2,FILE_PADS)
				print ("New PADS version installed, date:",url_date)
	else:
		os.rename(FILE_TEMP2,FILE_PADS)
		print ("No old PADS found, fetched latest version from date",url_date)

# Download files if they are not present in current directory
#if not os.path.isfile(FILE_DATA): update_GCAT()
#if not os.path.isfile(FILE_PADS): update_PADS()
update_GCAT()
update_PADS()

print('Loading data...')

# Importing upstream files into dataframes
df = pd.read_csv(FILE_DATA, sep='\t', header=None, skiprows=lambda x: x<2, names=['Launch_Tag', 'Launch_JD', 'Launch_Date', 'LV_Type', 'Variant', 'Flight_ID', 'Flight', 'Mission', 'FlightCode', 'Platform', 'Launch_Site', 'Launch_Pad', 'Ascent_Site', 'Ascent_Pad', 'Apogee', 'Apoflag', 'Range', 'RangeFlag', 'Dest', 'Agency', 'Launch_Code', 'Group', 'Category', 'LTCite', 'Cite', 'Notes'])
pads = pd.read_csv(FILE_PADS, sep='\t', header=None, skiprows=lambda xx: xx<2, names=['Site', 'Code', 'UCode', 'Type', 'StateCode', 'TStart', 'TStop', 'ShortName', 'Name', 'Location', 'Longitude', 'Latitude', 'Error', 'Parent', 'ShortEName', 'EName', 'Group', 'UName'])

# Cleaning up the countries a bit
pads['StateCode'] = pads['StateCode'].replace('DZ','EU', regex=True)
pads['StateCode'] = pads['StateCode'].replace('J','JP', regex=True)
pads['StateCode'] = pads['StateCode'].replace('GUF','EU', regex=True)
pads['StateCode'] = pads['StateCode'].replace('AU','EU', regex=True)
pads['StateCode'] = pads['StateCode'].replace('NZ','US', regex=True)
pads['StateCode'] = pads['StateCode'].replace('TTPI','US', regex=True)
pads['StateCode'] = pads['StateCode'].replace('ESCN','US', regex=True)
pads['StateCode'] = pads['StateCode'].replace('KE','US', regex=True)
pads['StateCode'] = pads['StateCode'].replace('KI','RU', regex=True)
pads['StateCode'] = pads['StateCode'].replace('SU','RU', regex=True)

# Quick and dirty fix, since I consider 2022-U02 to be a proper failed launch deserving the F tag
# To be removed if this changes upstream
df['Launch_Tag'] = df['Launch_Tag'].replace('2022-U02', '2022-F0x', regex=True)

# Filtering suborbital launches
df = df[df["Launch_Tag"].str.contains("-S") == False]
df = df[df["Launch_Tag"].str.contains("-A") == False]
df = df[df["Launch_Tag"].str.contains("-M") == False]
df = df[df["Launch_Tag"].str.contains("-W") == False]
df = df[df["Launch_Tag"].str.contains("-Y") == False]
df = df[df["Launch_Tag"].str.contains("-U") == False]
df = df[df["Launch_Tag"].str.contains("2014-000") == False]

# Changing date format
df['Launch_Date'] = df['Launch_Date'].replace(' Jan ', '-01-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Feb ', '-02-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Mar ', '-03-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Apr ', '-04-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' May ', '-05-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Jun ', '-06-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Jul ', '-07-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Aug ', '-08-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Sep ', '-09-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Oct ', '-10-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Nov ', '-11-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace(' Dec ', '-12-', regex=True)
df['Launch_Date'] = df['Launch_Date'].replace('- ', '-0', regex=True)

# Changing some rockets' name
#df['LV_Type'] = df['LV_Type'].replace('Delta 4H', 'Delta IV Heavy', regex=True)
df['LV_Type'] = df['LV_Type'].replace('Soyuz-2-1A', 'Soyuz-2.1a', regex=True)
df['LV_Type'] = df['LV_Type'].replace('Soyuz-2-1B', 'Soyuz-2.1b', regex=True)
df['LV_Type'] = df['LV_Type'].replace('Soyuz-2-1V', 'Soyuz-2.1v', regex=True)
#df['LV_Type'] = df['LV_Type'].replace('GSLV Mk II', 'GSLV Mk. 2', regex=True)
#df['LV_Type'] = df['LV_Type'].replace('GSLV Mk III', 'GSLV Mk. 3', regex=True)

# Removing seconds from timestamps
df['Launch_Date'] = df['Launch_Date'].apply(lambda x: x.split(':')[0] if len(x) > 16 else x)

# Adding the 'Country' column, based on launch pads country code in sites.tsv
dict_Site = dict(zip(pads.Site, pads.StateCode))
df['Country'] = df['Launch_Site'].map(dict_Site)

# adding 'Outcome' column, based on Launch_Tag
# def check_outcome(row):  
#    if '-F' in row['Launch_Tag']:
#        return 'F'
#    return 'S'
#df['Outcome'] = df.apply(lambda row: check_outcome(row), axis=1)

df['Outcome'] = df['Launch_Tag'].map(lambda x: 'F' if 'F' in x else 'S')

# Code to be optimized below this line:
#--------------------------------------

ldata = df.to_numpy()
pdata = pads.to_numpy()

ldata_rows = len(df.index)
pdata_rows = len(pads.index)

def locations():
    field_names = ["Centru", "Denumire", "Țara"]
    data = []
    i = 0
    list_locations = pd.unique(df['Launch_Site'])
    while i < pdata_rows:
        if pdata[i][0] in list_locations:
            data.append([pdata[i][0], pdata[i][8], pdata[i][4]])
        i+=1
    df_locations = pd.DataFrame(data, columns=field_names)
    return(df_locations.to_markdown(index=False))
    
list_legend = locations()

def succ_country(year):
 
	l_succ_country = [0] * 12
	i = 0
    
	while i<ldata_rows:
		if str(year) in str(ldata[i][2][0:7]) and "F" not in str(ldata[i][0]): 
			l_succ_country[11]+=1
			if ldata[i][26] == "US": l_succ_country[0]+=1
			if ldata[i][26] == "RU": l_succ_country[1]+=1
			if ldata[i][26] == "CN": l_succ_country[2]+=1
			if ldata[i][26] == "EU": l_succ_country[3]+=1
			if ldata[i][26] == "JP": l_succ_country[4]+=1
			if ldata[i][26] == "IN": l_succ_country[5]+=1
			if ldata[i][26] == "IR": l_succ_country[6]+=1
			if ldata[i][26] == "IL": l_succ_country[7]+=1
			if ldata[i][26] == "KR": l_succ_country[8]+=1
			if ldata[i][26] == "KP": l_succ_country[9]+=1
			if ldata[i][26] == "BR": l_succ_country[10]+=1
		i+=1
	return(l_succ_country)

def fail_country(year):
    
	l_fail_country = [0] * 12
	i = 0
    
	while i<ldata_rows:
		if str(year) in str(ldata[i][2][0:7]) and "F" in str(ldata[i][0]): 
			l_fail_country[11]+=1
			if ldata[i][26] == "US": l_fail_country[0]+=1
			if ldata[i][26] == "RU": l_fail_country[1]+=1
			if ldata[i][26] == "CN": l_fail_country[2]+=1
			if ldata[i][26] == "EU": l_fail_country[3]+=1
			if ldata[i][26] == "JP": l_fail_country[4]+=1
			if ldata[i][26] == "IN": l_fail_country[5]+=1
			if ldata[i][26] == "IR": l_fail_country[6]+=1
			if ldata[i][26] == "IL": l_fail_country[7]+=1
			if ldata[i][26] == "KR": l_fail_country[8]+=1
			if ldata[i][26] == "KP": l_fail_country[9]+=1
			if ldata[i][26] == "KP": l_fail_country[9]+=1
			if ldata[i][26] == "BR": l_fail_country[10]+=1
		i+=1
	return(l_fail_country)

# număr total lansări de succes pe țări, exportat ca array
def total_succ_country():
    i = 1957
    j = 0
    tsuc_country = [0] * 12
    while i<=curr_year:
        j = 0
        while j<12:
            tsuc_country[j] = tsuc_country[j] + succ_country(i)[j]
            j+=1
        i+=1
    return(tsuc_country)
ex_total_succ_country = total_succ_country()

# număr total eșecuri pe țări, exportat ca array
def total_fail_country():
    i = 1957
    j = 0
    tfail_country = [0] * 12
    while i<=curr_year:
        j = 0
        while j<12:
            tfail_country[j] = tfail_country[j] + fail_country(i)[j]
            j+=1
        i+=1
    return(tfail_country)
ex_total_fail_country = total_fail_country()

def total_tot_country():
    i = 0
    ttot_country = [0] * 12
    while i < 12:
        ttot_country[i] = ex_total_succ_country[i] + ex_total_fail_country[i]
        i+=1
    return(ttot_country)
ex_total_tot_country = total_tot_country()

def preambul(year):
    a = ("În anul %d au avut loc un total de %d tentative de lansări orbitale, din care %d eșecuri." % (year, succ_country(year)[11]+fail_country(year)[11], fail_country(year)[11]))
    return(a)

def launch_stat(year):
# ylaunch
	i = 0
	field_names = ["ID", "Dată (UTC)", "Lansator", "Serie", "Satelit (misiune)", "Or", "Centru", "R"]
	data = []

	while i<ldata_rows:
		if str(year) in str(ldata[i][2][0:7]):
			data.append([ldata[i][0].strip(), ldata[i][2] if ":" not in ldata[i][2] else ldata[i][2][:-3], ldata[i][3] if len(ldata[i][4])<2 else ldata[i][3]+" / "+ldata[i][4], ldata[i][5], ldata[i][6] if ldata[i][6].strip() == ldata[i][7].strip() else ldata[i][6].strip() +" ("+ldata[i][7].strip()+")", ldata[i][26], ldata[i][10] +"+"+ ldata[i][11], ldata[i][27]])
		i+=1
	df_ls = pd.DataFrame(data, columns=field_names)
	return(df_ls.to_markdown(index=False))

def launch_stat_list(year):
# zlaunch

	l_tot_country = [0] * 12
	l_fail_country = fail_country(year)
	l_succ_country = succ_country(year)
	field_names = ["Țara", "Tentative", "Reușite", "Eșecuri"]
	data = []

	i = 0
	while i<10:
		l_tot_country[i] = l_succ_country[i] + l_fail_country[i]
		i+=1
    
	i = 0
	while i<11:
		if l_tot_country[i]>0: data.append([country[i], l_succ_country[i]+l_fail_country[i], l_succ_country[i], l_fail_country[i]])
		i+=1
	df_lsl = pd.DataFrame(data, columns=field_names)

	return(df_lsl.to_markdown(index=False))

def launch_stat_graph(year):

	l_tot_country = [0] * 12
	l_fail_country = fail_country(year)
	l_succ_country = succ_country(year)
    
	i = 0
	while i<10:
		l_tot_country[i] = l_succ_country[i] + l_fail_country[i]
		i+=1

	list_countries = ["US", "CN", "RU", "EU", "JP", "IN", "IR", "IL", "KR", "KP"]
	list_slaunches = [l_succ_country[0], l_succ_country[2], l_succ_country[1], l_succ_country[3], l_succ_country[4], l_succ_country[5], l_succ_country[6], l_succ_country[7], l_succ_country[8], l_succ_country[9]]
	list_tlaunches = [l_tot_country[0], l_tot_country[2], l_tot_country[1], l_tot_country[3], l_tot_country[4], l_tot_country[5], l_tot_country[6], l_tot_country[7], l_tot_country[8], l_tot_country[9]]

	plt.bar(list_countries, list_tlaunches, color="r", label="Lansări eșuate")
	plt.bar(list_countries, list_slaunches, color="b", label="Lansări reușite")
	plt.title("Lansări orbitale %s" % str(year))
	plt.legend()
	plt.show()
	plt.close()

def all_succ_launches():
    i = curr_year
    data = []
    field_names = ["An", "Total", "SUA", "RU", "CN", "EU", "JP", "IN", "IR", "IL", "KP", "KR", "BR"]
    while i>1956:
        l_succ_country = succ_country(i)
        data.append([i, l_succ_country[11], l_succ_country[0], l_succ_country[1], l_succ_country[2], l_succ_country[3], l_succ_country[4], l_succ_country[5], l_succ_country[6], l_succ_country[7], l_succ_country[8], l_succ_country[9], l_succ_country[10]])
        i-=1
    df_als = pd.DataFrame(data, columns=field_names)
    return(df_als.to_markdown(index=False))

def all_fail_launches():
    i = curr_year
    data = []
    field_names = ["An", "Total", "SUA", "RU", "CN", "EU", "JP", "IN", "IR", "IL", "KP", "KR", "BR"]
    while i>1956:
        l_fail_country = fail_country(i)
        data.append([i, l_fail_country[11], l_fail_country[0], l_fail_country[1], l_fail_country[2], l_fail_country[3], l_fail_country[4], l_fail_country[5], l_fail_country[6], l_fail_country[7], l_fail_country[8], l_fail_country[9], l_fail_country[10]])
        i-=1
    df_alf = pd.DataFrame(data, columns=field_names)
    return(df_alf.to_markdown(index=False))

def all_succ_launches_matrix():
    i = 1957
    all_succ = [0 for i in range(curr_year-1957+1)] 
    while i<=curr_year:
        l_succ_country = succ_country(i)
        all_succ[i-1957] = l_succ_country[11]
        i+=1
    return(all_succ)

def all_fail_launches_matrix():
    i = 1957
    all_fail = [0 for i in range(curr_year-1957+1)] 
    while i<=curr_year:
        l_fail_country = fail_country(i)
        all_fail[i-1957] = l_fail_country[11]
        i+=1
    return(all_fail)

def all_tot_launches_matrix():
    a = all_succ_launches_matrix()
    b = all_fail_launches_matrix()
    all_tot = [0 for i in range(curr_year-1957+1)] 
    i = 0
    while i < curr_year-1957+1:
        all_tot[i] = a[i] + b[i]
        i+=1
    return(all_tot)

table_all_succ = all_succ_launches()
total_launches = all_tot_launches_matrix()
total_failed = all_fail_launches_matrix()
total_succ = all_succ_launches_matrix()

def racheta(nume):
    i = 0
    j = 0
    field_names = ["ID", "Dată (UTC)", "Lansator", "Serie", "Satelit (misiune)", "Or", "Centru", "R"]
    data = []
    r_launches = 0
    r_fail = 0
    while i<ldata_rows:
        if nume in ldata[i][3]: 
            data.append([ldata[i][0].strip(), ldata[i][2] if ":" not in ldata[i][2] else ldata[i][2][:-3], ldata[i][3], ldata[i][5], ldata[i][6] if (((ldata[i][6].strip() == ldata[i][7].strip()) or (ldata[i][7].strip == "-"))) else ldata[i][6].strip() +" ("+ldata[i][7].strip()+")", ldata[i][26], ldata[i][10] +"+"+ ldata[i][11], ldata[i][27]])
            r_launches+=1
            if "F" in ldata[i][27]: 
                r_fail+=1
                j = 0      
            j+=1
        i+=1
    line6 = ""
    launches_since_fail = j-1
    
    df_racheta = pd.DataFrame(data, columns=field_names)
    
    if r_launches == 0: 
        rate_succ = 100 
    else: 
        rate_succ = 100 - (r_fail / r_launches *100)
    
    line1 = ("Lista lansărilor orbitale pentru racheta %s:" % nume)
    line3 = ("Până în prezent, racheta %s a fost lansată de %d ori " % (nume, r_launches))
    line4 = ("(din care %d eșecuri)." % (r_fail))
    line5 = ("Rată de succes a rachetei %s este de %.2f%%." % (nume, rate_succ))
    if r_fail > 0: line6 = ("Număr de lansări reușite de la ultimul eșec: %d\n\n" % (launches_since_fail))
    
    r_content = line3 + line4 +'\n'+'\n'+ line5 +'\n'+ line6 +'\n'+ line1
    return (r_content, df_racheta.to_markdown(index=False))

def recent_launches(n):
    field_names = ["ID", "Dată (UTC)", "Lansator", "Serie", "Satelit (misiune)", "Or", "Centru", "R"]
    data = []
    i = 1
    while i<n:
        data.append([ldata[-i][0].strip(), ldata[-i][2] if ":" not in ldata[-i][2] else ldata[-i][2][:-3], ldata[-i][3] if len(ldata[-i][4])<2 else ldata[-i][3]+" / "+ldata[-i][4], ldata[-i][5], ldata[-i][6] if ldata[-i][6].strip() == ldata[-i][7].strip() else ldata[-i][6].strip() +" ("+ldata[-i][7].strip()+")", ldata[-i][26], ldata[-i][10] +"+"+ ldata[-i][11], ldata[i][27]])
        i+=1
    df_recent_launches = pd.DataFrame(data, columns=field_names)
    return(df_recent_launches.to_markdown(index=False))

def show_starlink():
    field_names = ["ID", "Dată (UTC)", "Lansator", "Serie", "Satelit (misiune)", "Centru"]
    data = []
    i = 0
    j = 0
    while i < ldata_rows:
        if ("Starlink" in ldata[i][6]) or ("Starlink" in ldata[i][7]):
            j+=1
            data.append([ldata[i][0].strip(), ldata[i][2] if ":" not in ldata[i][2] else ldata[i][2][:-3], ldata[-i][3] if len(ldata[i][4])<2 else ldata[i][3]+" / "+ldata[i][4], ldata[i][5], ldata[i][6] if ldata[i][6].strip() == ldata[i][7].strip() else ldata[i][6].strip() +" ("+ldata[i][7].strip()+")", ldata[i][10] +"+"+ ldata[i][11]])
        i+=1
    today = date.today()
    a =  ("Până la data %s, au ajut loc %d lansări Starlink\n" % (str(today), j))
    df_show_starlink = pd.DataFrame(data, columns=field_names)
    return(a, df_show_starlink.to_markdown(index=False))

list_starlink = show_starlink()

zlaunch = []
i = 1957
while i<=curr_year:
    zlaunch.append(launch_stat_list(i))
    i+=1

ylaunch = []
i = 1957
while i<=curr_year:
    ylaunch.append(launch_stat(i))
    i+=1

mlaunch = []
i = 1957
while i<=curr_year:
    mlaunch.append(preambul(i))
    i+=1

most_recent_launches = recent_launches(12)


marker_index = '## Cele mai recente lansări orbitale'
marker_index2= '## Lansări orbitale'
marker_index_line = 0
content_index = []

with open('_index.md', 'r') as f:
    contents = f.readlines()

index = [idx for idx, s in enumerate(contents) if marker_index in s][0]
index2 = [idx for idx, s in enumerate(contents) if marker_index2 in s][0]

del contents[index+2:index2-1]

most_recent_launches = most_recent_launches + '\n'
contents.insert(index+2, most_recent_launches)

with open('_index.md', 'w') as f:
    contents = "".join(contents)
    f.write(contents)
f.close()

def gen_year(y):
	ypath = 'y/' + str(y) + '.md'
	toprint = y-1957
	
	with open(ypath, 'w+') as f:
		f.writelines('---' + '\n')
		f.writelines('permalink: "/y/' + str(y) +'"' + '\n')
		f.writelines('title: Lansări orbitale în ' + str(y) + '\n')
		f.writelines('layout: default' + '\n')
		f.writelines('---' + '\n' + '\n')
		f.writelines(mlaunch[toprint] + '\n')
		f.writelines('\n' + '\n')
		f.writelines(zlaunch[toprint] + '\n')
		f.writelines('\n' + '\n')
		f.writelines(ylaunch[toprint] + '\n')
	f.close()

def gen_rockets(rocket_name):
	rname = str(active_rockets[rocket_name])
	ypath = 'r/' + rname + '.md'
	with open(ypath, 'w+') as f:
		f.writelines('---' + '\n')
		f.writelines('permalink: "/r/' + str(active_rockets[rocket_name]) +'"' + '\n')
		f.writelines('title: ' + str(rocket_name) + '\n')
		f.writelines('layout: default' + '\n')
		f.writelines('---' + '\n' + '\n')
		f.writelines(racheta(rocket_name)[0] + '\n')
		f.writelines(racheta(rocket_name)[1] + '\n')
	f.close()

def gen_total_launches():
	t = 0
	s = 0
	i = 0
	while i < len(total_launches):
		t = t + total_launches[i]
		s = s + total_succ[i]
		i+=1
	mess1 = "Din 1957 și până în prezent au avut loc {} tentative de lansări orbitale, din care {} lansări reușite și {} eșecuri (încărcătura primară nu a ajuns pe orbită).".format(t, s, t-s) + '\n' + '\n'
	mess2 = "În tabelul de mai jos sunt prezentate numărul total de lansări orbitale, pentru fiecare stat în parte, începând cu 1957. Câteva precizări: lansările URSS și ale Rusiei nu sunt numărate separat, iar lansările statelor europene, fie prin Arianespace sau separat, sunt catalogate drept lansări europene, indiferent de locul de unde este lansată racheta. În stabilirea țării în a cărei portofoliu intră lansarea, am considerat că statul în care este înregistrat operatorul este cel consiederat în statistici (de exemplu, lansările rachetei Electron din Noua Zeelandă sunt lansări ale Statelor Unite, pentru că Rocket Lab, compania care operează lansatorul, este o companie americană)." + '\n' + '\n'
	field_names_totalorbital = ["Țară", "Tentative", "Reușite", "Eșecuri"]
	data_totalorbital = []
	i = 0
	while i<11:
		data_totalorbital.append([country[i], ex_total_tot_country[i], ex_total_succ_country[i], ex_total_fail_country[i]])
		i+=1
	df_total_orbital = pd.DataFrame(data_totalorbital, columns=field_names_totalorbital)
	mess3 = "Tabel cu numărul de lansări orbitale reușit din fiecare stat, pentru fiecare an în parte" + '\n' + '\n'

	return(mess1, mess2, df_total_orbital.to_markdown(index=False), mess3, table_all_succ)

print('Generating yearly pages...')
for i in range (1957, curr_year+1): gen_year(i)

print ('Generating rockets pages...')
i = 0
while i<len(list_active_rockets):
	gen_rockets(list_active_rockets[i])
	i+=1

with open('v/starlink.md', 'w+') as f:
	f.writelines('---' + '\n')
	f.writelines('permalink: "/v/starlink"'+ '\n')
	f.writelines('title: Starlink'+ '\n')
	f.writelines('layout: default' + '\n')
	f.writelines('---' + '\n' + '\n')
	f.writelines(show_starlink())
	f.close()

with open('y/totalorbital.md', 'w+') as f:
	f.writelines('---' + '\n')
	f.writelines('permalink: "/y/totalorbital.md"'+ '\n')
	f.writelines('title: Lansări orbitale'+ '\n')
	f.writelines('layout: default' + '\n')
	f.writelines('---' + '\n' + '\n')
	f.writelines(gen_total_launches())
	f.close()

#et = time.time()

#print('Running time: ', et-st)
print("OK!")