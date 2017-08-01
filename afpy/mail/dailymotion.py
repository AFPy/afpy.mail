# -*- coding: utf-8 -*-
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from optparse import OptionParser
import mimetypes
import posixpath
import smtplib
import os

def sendfile(mfrom='www.afpy.org', mto=None, subject='Pycon FR', filename=''):
    fd = open(filename, 'rb')
    msg = MIMEBase('video','ogg')
    msg.set_payload(fd.read())
    fd.close()
    msg.add_header('Content-Disposition','attachment',
                    filename=os.path.basename(filename))
    Encoders.encode_base64(msg)
    mail = MIMEMultipart()
    mail['From'] = mfrom
    mail['To'] = mto
    subject = '%s - %s' % (subject, os.path.basename(filename))
    mail['Subject'] = subject
    mail.attach(msg)
    print 'Sending', subject
    server = smtplib.SMTP('localhost')
    server.sendmail(mfrom, mto, mail.as_string())
    server.quit()

def senddir(mfrom, mto, subject, dirname):
    for filename in os.listdir(dirname):
        if filename.endswith('.ogg'):
            sendfile(mfrom, mto, subject,
                     os.path.join(dirname, filename))

parser = OptionParser()
parser.add_option("-f", "--from", dest="mfrom",
                  default="www@afpy.org",
                  help="sender email Default: www@afpy.org")
parser.add_option("-t", "--to", dest="mto",
                  help="recipient email at dailymotion")
parser.add_option("-s", "--subject", dest="subject",
                  default="Pycon FR",
                  help="subject Default: Pycon FR")
parser.add_option("-d", "--dirname", dest="dirname",
                  help="dirname with .ogg files")

def main():
    options, args = parser.parse_args()
    if not options.mto or not options.dirname:
        raise RuntimeError('Invalid args')
    senddir(options.mfrom, options.mto, options.subject, options.dirname)


