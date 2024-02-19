import csv

from csv import reader, writer, DictWriter, DictReader
import datetime

with open('autoparkas.csv', encoding='utf8') as failas:
    skaitytojas = DictReader(failas, delimiter=',')
    next(skaitytojas)                   #Neima pirmos eilutes
    skaitytojas = list(skaitytojas)

#1
def unikalus (sarasas):
    automobiliai = {}
    print('\n1. Gamintojų automobiliai, kurių yra daugiau nei vienas:\n')
    for gamintojas in sarasas:
        if gamintojas['Marke'] not in automobiliai:
            automobiliai[gamintojas['Marke']] = 1
        else:
            automobiliai[gamintojas['Marke']] += 1
    for autokey, autovalue in automobiliai.items():
        if(autovalue > 1):
            print(autokey, '- kiekis:', autovalue)

#2

def pasirinktas_auto (sarasas):
    auto = input('\nIrasykite automobilio gamintoja is pateiktu sarase: ')
    print(f'\n2. Pasirinkto automobilio "{auto}" sąrašas:\n')
    pasirinktas = {}
    for gamintojas in sarasas:
        if auto == gamintojas['Marke']:
            if gamintojas['Marke'] not in pasirinktas:
                pasirinktas[gamintojas['Marke']] = [gamintojas]
            else:
                pasirinktas[gamintojas['Marke']].append(gamintojas)

    if len(pasirinktas) == 0:
        print('Tokio gamintojo automobilių sąraše nėra')
    else:
        for i in pasirinktas[auto]:
            print(i)

#3

def senienos (sarasas):
    buvo = False
    metai = datetime.datetime.now().year
    with open('senienos.csv', 'w', encoding='utf8', newline='') as failas:
        stulpeliu_pav = ['Numeriai', 'Marke', 'Modelis', 'Pagaminimo metai', 'Amzius']
        rasytojas = DictWriter(failas, delimiter=',', fieldnames=stulpeliu_pav)
        rasytojas.writeheader()
        for senas in sarasas:
            if metai - int(senas['Pagaminimo metai']) > 10:
                senas['Amzius'] = metai - int(senas['Pagaminimo metai'])
                buvo = True
                rasytojas.writerow(senas)

    if buvo == False:
        with open('senienos.csv', 'w', encoding='utf8', newline='') as failas:
            failas.write('Senesnių nei 10 metų automobilių sąraše nėra')


unikalus(skaitytojas)
pasirinktas_auto(skaitytojas)
senienos(skaitytojas)



