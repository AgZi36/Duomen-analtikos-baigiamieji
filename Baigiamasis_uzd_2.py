import sqlite3
import matplotlib
from matplotlib import pyplot as plt

conn = sqlite3.connect("saldainiu_DB.db")
c = conn.cursor()

#1

with conn:
    c.execute("CREATE TABLE IF NOT EXISTS saldainiai (Pavadinimas text, Tipas text, Kaina_kg float,\
    Perkamas_kiekis integer, Kaina float)")

#2

saldainiu_sarasas = [
    ("Aurora", "Kokosinis", 4, 10),
    ("Rūpintojė", "Karamelinis", 3, 15),
    ("Saulutė", "Bravorinis", 5, 8),
    ("Žiema", "Saldainių", 7, 12),
    ("Vėjopatis", "Likerinis", 8, 6),
    ("Gintarinė", "Agurkinis", 2, 20),
    ("Kukurūzai", "Želė", 6, 10),
    ("Šaltibarščiai", "Šokoladinis", 4, 18),
    ("Medus", "Bandelių", 5, 14),
    ("Lietuviškas Skonis", "Riešutų", 7, 7),
    ("Šokoladinė Puokštė", "Šokoladinis", 3, 25),
    ("Širdies Šokoladas", "Šokoladinis", 4, 15)
]


# c.executemany('INSERT OR REPLACE INTO saldainiai (Pavadinimas, Tipas, Kaina_kg, Perkamas_kiekis) VALUES\
# (?, ?, ?, ?)', saldainiu_sarasas)
#
# with conn:
#     c.execute("SELECT * FROM saldainiai")

print('2.')
for s in c.execute(f"SELECT * from saldainiai").fetchall():
    print(s)

print()

#3

c.execute(f"UPDATE saldainiai SET Kaina = Kaina_kg * Perkamas_kiekis")

print('3.')
for s in c.execute(f"SELECT * from saldainiai").fetchall():
    print(s)

print()

#4

print('4.')

sarasas = c.execute("SELECT * From saldainiai WHERE Tipas = 'Šokoladinis' and Kaina_kg > 5 ").fetchall()
if len(sarasas) == 0:
    print('Saldainių atitinkančių sąlyga nėra')
else:
    print(sarasas)

print()

for s in c.execute(f"SELECT * from saldainiai").fetchall():
    print(s)

print()

#5

print('5.')

naikinti = input('Įveskite saldainio pavadinimą, kurį norite pašalinti iš lentelės: ')

x = c.execute(f"SELECT * from saldainiai WHERE Pavadinimas = '{naikinti}'").fetchall()
if len(x) == 0:
    print('Saldainio tokiu paavdinimu lentelėje nėra')
else:
    c.execute(f"DELETE from saldainiai WHERE Pavadinimas = '{naikinti}'")

for s in c.execute(f"SELECT * from saldainiai").fetchall():
    print(s)

#7

data = c.execute(f"SELECT * from saldainiai").fetchall()
saldainiu_pavadinimas = []
for i in data:
    saldainiu_pavadinimas.append(i[0])

kaina_kg = []
for i in data:
    kaina_kg.append(i[2])

plot1 = plt.figure(1)
plt.bar(saldainiu_pavadinimas, kaina_kg)

plt.title("Saldainiai/kaina_kg")  #pavadinimai
plt.xlabel("Saldainiai")
plt.ylabel("Kaina_kg")
plt.xticks(rotation=90)

saldainiu_tipas = []
for i in c.execute(f"SELECT DISTINCT Tipas from saldainiai ").fetchall():
    saldainiu_tipas.append(i[0])

parduodamas_kiekis = []
for tipas in saldainiu_tipas:
    kiekis = c.execute(f"SELECT sum(Perkamas_kiekis) from saldainiai WHERE Tipas = '{tipas}' group by Tipas ").fetchall()
    parduodamas_kiekis.append(kiekis[0][0])

plot1 = plt.figure(2)
plt.pie(
    parduodamas_kiekis,
    labels = saldainiu_tipas,
    autopct ='%1.1f%%',
    explode =(0,0,0,0,0,0.1,0),
    startangle = 90,
    shadow = True
)
plt.title("Saldainių tipų pardavimai %")  #pavadinimai

plt.show()
conn.commit()
conn.close()