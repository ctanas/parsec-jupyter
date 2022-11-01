def recent_launches(n):
    ttable = PrettyTable()
    ttable.align = "l"
    ttable.field_names = ["ID", "Date", "Rocket", "Series", "Sat * Mission", "Or", "LSite"]

    i = 1
    while i<n:
        ttable.add_row([ldata[-i][0].strip(), ldata[-i][2] if ":" not in ldata[-i][2] else ldata[-i][2][:-3], ldata[-i][3] if len(ldata[-i][4])<2 else ldata[-i][3]+" / "+ldata[-i][4], ldata[-i][5], ldata[-i][6] if ldata[-i][6].strip() == ldata[-i][7].strip() else ldata[-i][6].strip() +" ("+ldata[-i][7].strip()+")", ldata[-i][26], ldata[-i][10] +"+"+ ldata[-i][11]])
        i+=1
    
    print(ttable)