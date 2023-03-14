# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 01:27:59 2023

@author: mavii
"""
import cv2


face_cascade = cv2.CascadeClassifier(#Yüz tepiti için
    "haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier(#Agız tespiti için 
    "haarcascade_mcs_mouth.xml")


org = (30,30)#resim üzerinde kordinat
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
weared_mask = "Thank you for wearing MASK"#maske takılıyken uyari verilecek string ifade
not_weared_mask = "Please wear MASK to defeat CORONA"#maske takili degilken uyari verilecek string ifade

cap = cv2.VideoCapture(0)#harici kameramız olmadığı için ilk kameramıza erişim için


while cap.isOpened():#Kameramız açık oldukça manasında bir döngü
    ret, frame = cap.read()#kameradan alınan görüntüyü okuma
    if not ret:#kameranın açılmadığı durum
        print("haydaa")
        
    gray_image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#görüntüyü gri tonlamaya çevirme
    
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 7)#yuzu bulacagimiz resim icin
    
    if(len(faces) == 0):#Yüz bulunmuş mu bulunmamış mı bunun tespiti
        cv2.putText(frame, "No face found", org, fontFace, 
                    fontScale, (255,255,255), 2)#ekrana çıkartmak istediğimiz yazı ve yazının tipi sekli
    else:
        for x, y, w, h in faces:#bulunan yuzun etrafina kare cizdirmek icin
            cv2.rectangle(frame, (x,y), (x+w,y+h), 
                          (255,0,0), 2)
            roi_gray = gray_image[y:y+h, x:x+w]
            
            mouth = mouth_cascade.detectMultiScale(roi_gray,
                                                   1.4, 15)#agizi bulacagimiz resim icin
            i = 0
            if(len(mouth) == 0):#agiz bulunamadiginda bu kosulun icine girer
                cv2.putText(frame, weared_mask, org, fontFace,
                            fontScale, (0,255,0), 
                            2, cv2.LINE_AA)
            else:#agiz bulundugunda bu kosulun icine girer
                cv2.putText(frame, not_weared_mask, org, 
                            fontFace, fontScale, (0,0,255),
                            4, cv2.LINE_AA)
                for mx, my, mw, mh in mouth:
                    if i == 0:
                        i+=1
                        cv2.rectangle(frame, (mx+x,my+y),
                                      (mx+x+mw, my+y+mh), (0,0,255),3)
                    else:
                        pass
        
    cv2.imshow("Mask Detection",frame)#cerceveyi gostermek icin
    
    if cv2.waitKey(1) & 0xFF == ord("q"):#1 salisede bir yeni görüntü gönderip ve q tuşuna basildiginda cikmak icin
        print("by")
        break



cap.release()#kamerayı bırakıyoruz
cv2.destroyAllWindows()#pencereleri kapatıyoruz

