from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import locale
import number
import pyodbc
from datetime import datetime
# import mysql.connector

locale.setlocale(locale.LC_ALL, 'es_Cl.UTF8')

'MySQL Server'
'''myDB = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="yapo_bbdd"
)
myCursor = myDB.cursor()'''

'SQL Server'
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=;'
                      'Database=YapoDB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
now = datetime.now()
print (now.date())

def run_all():

    # CARS
    cursor.execute('SELECT TOP 1 * FROM AutoSamples ORDER BY ID DESC')
    last_date = cursor.fetchall()

    if len(last_date) > 0:
        last_date_object = datetime.strptime(last_date[0][3], '%Y-%m-%d')

        if last_date_object.date() < now.date():
            print('Executing auto scrapper')
            execute_autos()
        elif last_date_object.date() >= now.date():
            print('Cars up to date')
    else:
        execute_autos()

    # REAL STATE
    cursor.execute('SELECT TOP 1 * FROM TerrenoSamples ORDER BY ID DESC')
    last_date = cursor.fetchall()

    if len(last_date) > 0:
        last_date_object = datetime.strptime(last_date[0][4], '%Y-%m-%d')
        if last_date_object.date() < now.date():
            print('Executing real state scrapper')
            execute_terrenos()
        elif last_date_object.date() >= now.date():
            print('Real State up to date')
    else:
        execute_terrenos()


def execute_autos():
    # autos
    baseURL = 'https://www.yapo.cl/chile/autos?ca=8_s&st=s&cg=2020&o='
    max_pages = 870
    for o in range(0, max_pages):

        page = urlopen(Request(baseURL + str(o + 1), headers={'User-Agent': 'Mozilla'}))
        soup = BeautifulSoup(page, 'html.parser')
        entry_trs = soup.find_all('tr', attrs={'class': 'ad listing_thumbs'})

        print('Cars index: ', o, ' of ', max_pages)

        if entry_trs:
            for tr in entry_trs:
                car_id = int(tr['id'])
                td = tr.find('td', attrs={'class': 'thumbs_subject'})
                href = td.find('a')['href']
                brand = td.find('a').text.strip()
                span_price = td.find('span', attrs={'class': 'price'})
                price = 0
                price_unit = "$"

                if span_price:
                    clean_price = span_price.text.strip()
                    price = int(locale.atof(clean_price.strip("$")))

                year = 0
                km = 0
                tx = ""

                div_icons = td.find('div', attrs={'class': 'icons'})
                if div_icons:
                    spans = div_icons.find_all('span', attrs={'class': 'icons__element-text'})
                    if spans:
                        for span in spans:
                            result = span.text.strip()
                            try:
                                year = int(result)
                            except ValueError:
                                if "km" in result:
                                    clean_km = result.replace('km', '')
                                    km = number.parseNumber(clean_km)
                                if "MT" or "AT" in result:
                                    tx = result

                #sql = "INSERT INTO auto_chile (car_id, brand, price, year, km, tx) " \
                #      "VALUES (%s, %s, %s, %s, %s, %s)"
                #val = (car_id, brand, price, year, km, tx)
                #myCursor.execute(sql, val)
                #myDB.commit()

                cursor.execute('SELECT yapo_id FROM Autos where yapo_id = ?', car_id)

                if len(list(cursor)) == 1:
                    cursor.execute("INSERT INTO AutoSamples (yapo_id, price, sample_date) "
                                   "VALUES (?, ?, ?) ", car_id, price, now)

                else:
                    'Create new main entry and add first sample'
                    cursor.execute("INSERT INTO Autos  (yapo_id, href, brand, year, km, tx) "
                                   "VALUES (?, ?, ?, ?, ?, ?) ", car_id, href, brand, year, km, tx)
                    cursor.execute("INSERT INTO AutoSamples  (yapo_id, price, sample_date) "
                                   "VALUES (?, ?, ?) ", car_id, price, now)

                conn.commit()


def execute_terrenos():
    # terrenos
    baseURL = 'https://www.yapo.cl/chile/comprar?ca=8_s&ret=5&cg=1220&o='
    max_pages = 251
    for o in range(max_pages):

        page = urlopen(Request(baseURL + str(o + 1), headers={'User-Agent': 'Mozilla'}))
        soup = BeautifulSoup(page, 'html.parser')
        entry_trs = soup.find_all('tr', attrs={'class': 'ad listing_thumbs'})

        print('Real State index: ', o, ' of ', max_pages - 1)

        if entry_trs:
            for tr in entry_trs:
                terreno_id = int(tr['id'])
                td_a = tr.find('td', attrs={'class': 'thumbs_subject'})
                href = td_a.find('a')['href']
                title = td_a.find('a').text.strip()
                span_price = td_a.find('span', attrs={'class': 'price'})
                price = 0
                price_unit = "$"

                if span_price:
                    clean_price = span_price.text.strip()
                    if "UF" in clean_price:
                        price_unit = "UF"
                    clean_price = clean_price.replace('UF ', '')
                    clean_price = clean_price.replace('$ ', '')
                    price = number.parseNumber(clean_price)

                span_sq_meters = td_a.find('div', attrs={'class': 'icons__element'})
                measurement = 0
                measurement_unit = "m2"
                if span_sq_meters:
                    meters = span_sq_meters.find_all('span', attrs={'class': 'icons__element-text'})
                    if meters:
                        for meter in meters:
                            clean_measurement = meter.text.strip()
                            if "ha" in clean_measurement:
                                measurement_unit = "ha"
                            clean_measurement = clean_measurement.replace('ha', '')
                            clean_measurement = clean_measurement.replace('m2', '')
                            measurement = number.parseNumber(clean_measurement)

                td_b = tr.find('td', attrs={'class': 'clean_links'})
                region = ""
                commune = ""
                reg = td_b.find('span', attrs={'class': 'region'})
                if reg:
                    region = reg.text.strip()
                com = td_b.find('span', attrs={'class': 'commune'})
                if com:
                    commune = com.text.strip()

                #print(terreno_id, href, title, price, price_unit, measurement, measurement_unit, region, commune)

                #sql = "INSERT INTO terreno_chile (terreno_id, href, title, price, price_unit, " \
                #      "measurement, measurement_unit, region, commune) " \
                #      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #val = (terreno_id, href, title, price, price_unit, measurement, measurement_unit, region, commune)
                #myCursor.execute(sql, val)
                #myDB.commit()

                cursor.execute('SELECT yapo_id FROM Terrenos where yapo_id = ?', terreno_id)

                if len(list(cursor)) == 1:
                    cursor.execute("INSERT INTO TerrenoSamples (yapo_id, price, unit, sample_date) "
                                   "VALUES (?, ?, ?, ?) ", terreno_id, price, price_unit, now)

                else:
                    'Create new main entry and add first sample'
                    cursor.execute("INSERT INTO Terrenos  (yapo_id, href, title, measurements, unit, region, commune) "
                                   "VALUES (?, ?, ?, ?, ?, ?, ?) ", terreno_id, href, title, measurement, measurement_unit, region, commune)
                    cursor.execute("INSERT INTO TerrenoSamples  (yapo_id, price, unit, sample_date) "
                                   "VALUES (?, ?, ?, ?) ", terreno_id, price, price_unit, now)
                conn.commit()


run_all()
