import csv
import json
from datetime import datetime
"""
# JPeZlL4HJfU,HcyeaHxtVpg,UNK,UNK,UNK,UNK,UNK,UNK,UNK,UNK

"""
class VideoData:
  def __init__(self, id, description, thumbnail, title, genre, noID):
    self.id = id
    self.genre = genre
    self.thumbnail = thumbnail
    self.description = description
    self.title = title
    self.noID = noID
    # 01/06/2022 18:05:14

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

VideoArray = []
dateArray = []

switcher = {
  "Kuliner": 2,
  "Homecare": 3,
  "Healthcare": 4,
  "Tutorial": 1,
  "Ecommerce": 5,
  "Marketing": 7,
  "Review": 6
}

with open('data.csv', encoding="utf-8") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=';')
  line_count = 0
  id = 1
  for row in csv_reader:
    dateArray.append(datetime.strptime(row[5], "%d/%m/%Y %H:%M:%S"))
    tempVidData = VideoData(row[0], row[1], row[2], row[3], row[4], id)
    id += 1
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

  for element in array:
    returnValue.append(switcher.get(element,0))

  return returnValue
    

def genreConcat(array):
  returnValue = []
  for element in array:
    returnValue.extend(genreSplice(getGenre(element)))
  len_genre = (len(returnValue))
  print(len_genre)

  
  if len_genre < 20:
    for i in range(len_genre,20):
      returnValue.append("UNK")
  print(returnValue)
  return genretoInt(returnValue[:21])

def getDetails(array):
  datas = []
  # str = "["
  # i = 0
  # for element in array:
  #   if i != 0:
  #     str += ","
  #   str += VideoArray[element-1].toJSON()
  #   i += 1
  # str += "]" 
  for e in array:
    datas.append(VideoArray[e-1])
  # print(VideoArray[e-1].toJSON())
  return datas

def sortArray(array):
  for i in range(len(array)):
    for j in range(0, len(array) - i - 1):
      if dateArray[array[j] - 1]< dateArray[array[j + 1] - 1]:
        temp = array[j]
        array[j] = array[j + 1]
        array[j + 1] = temp

def genreFilter(genre):
  returnValue = []
  for element in VideoArray:
    x = genreSplice(element.genre)
    genrePresent = False
    for i in x:
      if switcher.get(i, 0) == genre:
        genrePresent = True
    if genrePresent:
      returnValue.append(element.noID)

  sortArray(returnValue)  
  return returnValue

def getDates(array):
  for element in array:
    print(VideoArray[element - 1].uploadTime)

# print(genreFilter(4))