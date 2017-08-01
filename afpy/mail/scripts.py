# -*- coding: utf-8 -*-
from afpy.ldap import custom as ldap
from afpy.mail import LDAPMailTemplate
from optparse import OptionParser


def relance_payments():
    parser = OptionParser()
    parser.add_option("-s", "--smtp", dest="host",
                      default=None,
                      help="smtp server to use")
    (options, args) = parser.parse_args()

    mail = LDAPMailTemplate('need_payment',
                            cc='tresorerie@afpy.org',
                            subject="[Relance AFPy] Votre cotisation à l'association est expirée",
                            signature='tresorier')

    if options.host:
        mail.host = options.host

    members = ldap.getAwaitingPayments() | ldap.getExpiredUsers()
    for uid in members:
        u = ldap.getUser(uid)
        try:
            ldap.updateExpirationDate(u)
        except:
            print 'Cant edit %s' % u
        else:
            if u.expired:
                print 'Sending mail to', u.uid, u.email, 'expired since:', u.membershipExpirationDate
                mail.send(u)

    vips = set(ldap.getMembersOf('bureau')) | set(ldap.getMembersOf('cd'))
    for uid in vips:
        if uid in members:
            continue
        u = ldap.getUser(uid)
        try:
            ldap.updateExpirationDate(u)
        except:
            print 'Cant edit %s' % u
        else:
            if u.expired or not u.payments:
                print 'Sending mail to', u.uid, u.email, 'expired since:', u.membershipExpirationDate
                mail.send(u)

    print len(vips|members), 'relances sent'
