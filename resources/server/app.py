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
  msg = MIMEMultipart()
  request = urllib2.Request(app.config[IMG_URL])
  auth = base64.encodestring('%s:%s' % (app.config[USERNAME], app.config[PASSWORD])).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % auth)
  cherrypy.log("Pulling image from URL: " + app.config[IMG_URL])
  try:
    image = MIMEImage(urllib2.urlopen(link).read())
  except: 
    cherrypy.log("Failed to load image", traceback=True)

  text = MIMEText("")

  msg.attach(text)
  msg.attach(image)

  mailer = smtplib.SMTP()
  mailer.connect()
  cherrypy.log("Sending mail to " + app.config[EMAIL_FROM])
  try:
    mailer.sendmail(app.config[EMAIL_FROM], app.config[EMAIL_TO], msg.as_string())
  except:
    cherrypy.log("Failed to send mail", traceback=True)

  mailer.close()

  return "Ok"

if __name__ == "__main__":
    app.run()
