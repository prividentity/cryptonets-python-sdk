#  PRIVATE IDENTITY LLC - PROPRIETARY AND CONFIDENTIAL (c) COPYRIGHT 2018 - 2020 PRIVATE IDENTITY LLC
#  All Rights Reserved.
#  NOTICE:  All information contained herein is, and remains the
#  property of PRIVATE IDENTITY LLC and its suppliers, if any.  The intellectual and technical concepts contained
#  herein are proprietary to PRIVATE IDENTITY LLC and its suppliers and may be covered by U.S. and Foreign Patents,
#  patents in process, and are protected by trade secret or copyright law. Dissemination of this information or
#  reproduction of this material is strictly forbidden unless prior written permission is obtained from PRIVATE
#  IDENTITY LLC. Any software that is made available to download from Private Identity LLC ("Software") is the
#  copyrighted work of Private Identity LLC and/or its suppliers. Use of the Software is governed by the terms of the
#  end user license agreement, if any, which accompanies or is included with the Software ("License Agreement"). An
#  end user must not install any Software that is accompanied by or includes a License Agreement, unless he or she
#  first agrees to the License Agreement terms. RESTRICTED RIGHTS LEGEND. Any Software which is downloaded from
#  PRIVATE IDENTITY LLC for or on behalf of the United States of America, its agencies and/or instrumentalities ("U.S.
#  Government"), is provided with Restricted Rights. Use, duplication, or disclosure by the U.S. Government is subject
#  to restrictions as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and Computer Software
#  clause at DFARS 252.227-7013 or subparagraphs (c)(1) and (2) of the Commercial Computer Software - Restricted
#  Rights at 48 CFR 52.227-19, as applicable.
#  Manufacturer is PRIVATE IDENTITY LLC , 13331 Signal Tree, Potomac, MD  20854  USA.

import functools
import warnings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)  # turn off filter
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


def log_error(logger):
    def decorated(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.exception(e)
                raise e

        return wrapped

    return decorated
