# Copyright (c) 2023, Vignesh P and contributors
# For license information, please see license.txt
import cv2
import face_recognition
import datetime
# import numpy as np
import frappe
from frappe.model.document import Document
# from PIL import Image
from frappe.utils.file_manager import get_file, get_file_path
class EmployeeCheck(Document):
	pass

@frappe.whitelist()
def picture_for_verification(check,name):
	
	# date_and_time = datetime.datetime.now()
	# str_date_and_time = date_and_time.strftime("%d-%m-%Y, %H:%M:%S")
	verification_doc = frappe.get_doc("Employee Check",name)
	verification_image = get_file_path(verification_doc.image_for_verification)
	stored_image_in_db = frappe.get_doc("Employees",name)
	test_image = get_file_path(stored_image_in_db.image) 
 
	if verification_image == "":
		frappe.msgprint("Please Upload the Image or Take photo in Camera")
	elif verification_image != "":
		# first loading the data
		img = face_recognition.load_image_file(verification_image)
		# converting to rgb
		img_converted =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		#  location of the face needed for the square appeareance around the face while getting the data from camera
		img_face_loc = face_recognition.face_locations(img_converted)[0]
		# encoding the image
		encoded_img = face_recognition.face_encodings(img_converted)[0]
		print(encoded_img)
	
   
		# data stored in db
		stored_img = face_recognition.load_image_file(test_image)
		stored_img_converted = cv2.cvtColor(stored_img,cv2.COLOR_BGR2RGB)
		stored_img_loc = face_recognition.face_locations(stored_img_converted)
		# print("stored face location =====> ",stored_img_loc)
		encoded_stored_img = face_recognition.face_encodings(stored_img_converted)[0]
		print(encoded_stored_img)
	
		results = face_recognition.compare_faces([encoded_img],encoded_stored_img)
		# print("results =====>  ",results)
		if results[0] == True:
			frappe.msgprint("Face Matched Attendance is Recorded")
			print("results =====>  ",results)
			if verification_doc.check == 'In':
				print("working +++=============>>>>>>>>>>>>")
				checkin_log = frappe.new_doc("Employee CheckIn Log")
				checkin_log.update({
					"employee_name" : verification_doc.employee_name,
					"employee_number" : verification_doc.employee_number,
     				"status" : "In",
					"date_and_time" :datetime.datetime.now()
     			})
				checkin_log.insert(ignore_permissions=True)
				checkin_log.submit()
				# print(datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
			elif verification_doc.check == 'Out':
				checkin_log = frappe.new_doc("Employee CheckOut Log")
				checkin_log.update({
					"employee_name" : verification_doc.employee_name,
					"employee__number" : verification_doc.employee_number,
     				"status" : "Out",
					"date_and_time" :datetime.datetime.now()
     			})
				checkin_log.insert(ignore_permissions=True)
				checkin_log.submit()
		elif results[0] == False:
			frappe.msgprint("Face not matched")

	
	
	# trainedDataset = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	# # video = cv2.VideoCapture(0)
	# while True:
	# 	success,frame = video.read()
	# 	if success==True:
	# 		gray_video = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	# 		faces = trainedDataset.detectMultiScale(gray_video)
	# 		for x,y,w,h in faces:
	# 			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
	# 		cv2.imshow('video',frame)
	# 		key = cv2.waitKey(1)
	# 		if key == 81 or key == 113:
	# 			break
	# 	else:
	# 		print("Video Completed or frame Nill")
	# 		break
	# print("click")
	# ret, frame = video.read()
	# # return {"message": "Image captured successfully"}
 
	# picture_stored = frappe.get_doc("Employees",check)
	# exited_picture = picture_stored.get("image")
	# exited_picture_bytes = exited_picture.encode('utf-8')  # Encode the string to bytes
	# exited_picture_array = cv2.imdecode(np.frombuffer(exited_picture_bytes, np.uint8), -1)

	# exited_picture_array = cv2.imdecode(np.frombuffer(exited_picture, np.uint8), -1)
	# if exited_picture is not None and len(exited_picture) > 0:
	# 	cv2.imshow('Picture', exited_picture)
  

	# cv2.imshow('Picture',exited_picture)
 	# # pass
	# img = Image.open(exited_picture)
	# img.show()
