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
		
def launch_stat(year):

	l_succ_curr = 0 # nr. succese din anul curent
	l_fail_curr = 0 # nr. lansări eșuate din anul curent
	i = 0

	l_succ_country = [0] * 12
	l_tot_country = [0] * 12
	l_fail_country = [0] * 12
    
	country[0] = "SUA"
	country[1] = "Rusia"
	country[2] = "China"
	country[3] = "Europa"
	country[4] = "Japonia"
	country[5] = "India"
	country[6] = "Iran"
	country[7] = "Israel"
	country[8] = "Coreea de Sud"
	country[9] = "Coreea de Nord"
	country[10] = "Brazilia"
    
	while i<ldata_rows:
		if str(year) in str(ldata[i][2]) and "F" not in str(ldata[i][0]): 
			l_succ_curr+=1
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

		if str(year) in str(ldata[i][2]) and "F" in str(ldata[i][0]): 
			l_fail_curr+=1
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

	i = 0
	while i<10:
		l_tot_country[i] = l_succ_country[i] + l_fail_country[i]
		i+=1
	l_succ_country[11] = l_succ_curr
	l_fail_country[11] = l_fail_curr
    
	ytable = PrettyTable()
	ytable.align = "l"
	ytable.field_names = ["Țara", "Tentative", "Reușite", "Eșecuri"]
	i = 0
	while i<11:
		if l_tot_country[i]>0: ytable.add_row([country[i], l_succ_country[i]+l_fail_country[i], l_succ_country[i], l_fail_country[i]])
		i+=1
    
	print("În anul %d au avut loc un total de %d tentative de lansări orbitale, din care %d eșecuri.\n" % (year, l_succ_country[11]+l_fail_country[11], l_fail_country[11]))
	print(ytable)

def racheta(nume):
    i = 0
    j = 0
    rtable = PrettyTable()
    rtable.align = "l"
    rtable.field_names = ["ID", "Date", "Rocket", "Series", "Sat * Mission", "Or", "LSite", "R"]
    r_launches = 0
    r_fail = 0
    while i<ldata_rows:
        if nume in ldata[i][3]: 
            rtable.add_row([ldata[i][0].strip(), ldata[i][2] if ":" not in ldata[i][2] else ldata[i][2][:-3], ldata[i][3], ldata[i][5], ldata[i][6] if ldata[i][6].strip() == ldata[i][7].strip() else ldata[i][6].strip() +" ("+ldata[i][7].strip()+")", ldata[i][26], ldata[i][10] +"*"+ ldata[i][11], ldata[i][27]])
            r_launches+=1
            if "F" in ldata[i][27]: 
                r_fail+=1
                j = 0      
            j+=1
        i+=1
    line6 = ""
    launches_since_fail = j
    
    rate_succ = 100 - (r_fail / r_launches *100)
    
    line1 = ("Lista lansărilor orbitale pentru racheta %s\n" % nume)
    line2 = str(rtable)+"\n"
    line3 = ("Număr total de lansări %s: %d\n" % (nume, r_launches))
    line4 = ("Număr de eșecuri %s: %d\n" % (nume, r_fail))
    line5 = ("Rată de succes %s: %.2f%%\n" % (nume, rate_succ))
    if r_fail > 0: line6 = ("Număr de lansări reușite de la ultimul eșec: %d\n" % (launches_since_fail))
    
    r_content = line3 + line4 + line5 + line6 +"\n"+ line1 + line2
    return (r_content)

def active_rockets():
    list_active_rockets = []
    i = 1
    atable = PrettyTable()
    atable.align = "l"
    atable.field_names = ["Rachetă", "O.", "Cea mai recentă lansare"]
    while i<ldata_rows:
        if ldata[-i][3] not in list_active_rockets: 
            list_active_rockets.append(ldata[-i][3])
            atable.add_row([ldata[-i][3], ldata[-i][26], ldata[-i][2] if ":" not in ldata[-i][2] else ldata[-i][2][:-3]])
        i+=1
    return(atable)