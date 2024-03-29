import pandas as pd
import unicodedata
import pandas as py, pygame, matplotlib.pyplot as plt, time
pd.options.mode.chained_assignment = None
import threading, numpy as np

# self.worldCities, contains the information of the cities of the world

class Map():
    def __init__(self, countryName, citiesPerState = 1, verbose = False, mapsFile = "./RBFS/worldcities.csv"):
        self.worldCities = py.read_csv(mapsFile, usecols=['city', 'lat', 'lng', 'country', 'admin_name'])
        self.initialize(countryName, citiesPerState)
        self.countryName = countryName
        if verbose : self.seeAllData()
        self.maxPath = 0
        self.currentVisitedNode = ""
    
    def resetAllStates(self):
        self.map['state'] = 'closed'
    
    def seeAllData(self):
        print("SEEING ALL DATA")    
        for i in range(self.map.shape[0]-1):
            print(f"State: {self.map.loc[i+1]['admin_name']}, City: {self.map.loc[i+1]['city']}")
    
    def initialize(self, countryName, citiesPerState):
        self.map = self.createCountryDF(countryName)
        self.changeCitiesPerState(citiesPerState)

    def createCountryDF(self, countryName):
        countryDF = self.worldCities.copy()
        countryDF = countryDF[countryDF['country'] == countryName]
        countryDF = countryDF[countryDF['admin_name'] != 'Baja California Sur']
        countryDF['state'] = 'closed'
        countryDF = countryDF.reset_index(drop=True)
        return countryDF
    
    def changeCitiesPerState(self, citiesPerState):
        if citiesPerState != -1:
            self.map = self.map.groupby('admin_name').head(citiesPerState)
        self.map = self.map.reset_index(drop=True)

    def visualizeData(self, number=10):
        print("Info of map", self.map[0].head(number), sep="\n")    

    def updateState(self, city, state):
        self.map['state'].loc[self.map['city'] == city] = state
    
    def getCoordinates (self, city):
        city = self.map.loc[self.map['city'] == city]
        return (city['lat'].values[0], city['lng'].values[0])
    
    def getEuclideanDistance(self, city1Name, city2Name):
        city1 = self.map.loc[self.map['city'] == city1Name]
        city2 = self.map.loc[self.map['city'] == city2Name]

        lat1 = float(city1['lat'].values[0])
        lng1 = float(city1['lng'].values[0])
        lat2 = float(city2['lat'].values[0])
        lng2 = float(city2['lng'].values[0])

        # distance = ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5
        distance = np.hypot((lng2 - lng1), (lat2 - lat1))
        distance = round(distance, 2)

        return distance
    
    def playVisualization(self, sleepTime = 2):
        pygame.init()

        # Define colors
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        black = (0, 0, 0)
        gray = (200, 200, 200)
        white = (255, 255, 255)
        
        font = pygame.font.Font(None, 36)
        titleText = font.render(f"{self.countryName}'s Map", True, black)
        visitedNodeText = font.render("Visited Node:", True, black)

        # Set the width and height of the screen
        screenWidth = 1200
        screenHeight = 800
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        pygame.display.set_caption(f"{self.countryName} Map Visualization")

        textWidth = titleText.get_width()
        textHeight = titleText.get_height()
        
        screenWidth *= .9
        screenHeight *= .9
        # Scale the latitude and longitude values to fit the screen
        min_lat = self.map['lat'].min()
        max_lat = self.map['lat'].max()
        min_lng = self.map['lng'].min()
        max_lng = self.map['lng'].max()

        scaled_lat = (self.map['lat'] - min_lat) / (max_lat - min_lat) * screenHeight
        print("Info", type(scaled_lat))

        scaled_lng = (self.map['lng'] - min_lng) / (max_lng - min_lng) * screenWidth
        scaled_lat = screenHeight - scaled_lat
        # Game loop
        running = True

        counter = 0
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill(white)

            # Draw the points
            for lat, lng, state in zip(scaled_lat + screenWidth/10, scaled_lng + screenHeight/10, self.map['state']):
                match (state):
                    case "open":
                        color = red
                    case "closed":
                        color = black
                    case "frontier":
                        color = blue
                    case _:
                        color = gray
                pygame.draw.circle(screen, color, (int(lng), int(lat)), 8)

            # Update the screen
            textX = (screenWidth - textWidth) // 2
            textY = 20
            screen.blit(titleText, (textX, textY))

            textY = 40
            screen.blit(visitedNodeText, (40, textY))

            visitedNodeText = font.render("Visited Node: " + str(counter), True, black)
            counter += 1
            if(counter%2 == 0):
                self.updateState('Mexico City', 'closed')
            else:
                self.updateState('Mexico City', 'frontier')

            pygame.display.flip()

            # time.sleep(sleepTime)
            # print("Slept")
        # Quit Pygame
        pygame.quit()
    

    def runVisualization(self):
        self.playVisualization()
        # visualization_thread = threading.Thread(target=self.playVisualization)
        # visualization_thread.start()

# map = Map("Mexico", 1)
# map.playVisualization()