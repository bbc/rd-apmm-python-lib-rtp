# James Sandford, copyright BBC 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional
from .errors import LengthError


class Extension:
    '''
    A data structure for storing RTP header extensions as defined by RFC 3550.

    Attributes:
        startBits (bytearray): The initial 16bits of the header extension. Must
            be 2 bytes long.
        headerExtension (bytearray): The main header extension bits. Must be a
            multiple of 4 bytes long.
    '''

    def __init__(
       self,
       startBits: Optional[bytearray] = None,
       headerExtension: Optional[bytearray] = None) -> None:

        self.startBits = bytearray(2)
        self.headerExtension = bytearray()

        if startBits is not None:
            self.startBits = startBits

        if headerExtension is not None:
            self.headerExtension = headerExtension

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Extension):
            return NotImplemented
        return (
            (type(self) is type(other)) and
            (self.startBits == other.startBits) and
            (self.headerExtension == other.headerExtension))

    @property
    def startBits(self) -> bytearray:
        return self._startBits

    @startBits.setter
    def startBits(self, s: bytearray) -> None:
        if type(s) is not bytearray:
            raise AttributeError("Extension startBits must be bytearray")
        elif len(s) != 2:
            raise LengthError("Extension startBits must be 2 bytes long")
        else:
            self._startBits = s

    @property
    def headerExtension(self) -> bytearray:
        return self._headerExtension

    @headerExtension.setter
    def headerExtension(self, s: bytearray) -> None:
        if type(s) is not bytearray:
            raise AttributeError("Extension headerExtension must be bytearray")
        elif (len(s) % 4) != 0:
            raise LengthError(
                "Extension headerExtension must be 32-bit aligned")
        elif (len(s)/4) > ((2**16) - 1):
            raise LengthError(
                "Extension headerExtension must be fewer than 2**16 words")
        else:
            self._headerExtension = s

    def fromBytearray(self, inBytes: bytearray) -> 'Extension':
        '''
        Populate instance from a bytearray.
        '''

        length = int.from_bytes(inBytes[2:4], byteorder='big')
        if ((len(inBytes)/4) - 1) != int(length):
            raise LengthError(
                "Extension bytearray length doesn't match length field")

        self.startBits = inBytes[0:2]
        self.headerExtension = inBytes[4:]

        return self

    def toBytearray(self) -> bytearray:
        '''
        Encode instance as a bytearray.
        '''

        heLen = len(self.headerExtension)

        # Align to 32bits (4 bytes)
        heLenWords = heLen/4

        # Add on bytes for startBits & length
        extLen = heLen + 4

        bArray = bytearray(extLen)

        bArray[0:2] = self.startBits
        bArray[2:4] = int(heLenWords).to_bytes(2, byteorder='big')
        bArray[4:extLen] = self.headerExtension

        return bArray

    def __bytes__(self) -> bytes:
        return bytes(self.toBytearray())
