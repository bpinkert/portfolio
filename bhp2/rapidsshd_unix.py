#!/usr/bin/env python
#
# This file is part of rapidssh - http://bitbucket.org/gnotaras/rapidssh/
#
# rapidssh - A set of Secure Shell (SSH) server implementations in Python
#            using Twisted.conch, part of the Twisted Framework.
#
# Copyright (c) 2010 George Notaras - http://www.g-loaded.eu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Initially based on the sshsimpleserver.py kindly published by:
# Twisted Matrix Laboratories - http://twistedmatrix.com
#
 
import sys
import pam
 
from twisted.conch.unix import UnixSSHRealm
from twisted.cred import portal
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred.error import UnauthorizedLogin
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.internet import reactor, defer
from zope.interface import implements
from twisted.python import log
 
# Logging
# Currently logging to STDERR
log.startLogging(sys.stderr)
 
# Server-side public and private keys. These are the keys found in
# sshsimpleserver.py. Make sure you generate your own using ssh-keygen!
 
publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDoB96ecssW2Jg7vaUtTALyC1YPyO9ubeBNfVOmiEGH6n5tbg53Ldkm8XLtMEBsuM5QHIG1eyvuqAZUichtSw0TEYEjXwbP/YV7UyO/7QODOEWDoqZ1Ie6MV7ncQaUo1qIeECdNQWdSuow8khsUz6Icgo4wWfmwdqc4EYgqOfLkV2WwA205iMM2OegXNUopiE0h1OB4FBkgtcpddMvZcjvoLNaEBHJylNxdix0AUfwjOmki+QCCUpb7SVHH9nuNK0pIXe46mMACgag1o7hIanHYDsz+RwHv22INmGhci7Mjw8wW26Ymy3ZowLQhQgYw6OmEk/6kcMn2KuJrxD1yiU15'
 
privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA6AfennLLFtiYO72lLUwC8gtWD8jvbm3gTX1TpohBh+p+bW4O
dy3ZJvFy7TBAbLjOUByBtXsr7qgGVInIbUsNExGBI18Gz/2Fe1Mjv+0DgzhFg6Km
dSHujFe53EGlKNaiHhAnTUFnUrqMPJIbFM+iHIKOMFn5sHanOBGIKjny5FdlsANt
OYjDNjnoFzVKKYhNIdTgeBQZILXKXXTL2XI76CzWhARycpTcXYsdAFH8IzppIvkA
glKW+0lRx/Z7jStKSF3uOpjAAoGoNaO4SGpx2A7M/kcB79tiDZhoXIuzI8PMFtum
Jst2aMC0IUIGMOjphJP+pHDJ9iria8Q9colNeQIDAQABAoIBAH+mrLPxJYfpGz9q
oy/bbJdq4ysF+auAKXGYLGgm+B5lRK7BaJXqlFgXZ4nUDO2DcoWiWT3ViKLgr7Lc
pnZyXrwJ2kjyY5YTvNbPM5DIPTF4yM2Vswwn4cw2CxuAxfNEuaXebzDSdZyO4s4D
94AohuA2dzFknriVXoO7KXVJsjYqTpJM+Bsq7AIzNOyg7dIuoYZ4I/2yd2qHXI/F
jKj5hjX0/J7VsqfB9HjfOUD3zfVbd2dFLhEXixxMVUxWqA8C6hjjL0om7kjFDsIA
dP9nhWvlfuwgq/qoj9Si7fj5VxzfWaiuInR11Dpn8jsW5Iq1yCCCilcuRtAd0IdB
sb16fwECgYEA+qFpOssOeMeNRITjMeXTTVbIc0rSDDW/DOfPY5NFioWy/HFOOxKw
PXP8r0k1GP87COsM/V3KTW3HEh0smD1dZ8erBgD+WqHnHaVc1v2jVpchFC+DPe3K
5Ua/W8CqCYa1MjHlbUo59EZZBLyvc8nNs2biKLoWjJzfP5NHEU4bTmECgYEA7QBy
mmDhaBiq13nE3gqhxEOK2boNkIOe/o+Yx604KmXs4Q3NoSasv0T7RILXHQ5qtlUS
S2SfQygUEAUE42gJofoY32zmpIPY0i76/hA33CEbFjbdU2q2Gsx+h+CU2ByTESZy
8cMu1MIshW4X1t+YcJztOShltrX4gj2hcMskZhkCgYEA7NI0Qq+4XvwASmxe2blW
rk+AXSCn1Y27lxA7cNWp8jhfZhYSW9NO4OKGM4MzPwl82PJxdb939y3x2vXiO4BQ
kE2lFqk9rpopbmPgk+1at+laAl7a3luhSoBNNP+aLCIzeNiY92oZ1O3cE5PPHdPk
IM7oiJ89y2Q3tzUNBBcPykECgYEAn6f+jBsZnduIM1IXmhEFesaZYiUhACp60DgC
DvmU7ZLuKYn37Ui1dMBOmI+fxDYzExNqGJn3Y/E62rPW4C701kY5vUGKemdLiAQY
F1DroII40hUxsgEgHhuGXZigDJnrRNFm+5CmGrOX9Gb+7kSAV9SPRkL9ikE54NsN
x4NByPkCgYEAzL/UyihXce3KHOFXUAm9atw90RvCdX/uChGFdd2c77uk4lXG3HuN
B+xf4CNans/Z3YNBCVqsvDvgdd+xhyGOBz54XgJHAT0qoUdpnxJU2YMGYi/91kxe
NwOwZgqsy3ewE+7ruq6E6/cgChGjrUF1qkT2ZxdRhWWTTILkdragiek=
-----END RSA PRIVATE KEY-----"""
 
 
class PamPasswordDatabase:
    """Authentication/authorization backend using the 'login' PAM service"""
    credentialInterfaces = IUsernamePassword, implements(ICredentialsChecker)
 
    def requestAvatarId(self, credentials):
        if pam.authenticate(credentials.username, credentials.password):
            return defer.succeed(credentials.username)
        return defer.fail(UnauthorizedLogin("invalid password"))
 
 
class UnixSSHdFactory(factory.SSHFactory):
    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=publicKey)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privateKey)
    }
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }
 
# Components have already been registered in twisted.conch.unix
 
portal = portal.Portal(UnixSSHRealm())
portal.registerChecker(PamPasswordDatabase())   # Supports PAM
portal.registerChecker(SSHPublicKeyDatabase())  # Supports PKI
UnixSSHdFactory.portal = portal
 
if __name__ == '__main__':
    try:
        reactor.listenTCP(2200, UnixSSHdFactory())
        reactor.run()
    except Exception, e:
        print '[-] Caught exception: ' + str(e)
        reactor.stop()

