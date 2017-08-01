# -*- coding: utf-8 -*-

from iw.email.testing import EmailTestCase
from afpy.mail import LDAPMailTemplate
from afpy.ldap import custom as ldap

class TestMail(EmailTestCase):

    def test_new_members(self):
        mail = LDAPMailTemplate('new_members', subject='test welcome',
                                passwd='toto', paymentObject='cheque')
        mail.send('gawel')

        mail = self.mail_output()
        mail.mustcontain('http://www.afpy.org/membres/courrier',
                         '- Email: gawel@afpy.org')

    def test_new_subscription(self):
        mail = LDAPMailTemplate('new_subscription', subject='test subscription',
                                paymentObject='cheque', paymentComment='comment', paymentMode='cheque')
        mail.send('gawel')

    def test_password(self):
        mail = LDAPMailTemplate('send_password', subject='test password', passwd='toto')
        mail.send('gawel')

        mail = self.mail_output()
        mail.mustcontain('gawel', 'toto')

    def test_send_key(self):
        mail = LDAPMailTemplate('send_key', subject='test send key', passwd='toto',
                                confirm_url='http://confirm')
        mail.send('gawel')

        mail = self.mail_output()
        mail.mustcontain('/confirm', 'gawel', 'toto')


    def test_need_payment(self):
        mail = LDAPMailTemplate('need_payment', subject='test need_payment',
                                )
        mail.send('bluetouff')

        mail = self.mail_output()
        mail.mustcontain('gawel')

