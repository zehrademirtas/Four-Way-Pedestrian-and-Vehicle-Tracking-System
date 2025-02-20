import cv2
import numpy as np

video_path = r"C:\Users\zehra\OneDrive\Desktop\Train.mp4"

cap = cv2.VideoCapture(video_path)

fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

tracked_nesneler = {}
next_object_id = 0
yaya_sayisi = 0
tasit_sayisi = 0
fps = cap.get(cv2.CAP_PROP_FPS)
frame_time = 1 / fps

min_contour_area = 1500
mesafe_esigi = 50
min_hiz = 0.5
yaya_boyutu = (15, 60)
tasit_boyutu = (40, 25)

min_frame_sayisi = 5
min_stabil_frame = 5
max_kayip_frame = 15
max_mesafe = 200

def hiz_hesapla(eski_merkez, yeni_merkez):
    mesafe = np.linalg.norm(np.array(yeni_merkez) - np.array(eski_merkez))
    return mesafe / frame_time

def nesne_siniflandir(w, h, hiz):
    if hiz > min_hiz:
        if h > w and h >= yaya_boyutu[1]:
            return "Yaya"
        elif w >= tasit_boyutu[0] and h >= tasit_boyutu[1]:
            return "Tasit"
    return "Bilinmiyor"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    current_nesneler = {}
    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        merkez = (x + w // 2, y + h // 2)

        eslesen_id = None
        for nesne_id, nesne_data in tracked_nesneler.items():
            eski_merkez = nesne_data["center"]
            mesafe = np.linalg.norm(np.array(merkez) - np.array(eski_merkez))

            if mesafe < mesafe_esigi:
                eslesen_id = nesne_id
                break

        if eslesen_id is None:
            eslesen_id = next_object_id
            next_object_id += 1
            tracked_nesneler[eslesen_id] = {
                "center": merkez,
                "bbox": (x, y, w, h),
                "speed": 0,
                "frames": 0,
                "label": None,
                "counted": False,
                "lost_frames": 0
            }
        else:
            nesne_data = tracked_nesneler[eslesen_id]
            hiz = hiz_hesapla(nesne_data["center"], merkez)
            nesne_data["speed"] = hiz
            nesne_data["center"] = merkez

            if nesne_data["label"] is None:
                label = nesne_siniflandir(w, h, hiz)
                nesne_data["label"] = label

            label = nesne_data["label"]
            nesne_data["frames"] += 1

            if nesne_data["frames"] >= min_frame_sayisi and not nesne_data["counted"]:
                if label == "Yaya":
                    nesne_data["counted"] = True
                    yaya_sayisi += 1
                elif label == "Tasit":
                    nesne_data["counted"] = True
                    tasit_sayisi += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {hiz:.2f} px/s", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        current_nesneler[eslesen_id] = tracked_nesneler[eslesen_id]

    for nesne_id in list(tracked_nesneler.keys()):
        if nesne_id not in current_nesneler:
            tracked_nesneler[nesne_id]["lost_frames"] += 1
            tracked_nesneler[nesne_id]["frames"] = 0

            if tracked_nesneler[nesne_id]["lost_frames"] > max_kayip_frame:
                del tracked_nesneler[nesne_id]

    cv2.imshow("Tracked Objects", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"Tüm Yaya Sayisi: {yaya_sayisi}")
print(f"Tüm Tasit Sayisi: {tasit_sayisi}")

cap.release()
cv2.destroyAllWindows()
