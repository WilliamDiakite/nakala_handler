import pandas as pd
import numpy as np
import datetime


months = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


def rm_digit(str):
    return ''.join([c for c in str if not c.isdigit()])


def clean_date(d):
    if isinstance(d, str):
        if len(d.split('-')) > 1 and d.split('-')[1] in months:
            rep = d.replace(d.split('-')[1], months[d.split('-')[1]])
            rep = rep.split('-')[::-1]
            rep[0] = '19' + rep[0]
            return '-'.join(rep)
        elif len(d.split('-')) > 1 and d.split('-')[0] in months:
            rep = d.replace(d.split('-')[0], months[d.split('-')[0]])
            rep = rep.split('-')[::-1]
            rep[0] = '19' + rep[0]
            return '-'.join(rep)
        elif len(d.split('-')) == 2 and len(d.split('-')[0]) == 4 and len(d.split('-')[1]) == 4:
            return d.replace('-', ' - ')
        else:
            return d
    else:
        return d


def prepare(src):

    data = pd.read_csv(src).drop_duplicates()

    data['fonds'] = data['Référence Num'].apply(
        lambda x: rm_digit(x.split('_')[0].strip()) if pd.notnull(x) else np.nan)

    data['dossier'] = data['Référence Num'].apply(
                    lambda x: x.split('_')[3].strip() if pd.notnull(x) else np.nan)

    data['dossier_ref'] = data['Référence Num'].apply(
        lambda x: x.split('_')[0].strip() if pd.notnull(x) else np.nan)

    data['dossier_ref'] = data['dossier_ref'].apply(
        lambda x: x[:5] + '_' + x[5:] if pd.notnull(x) else np.nan)

    data['dossier_ref'] = data['dossier_ref'] + '_' + data['dossier']

    #
    # Get magazines and issues
    #
    data['magazine_name'] = data['Support  (titre per, cat…)'].apply(
        lambda x: x[:x.find('°')-1].strip() if isinstance(x, str) and '°' in x else x
    )
    data['magazine_issue'] = data['Support  (titre per, cat…)'].apply(
        lambda x: x[x.find('°')+1:].strip() if isinstance(x, str) and '°' in x else np.nan
    )

    #
    # Clean dates
    #
    data['date'] = data['Date ou chrono.'].apply(lambda x: clean_date(x))

    return data
