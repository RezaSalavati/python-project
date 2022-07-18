import mysql.connector
import requests
from bs4 import BeautifulSoup
from sklearn import tree

cnx = mysql.connector.connect(user='root', password='reza', host='127.0.0.1', database='car2')
cursor = cnx.cursor()
for page in range(0, 2):
    url = 'https://www.truecar.com/used-cars-for-sale/listings/?page=%s' % format(page)
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    all_objects = soup.find_all('div', attrs={'class': "linkable card card-shadow vehicle-card _1qd1muk"})
    for object in all_objects:
        name = object.find('span', attrs={'class': "vehicle-header-make-model text-truncate"}).text
        yearOfBuild = object.find('span', attrs={'class': "vehicle-card-year font-size-1"}).text
        yearOfBuild = int(yearOfBuild)
        price = object.find('div', attrs={'class': "heading-3 margin-y-1 font-weight-bold"}).text.replace('$', '')
        vehicleMileage = object.find('div', attrs={"data-test": "vehicleMileage"}).text.replace('miles', '')
        cursor.execute('INSERT INTO info VALUES (\'%s\',\' %s\' ,\'%s\',\' %s\' )' % (
            name, yearOfBuild, price, vehicleMileage))
        cnx.commit()
query = 'SELECT * FROM info;'
cursor.execute(query)
x = []
y = []
for (name, yearOfBuild, price, vehicleMileage) in cursor:
    price = price.replace(',', '.').strip()
    vehicleMileage = vehicleMileage.replace(',', '.').strip()
    l = []
    l.append(float(vehicleMileage))
    l.append(float(yearOfBuild))
    x.append(l)
    y.append(price)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
p = input()
y = input()
new_data = [[p, y]]
answer = clf.predict(new_data)
print(float(answer))

cnx.close()
