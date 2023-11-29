# Copyright (c) 2023, Vignesh P and contributors
# For license information, please see license.txt
import cv2
import dlib
import face_recognition
import datetime
import numpy as np
from deepface import DeepFace
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file, get_file_path


class EmployeeCheck(Document):
    pass


@frappe.whitelist()
def picture_for_verification(name):
    verification_doc = frappe.get_doc("Employee Check", name)
    verification_image = get_file_path(verification_doc.image_for_verification)
    stored_image_in_db = frappe.get_doc("Employees", name)
    test_image = get_file_path(stored_image_in_db.image)
    
    deepface_result = deep_face(verification_image, test_image)
    cv2_result = face_check(verification_image, test_image)

    # Load the pre-trained face recognition model from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        "/home/vickystreak/frappe-bench/apps/face_attendance/face_attendance/face_attendance/doctype/employee_check/shape_predictor_68_face_landmarks.dat"
    )

    # Load the images
    image_of_person1 = cv2.imread(verification_image)
    image_of_person2 = cv2.imread(test_image)

    # Convert the images to grayscale
    gray_person1 = cv2.cvtColor(image_of_person1, cv2.COLOR_BGR2GRAY)
    gray_person2 = cv2.cvtColor(image_of_person2, cv2.COLOR_BGR2GRAY)

    # Detect faces in the images
    faces_person1 = detector(gray_person1)
    faces_person2 = detector(gray_person2)

    # Encode faces
    face_encoder = dlib.face_recognition_model_v1(
        "/home/vickystreak/frappe-bench/apps/face_attendance/face_attendance/face_attendance/doctype/employee_check/dlib_face_recognition_resnet_model_v1.dat"
    )

    # Get face descriptors
    face_descriptor_person1 = face_encoder.compute_face_descriptor(
        image_of_person1, predictor(gray_person1, faces_person1[0])
    )
    face_descriptor_person2 = face_encoder.compute_face_descriptor(
        image_of_person2, predictor(gray_person2, faces_person2[0])
    )

    # Compare the face descriptors
    distance = np.linalg.norm(
        np.array(face_descriptor_person1) - np.array(face_descriptor_person2)
    )

    # Set a threshold for similarity
    threshold = 0.5
    print("dlib ======================================>", distance)

    # Print the result
    if (
        cv2_result == True
        and distance <= threshold
        and cv2_result == True
        and deepface_result == True
        or deepface_result == True
        and distance <= threshold
    ):
        frappe.msgprint("Face Matched. Attendance is Recorded")
        # attendance_log(verification_doc)
    else:
        frappe.msgprint("Face not matched")


def face_check(verification_image, test_image):
    # Loading the data
    img = face_recognition.load_image_file(verification_image)

    # converting to RGB
    img_converted = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # encoding the image
    encoded_img = face_recognition.face_encodings(img_converted)[0]

    # data stored in dB
    stored_img = face_recognition.load_image_file(test_image)
    stored_img_converted = cv2.cvtColor(stored_img, cv2.COLOR_BGR2RGB)
    encoded_stored_img = face_recognition.face_encodings(stored_img_converted)[0]

    facerecognition_results = face_recognition.compare_faces(
        [encoded_img], encoded_stored_img
    )
    print("facerecognition results =====>  ", facerecognition_results)

    if facerecognition_results[0] == True:
        return True
    else:
        return False


# using deepface
def deep_face(verification_image, test_image):
    models = [
        "VGG-Face",
        "Facenet",
        "Facenet512",
        "OpenFace",
        "DeepFace",
        "DeepID",
        "ArcFace",
        "Dlib",
        "SFace",
    ]
    backends = [
        "opencv",
        "ssd",
        "dlib",
        "mtcnn",
        "retinaface",
        "mediapipe",
        "yolov8",
        "yunet",
        "fastmtcnn",
    ]

    deepface_result1 = DeepFace.verify(
        img1_path=verification_image,
        img2_path=test_image,
        model_name=models[0],
        detector_backend=backends[0],
    )
    print("Deepface model1 result============>", deepface_result1)

    if deepface_result1.get("verified") == True:
        return True
    else:
        return False
    # deepface_result2 = DeepFace.verify(
    #     img1_path=verification_image,
    #     img2_path=test_image,
    #     model_name=models[1],
    #     detector_backend=backends[0],
    # )
    # print("DeepFace model2 result===========>", deepface_result2)

    # if (
    #     facerecognition_results[0] == True
    #     and deepface_result1.get("verified") == True
    #     or facerecognition_results[0] == True
    #     and deepface_result2.get("verified") == True
    #     or deepface_result1.get("verified") == True
    #     and deepface_result2.get("verified") == True
    # ):
    #     frappe.msgprint("Face Matched Attendance is Recorded")


def attendance_log(verification_doc):
    if verification_doc.check == "In":
        checkin_log = frappe.new_doc("Employee CheckIn Log")
        checkin_log.update(
            {
                "employee_name": verification_doc.employee_name,
                "employee_number": verification_doc.employee_number,
                "status": "In",
                "date_and_time": datetime.datetime.now(),
            }
        )
        checkin_log.insert(ignore_permissions=True)
        checkin_log.submit()

    elif verification_doc.check == "Out":
        checkin_log = frappe.new_doc("Employee CheckOut Log")
        checkin_log.update(
            {
                "employee_name": verification_doc.employee_name,
                "employee__number": verification_doc.employee_number,
                "status": "Out",
                "date_and_time": datetime.datetime.now(),
            }
        )
        checkin_log.insert(ignore_permissions=True)
        checkin_log.submit()
    else:
        frappe.msgprint("Face not matched")
