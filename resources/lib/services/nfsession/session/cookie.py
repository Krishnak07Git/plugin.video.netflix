# -*- coding: utf-8 -*-
"""
    Copyright (C) 2017 Sebastian Golasch (plugin.video.netflix)
    Copyright (C) 2018 Caphm (original implementation module)
    Copyright (C) 2019 Stefano Gottardo - @CastagnaIT
    Handle the cookies

    SPDX-License-Identifier: MIT
    See LICENSES/MIT.md for more information.
"""
from __future__ import absolute_import, division, unicode_literals

import time

import resources.lib.common as common
import resources.lib.common.cookies as cookies
from resources.lib.globals import G
from resources.lib.services.nfsession.session.base import SessionBase

LOGIN_COOKIES = ['nfvdid', 'SecureNetflixId', 'NetflixId']


class SessionCookie(SessionBase):
    """Handle the cookies"""

    @common.time_execution(immediate=True)
    def _load_cookies(self):
        """Load stored cookies from disk"""
        # pylint: disable=broad-except
        if not self.session.cookies:
            try:
                self.session.cookies = cookies.load(self.account_hash)
            except cookies.MissingCookiesError:
                return False
            except Exception as exc:
                import traceback
                common.error('Failed to load stored cookies: {}', type(exc).__name__)
                common.error(G.py2_decode(traceback.format_exc(), 'latin-1'))
                return False
            common.info('Successfully loaded stored cookies')
        return True

    @common.time_execution(immediate=True)
    def _verify_session_cookies(self):
        """Verify that the session cookies have not expired"""
        if not self.session.cookies:
            return False
        for cookie_name in LOGIN_COOKIES:
            if cookie_name not in list(self.session.cookies.keys()):
                common.error('The cookie "{}" do not exist, it is not possible to check the expiration',
                             cookie_name)
                return False
            for cookie in list(self.session.cookies):
                if cookie.name != cookie_name:
                    continue
                if cookie.expires <= int(time.time()):
                    common.info('Login is expired')
                    return False
        return True