import base64
import cv2
import mysql.connector


connection = mysql.connector.connect(host=host,user = user, password = password, database = database)
cursor = connection.cursor()

images = "SELECT Image FROM user_face.user "
classes =  "SELECT Name FROM user_face.user "

img = []
name = []
#convert data to str
file = (images)
a = file.encode()
data_to_img =  base64.b64decode(a)

for i in data_to_img,classes:
    image =  cv2.imread(data_to_img)
    img.append(image)
    name.append(classes)
