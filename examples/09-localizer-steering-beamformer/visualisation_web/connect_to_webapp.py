# -*- coding: utf-8 -*-
# This file is part of the HörTech Open Master Hearing Aid (openMHA)
# Copyright © 2018 2019 HörTech gGmbH
#
# openMHA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# openMHA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License, version 3 for more details.
#
# You should have received a copy of the GNU Affero General Public License, 
# version 3 along with openMHA.  If not, see <http://www.gnu.org/licenses/>.

from collections import Sequence
import socket
import sys

# Python 3 has no unicode type, but we need to test for it in Python 2, so
# create an alias.
if sys.version_info.major != 2:
    unicode = str


def connect_to_webapp(host="localhost", port=9990):
    """Connect to the visualisation web-app

    Opens a connection to the server at the specified host and port and returns
    a function, with which you can send data to the visualisation TCP server,
    along with a socket object.  The function is a closure over the socket
    object, so that you can call, e.g., fun(data) without having to carry
    around the socket object.

    The returned function accepts a single argument, which must be a sequence
    type (e.g., a list or a tuple).  For example:

        [send_data, sock] = connect_to_webapp()
        send_data(numpy.random.rand(37).tolist())

    This will send a vector of uniformly distributed numbers (converted to a
    list) to the TCP server, which will then hand the data on to the
    visualisation web-app.
    """

    sock = socket.create_connection((host, port))

    def send_data(data):

        if not isinstance(data, Sequence) or isinstance(data, (str, bytes,
                                                               unicode)):
            raise ValueError('Invalid data type "{}".'.format(type(data)))

        data_str = str(data).strip('[]()').replace(',', '')
        sock.send('{}\n'.format(data_str).encode())

    return send_data, sock
