def Get_Years(Datalist):
    Year = []
    filter_data = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), Datalist))
    for x in filter_data:
        if int(x['Year']) in Year:
            pass
        else:
            Year.append(int(x['Year']))
    return(Year)

def Get_Countries(Datalist):
    Countries = []
    filter_data = list(filter(lambda x: 'Emissions (thousand metric tons of carbon dioxide)' in x.values(), Datalist))
    for x in filter_data:
        if (x['Country']) in Countries:
            pass
        else:
            Countries.append((x['Country']))
    return(Countries)


def Get_Land(Land_Datalist):
    Land_Type = []
    for x in Land_Datalist:
        if (x['Series']) in Land_Type:
            pass
        else:
            Land_Type.append(x['Series'])
    return(Land_Type)