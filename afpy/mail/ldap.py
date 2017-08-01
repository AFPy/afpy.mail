# -*- coding: utf-8 -*-
import os
import smtplib
from afpy.ldap import custom as ldap
from iw.email import MakoMail

roles = {'tresorier':u'Trésorier',
         'president':u'Président',
         'secretaire':u'Secrétaire',
         }

keys = roles.keys()
for k in keys:
    roles['vice-%s' % k] = u'Vice-%s' % roles[k].lower()
del keys
del k


class LDAPMailTemplate(object):
    host = 'localhost'
    port = 25

    def __init__(self, name='', mfrom='', subject='',**kwargs):
        self.server = None
        self.name = name
        self.mfrom = mfrom
        kwargs['subject'] = subject
        signature = kwargs.get('signature', 'tresorier')
        if not self.mfrom:
            self.mfrom = '%s@afpy.org' % (signature == 'tresorier' and 'tresorerie' or signature)
        signature=ldap.getUserByTitle(signature)
        kwargs['signature'] = signature
        self.data = kwargs

    def send(self, uid, **kwargs):
        if isinstance(uid, ldap.User):
            user = uid
        else:
            user = ldap.getUser(uid)
        data = dict(user=user)
        data.update(self.data)
        data.update(kwargs)
        mto = [kwargs.get('mto', user.email)]

        if 'cc' in data:
            cc = data['cc'].split(',')
            cc = [c.strip() for c in cc]
            mto = mto + cc

        dirname = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(dirname, 'templates', '%s.txt' % self.name)
        if not os.path.isfile(path):
            path = os.path.join(dirname, 'templates', '%s.rst' % self.name)
        mail = MakoMail(path=path, format='plain', mto=', '.join(mto), mfrom=self.mfrom,
                        afpy_org='http://www.afpy.org', **data)

        if self.server is None:
            self.server = smtplib.SMTP(self.host, self.port)

        self.server.sendmail(self.mfrom, ','.join(mto), str(mail))

def getSignature(title, **kwargs):
    res = ldap.get_conn().search_nodes(filter='(title=%s)' % title, node_class=ldap.User)
    return res[0]

def getAddress(title, **kwargs):
    res = ldap.get_conn().search_nodes(filter='(title=%s)' % title, node_class=ldap.User)
    data = dict(user=res[0])
    address = LDAPMailTemplate(name='address')
    data.update(kwargs)
    data['role'] = roles.get(title)
    return ''

def send_template():
    from optparse import OptionParser, OptionValueError
    parser = OptionParser()
    parser.add_option('-n', dest='name',
                      help='name of the template')
    parser.add_option('-f', dest='mfrom',
                      help='sender account')
    parser.add_option('-t', dest='mto',
                      help='recipient account')
    parser.add_option('-s', dest='subject',
                      help='mail subject')
    (options, args) = parser.parse_args()
    if not options.name or not options.mto or not options.mfrom:
        parser.parse_args(['-h'])
    else:
        subject = options.subject
        if not subject:
            subject = 'test template %s' % options.name
        mail = LDAPMailTemplate(signature=options.mfrom,
                                subject=subject,
                                name=options.name)
        mail.send(options.mto)

