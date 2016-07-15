from flask import Flask
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import cherrypy
import smtplib
import urllib2, base64

app = Flask(__name__)
app.config.from_pyfile("/config/img_mailer.cfg")

@app.route ("/")
def info():
  return "To send mail use /mailsend"

@app.route("/mailsend")
def mailsend():
  cherrypy.log("Application triggered")
  cherrypy.log("IMG_URL=" + app.config["IMG_URL"])
  cherrypy.log("USERNAME=" + app.config["USERNAME"])
  request = urllib2.Request(app.config["IMG_URL"])
  auth = base64.encodestring('%s:%s' % (app.config["USERNAME"], app.config["PASSWORD"])).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % auth)
  cherrypy.log("Pulling image from URL: " + app.config["IMG_URL"])
  try:
    image = MIMEImage(urllib2.urlopen(request).read())
  except: 
    cherrypy.log("Failed to load image", traceback=True)

  text = MIMEText("")

  msg = MIMEMultipart()
  msg.attach(text)
  msg.attach(image)
  msg["From"] = app.config["EMAIL_FROM"]
  msg["To"] = app.config["EMAIL_TO"]
  msg["Subject"] = "Image Attached"

  cherrypy.log("Connecting to SMTP server as " + app.config["EMAIL_USERNAME"])
  try: 
    mailer = smtplib.SMTP_SSL("smtp.gmail.com")
    mailer.login(app.config["EMAIL_USERNAME"], app.config["EMAIL_PASSWORD"])
  except:
    cherrypy.log("Failed to login to SMTP server")

  cherrypy.log("Sending mail to " + app.config["EMAIL_TO"])
  try:
    mailer.sendmail(app.config["EMAIL_FROM"], app.config["EMAIL_TO"], msg.as_string())
  except:
    cherrypy.log("Failed to send mail", traceback=True)

  mailer.quit()

  return "Ok"

if __name__ == "__main__":
    app.run()
