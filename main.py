import cv2
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ====== Gmail 寄信設定 ======

GMAIL_ADDRESS = "@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx"
TO_EMAIL = "@gmail.com"

def send_email_notification(filename):
    subject = "⚠️ 人臉偵測通知"
    body = f"攝影機剛剛偵測到人臉，已保存圖片：{filename}"

    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # 寄送 Gmail（使用 SSL）
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, TO_EMAIL, msg.as_string())

    print("📧 Gmail 通知已發送!")


# ====== OpenCV 人臉偵測 ======
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 保存圖片
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")

        # Gmail 通知
        send_email_notification(filename)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
