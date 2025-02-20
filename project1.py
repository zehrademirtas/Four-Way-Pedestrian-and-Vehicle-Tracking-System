import cv2
import numpy as np

video_yolu = r"C:\Users\zehra\OneDrive\Desktop\Train.mp4"
cap = cv2.VideoCapture(video_yolu)

fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

min_contour_alani = 1500
yaya_boyut = (15, 60)
arac_boyut = (40, 25)

cizim_yapiliyor = False
baslangic_noktasi = None
bitis_noktasi = None
yaya_yollari = []
arac_yollari = []
mod = None

def nesne_siniflandir(boy, yukseklik):
    if yukseklik > boy and yukseklik >= yaya_boyut[1]:
        return "Yaya"
    elif boy >= arac_boyut[0] and yukseklik >= arac_boyut[1]:
        return "Arac"
    return "Bilinmiyor"

def alanda_mi(center, alanlar):
    for (x1, y1), (x2, y2) in alanlar:
        if x1 <= center[0] <= x2 and y1 <= center[1] <= y2:
            return True
    return False

def dikdörtgen_ciz(event, x, y, flags, param):
    global cizim_yapiliyor, baslangic_noktasi, bitis_noktasi, yaya_yollari, arac_yollari, mod
    if event == cv2.EVENT_LBUTTONDOWN:
        cizim_yapiliyor = True
        baslangic_noktasi = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if cizim_yapiliyor:
            bitis_noktasi = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        cizim_yapiliyor = False
        bitis_noktasi = (x, y)
        if mod == 'yaya':
            yaya_yollari.append((baslangic_noktasi, bitis_noktasi))
        elif mod == 'Arac':
            arac_yollari.append((baslangic_noktasi, bitis_noktasi))

cv2.namedWindow("Ihlal Tespiti")
cv2.setMouseCallback("Ihlal Tespiti", dikdörtgen_ciz)

video_duraklatildi = False
kaydedilen_frame = None

while cap.isOpened():
    if not video_duraklatildi:
        ret, frame = cap.read()
        if not ret:
            break
        kaydedilen_frame = frame.copy()
    else:
        frame = kaydedilen_frame.copy()

    fgmask = fgbg.apply(frame)
    konturlar, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for kontur in konturlar:
        if cv2.contourArea(kontur) < min_contour_alani:
            continue

        x, y, w, h = cv2.boundingRect(kontur)
        center = (x + w // 2, y + h // 2)
        etiket = nesne_siniflandir(w, h)

        if etiket == "Yaya":
            renk = (0, 255, 0)
        elif etiket == "Arac":
            renk = (255, 0, 0)
        else:
            continue

        if etiket == "Yaya" and not alanda_mi(center, yaya_yollari):
            renk = (0, 0, 255)
            cv2.putText(frame, "Ihlal: Yaya", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif etiket == "Arac" and not alanda_mi(center, arac_yollari):
            renk = (0, 0, 255)
            cv2.putText(frame, "Ihlal: Arac", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.rectangle(frame, (x, y), (x + w, y + h), renk, 2)

    for (x1, y1), (x2, y2) in yaya_yollari:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    for (x1, y1), (x2, y2) in arac_yollari:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

    cv2.imshow("Ihlal Tespiti", frame)

    tus = cv2.waitKey(1) & 0xFF
    if tus == ord('q'):
        break
    elif tus == ord('1'):
        mod = 'yaya'
        video_duraklatildi = True
    elif tus == ord('2'):
        mod = 'Arac'
        video_duraklatildi = True
    elif tus == ord('r'):
        video_duraklatildi = False  

cap.release()
cv2.destroyAllWindows()
