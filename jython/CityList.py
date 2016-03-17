import csv
import sys

class CityList:
    def __init__(self):
        self.cities = []
        self.initCities()
    def getCoords(self, index):
        return [self.cities[index][0], self.cities[index][1]]
    def initCities(self):
        self.cities.append([-84.3900, 33.7550, 'Atlanta', 'GA'])
        self.cities.append([-118.2500, 34.0500, 'Los Angeles', 'CA'])
        self.cities.append([-122.3331, 47.6097, 'Seattle', 'WA'])
        self.cities.append([-74.0059, 40.7127, 'New York City', 'NY'])
        self.cities.append([-77.0164, 38.9047, 'Washington DC', ''])
        self.cities.append([-89.9711, 35.1174, 'Memphis', 'TN']) #memphis
        self.cities.append([-80.2089, 25.7753, 'Miami', 'FL']) #mia
        self.cities.append([-87.6847, 41.8369, 'Chicago', 'IL']) #chi
        self.cities.append([-83.0458, 42.3314, 'Detroit', 'MI']) #detroit
        self.cities.append([-75.1667, 39.9500, 'Philadelphia', 'PA']) #phil
        self.cities.append([-80.8966, 34.0298, 'Columbia', 'SC']) #columbia,sc
        self.cities.append([-76.2000, 36.9167, 'Norfolk', 'VA']) #norfolk
        self.cities.append([-76.6167, 39.2833, 'Baltimore', 'MD']) #baltimore
        self.cities.append([-90.0667, 29.9500, 'New Orleans', 'LA']) #nola
        self.cities.append([-96.7970, 32.7767, 'Dallas', 'TX']) #dallas
        self.cities.append([-95.3698, 29.7604, 'Houston', 'TX']) #houston
        self.cities.append([-90.1978, 38.6272, 'Saint Louis', 'MO']) #stl
        self.cities.append([-74.2624, 40.7915, 'Jersey City', 'NJ']) #nnj
        self.cities.append([-121.4689, 38.5556, 'Sacramento', 'CA']) #sac
        self.cities.append([-122.4167, 37.7833, 'San Francisco', 'CA']) #sfo
        self.cities.append([-80.8433, 35.2269, 'Charlotte', 'NC']) #clt
        self.cities.append([-157.8167, 21.3000, 'Honolulu', 'HI']) #hon
        self.cities.append([-81.6697, 41.4822, 'Cleveland', 'OH']) #cleveland
        self.cities.append([-115.1739, 36.1215, 'Las Vegas', 'NV']) #vegas
        self.cities.append([-87.9500, 43.0500, 'Milwaukee', 'WI']) #milwaukee
        self.cities.append([-86.1480, 39.7910, 'Indianapolis', 'IN']) #indy
        self.cities.append([-86.2792, 32.3617, 'Montgomery', 'AL']) #montgomery
        self.cities.append([-86.8130, 33.5250, 'Birmingham', 'AL']) #birmingham
        self.cities.append([-90.1847, 32.2989, 'Jackson', 'MS']) #jackson ms
        self.cities.append([-72.9236, 41.3100, 'New Haven', 'CT']) #new haven
        self.cities.append([-77.4667, 37.5333, 'Richmond', 'VA']) #richmond
        self.cities.append([-96.0000, 41.2500, 'Omaha', 'NE']) #omaha
        self.cities.append([-77.4111, 39.4139, 'Frederick', 'MD']) #frederick, md
        self.cities.append([-81.6614, 30.3369, 'Jacksonville', 'FL']) #jax
        self.cities.append([-81.2989, 28.4158, 'Orlando', 'FL']) #orl
        self.cities.append([-84.2533, 30.4550, 'Tallahassee', 'FL']) #tallahassee
        self.cities.append([-85.7667, 38.2500, 'Louisville', 'KY']) #louisville
        self.cities.append([-75.9117, 42.1022, 'Binghampton', 'NY']) #binghampton
    def __len__(self):
        return len(self.cities)
    def makeCities(self):
        fileName = 'data/TravelingSalesProblem/' + 'TSP_cities_DB.csv'
        with open(fileName, 'wb') as f:
            fileWriter = csv.writer(f,delimiter=',')
            fileWriter.writerow(['Latitude', 'Longitude', 'City', 'State']) # column header
            for city in self.cities:
                fileWriter.writerow(city)
        print "Wrote city database to " + fileName
