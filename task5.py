import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import pickle

FACE_DB_PATH = "face_db.pkl"
CONFIDENCE_THRESHOLD = 0.6  

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

if os.path.exists(FACE_DB_PATH):
    with open(FACE_DB_PATH, 'rb') as f:
        face_db = pickle.load(f)
else:
    face_db = {}

def save_face_db():
    with open(FACE_DB_PATH, 'wb') as f:
        pickle.dump(face_db, f)

def register_mode():
    name = input("Enter name to register: ")
    if name in face_db:
        choice = input("Name already exists. Overwrite? (y/n): ")
        if choice.lower() != 'y':
            return

    cap = cv2.VideoCapture(0)
    print("[INFO] Capturing face. Please stay still...")

    embeddings = []
    frame_count = 0
    max_frames = 10

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        faces = app.get(frame)
        if faces:
            embedding = faces[0].embedding
            embeddings.append(embedding)
            frame_count += 1
            box = faces[0].bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"Captured: {frame_count}/{max_frames}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Registration cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    if embeddings:
        avg_embedding = np.mean(embeddings, axis=0)
        face_db[name] = avg_embedding
        save_face_db()
        print(f"[INFO] Face for '{name}' registered successfully.")


from numpy.linalg import norm

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b) + 1e-6)

def recognize_mode():
    if not face_db:
        print("[ERROR] No registered faces found. Please register first.")
        return

    cap = cv2.VideoCapture(0)
    print("[INFO] Press 'q' to quit.")

    names = list(face_db.keys())
    embeddings = np.array(list(face_db.values()))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        faces = app.get(frame)
        for face in faces:
            box = face.bbox.astype(int)
            embedding = face.embedding

            sims = [cosine_similarity(embedding, e) for e in embeddings]
            best_idx = np.argmax(sims)
            best_sim = sims[best_idx]

            accuracy = best_sim * 100
            if best_sim > 0.4: 
                label = f"{names[best_idx]} ({accuracy:.2f}%)"
            else:
                label = "Unknown"

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    while True:
        print("\n===== Face Recognition System =====")
        print("1. Register New Face")
        print("2. Recognize Faces")
        print("3. Exit")
        choice = input("Choose option (1/2/3): ")

        if choice == '1':
            register_mode()
        elif choice == '2':
            recognize_mode()
        elif choice == '3':
            print("[INFO] Exiting system.")
            break
        else:
            print("[ERROR] Invalid choice. Please enter 1, 2, or 3.")
