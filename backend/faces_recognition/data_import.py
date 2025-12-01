import os
import numpy as np
from pymongo import MongoClient
import face_recognition

uri = "mongodb+srv://data_team:ktmt@facereccluster.hjfd7ad.mongodb.net/?retryWrites=true&w=majority&appName=FaceRecCluster"
client = MongoClient(uri)
db = client['FaceRecProject']
collection = db['PeopleMetadata']

current_dir = os.path.dirname(os.path.abspath(__file__))
image_stored = os.path.join(current_dir, "Demo_Final_Images")

def update_vectors():
    documents = collection.find({})
    count = 0
    for doc in documents:
        doc_id = doc['_id']
        relative_path = doc['File_Path_Demo']
        full_image_path = os.path.join(image_stored, relative_path)

        if os.path.exists(full_image_path):
            try:
                image = face_recognition.load_image_file(full_image_path)
                all_faces = face_recognition.face_encodings(image)

                if len(all_faces) > 0:
                    face_vector = all_faces[0]
                    result_vector = face_vector.tolist()
                    #print(result_vector)
                    collection.update_one(
                        {'_id': doc_id},
                        {'$set': {'feature_vector': result_vector}}
                    )
                    print(f"Updated: {doc['Ten']}")
                    count += 1
                else:
                    print(f"No face found: {doc['Ten']}")
            except Exception as e:
                print(f"Error {doc['Ten']}: {e}")
        else:
            print(f"Path not found: {full_image_path}")

    print(f"Done. Updated {count} documents.")

if __name__ == "__main__":
    update_vectors()