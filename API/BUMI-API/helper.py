import csv
import json

class VideoData:
  def __init__(self, id, description, thumbnail, title, genre):
    self.id = id
    self.genre = genre
    self.thumbnail = thumbnail
    self.description = description
    self.title = title

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

VideoArray = []

with open('data.csv', encoding="utf-8") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=';')
  line_count = 0
  for row in csv_reader:
    tempVidData = VideoData(row[0], row[1], row[2], row[3], row[4])
    VideoArray.append(tempVidData)

def getGenre(id):
  return VideoArray[id-1].genre

def getID(id):
  return VideoArray[id-1].id

def genreSplice(genre):
  x = genre.split("|")
  return x

def genretoInt(array):
  returnValue = []
  switcher = {
    "Kuliner": 2,
    "Homecare": 3,
    "Healthcare": 4,
    "Tutorial": 1,
    "Ecommerce": 5,
    "Marketing": 7,
    "Review": 6
  }

  for element in array:
    returnValue.append(switcher.get(element, 0))

  return returnValue
    

def genreConcat(array):
  returnValue = []
  for element in array:
    x = genreSplice(getGenre(element))
    returnValue += x

  returnValue.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
  return genretoInt(returnValue[:20])

def getDetails(array):
  str = "["
  i = 0
  for element in array:
    if i != 0:
      str += ","
    str += VideoArray[element-1].toJSON()
    i += 1
  str += "]" 
  return str

# inputArray = [1, 2, 3, 4, 5]

# print(getDetails(inputArray))