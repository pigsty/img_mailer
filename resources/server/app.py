from flask import Flask
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
import urllib2, base64

app = Flask(__name__)
app.config.from_pyfile("/config/img_mailer.cfg")


@app.route("/")
def mailsend():

  msg = MIMEMultipart()

  link = urllib2.Request(app.config[IMG_URL])
  base64string = base64.encodestring('%s:%s' % (app.config[USERNAME], app.config[PASSWORD])).replace('\n', '')
  link.add_header("Authorization", "Basic %s" % base64string)
  image = MIMEImage(urllib2.urlopen(link).read())
  text = MIMEText("")

  msg.attach(text)
  msg.attach(image)

  mailer = smtplib.SMTP()
  mailer.connect()
  mailer.sendmail(app.config[EMAIL_FROM], app.config[EMAIL_TO], msg.as_string())
  mailer.close()

  return "Ok"

if __name__ == "__main__":
    app.run()
