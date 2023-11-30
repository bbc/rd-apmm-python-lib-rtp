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

from typing import Iterable, Optional
from random import randint
from .payloadType import PayloadType
from .csrcList import CSRCList
from .extension import Extension


class RTP:
    '''
    A data structure for storing RTP packets as defined by RFC 3550.

    Attributes:
        version (int): The RTP version. MUST be set to ``2``.
        padding (bool): If set to true, the packet contains extra padding.
        marker (bool): The interpretation of the marker bit is defined by the
            payload profile.
        payloadType (PayloadType): Identifies the format of the payload.
        sequenceNumber (int): The sequence number of the packet. Must be in the
            range ``0 <= x < 2**16``
        timestamp (int): The timestamp of the packet. Must be in the range
            ``0 <= x < 2**32``
        ssrc (int): The Synchronization Source Identifier. Must be in the range
            ``0 <= x < 2**32``
        extension (:obj:`Extension`): A header extension. May be ``None``.
        csrcList (:obj:`CSRCList`): The CSRC list.
        payload (bytearray): The RTP payload.

    '''

    def __init__(
       self,
       version: int = 2,
       padding: bool = False,
       marker: bool = False,
       payloadType: PayloadType = PayloadType.DYNAMIC_96,
       sequenceNumber: Optional[int] = None,
       timestamp: int = 0,
       ssrc: Optional[int] = None,
       extension: Optional[Extension] = None,
       csrcList: Optional[Iterable[int]] = None,
       payload: Optional[bytearray] = None) -> None:
        self.version = version
        self.padding = padding
        self.marker = marker
        self.payloadType = payloadType
        self.timestamp = timestamp
        self.ssrc = timestamp
        self.extension = extension
        self._csrcList = CSRCList()
        self.payload = bytearray()

        if sequenceNumber is None:
            self.sequenceNumber = randint(0, (2**16)-1)
        else:
            self.sequenceNumber = sequenceNumber

        if ssrc is None:
            self.ssrc = randint(0, (2**32)-1)
        else:
            self.ssrc = ssrc

        if csrcList is not None:
            self.csrcList.extend(csrcList)

        if payload is not None:
            self.payload = payload

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RTP):
            return NotImplemented
        return (
            (type(self) is type(other)) and
            (self.version == other.version) and
            (self.padding == other.padding) and
            (self.marker == other.marker) and
            (self.payloadType == other.payloadType) and
            (self.sequenceNumber == other.sequenceNumber) and
            (self.timestamp == other.timestamp) and
            (self.ssrc == other.ssrc) and
            (self.extension == other.extension) and
            (self.csrcList == other.csrcList) and
            (self.payload == other.payload))

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, v: int) -> None:
        # We only support RFC 3550
        if v == 2:
            self._version = v
        else:
            raise ValueError("Version must be '2' under RFC 3550")

    @property
    def padding(self) -> bool:
        return self._padding

    @padding.setter
    def padding(self, p: bool) -> None:
        if type(p) is bool:
            self._padding = p
        else:
            raise AttributeError("Padding value must be boolean")

    @property
    def extension(self) -> Optional[Extension]:
        return self._extension

    @extension.setter
    def extension(self, e: Optional[Extension]) -> None:
        if (type(e) is Extension) or (e is None):
            self._extension = e
        else:
            raise AttributeError(
                "Extension value type must be Extension or None")

    @property
    def marker(self) -> bool:
        return self._marker

    @marker.setter
    def marker(self, m: bool) -> None:
        if type(m) is bool:
            self._marker = m
        else:
            raise AttributeError("Marker value must be boolean")

    @property
    def payloadType(self) -> PayloadType:
        return self._payloadType

    @payloadType.setter
    def payloadType(self, p: PayloadType) -> None:
        if type(p) is PayloadType:
            self._payloadType = p
        else:
            raise AttributeError("PayloadType value must be PayloadType")

    @property
    def sequenceNumber(self) -> int:
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, s: int) -> None:
        if type(s) is not int:
            raise AttributeError("SequenceNumber value must be integer")
        elif (s < 0) or (s >= 2**16):
            raise ValueError("SequenceNumber must be in range 0-2**16")
        else:
            self._sequenceNumber = s

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, t: int) -> None:
        if type(t) is not int:
            raise AttributeError("Timestamp value must be integer")
        elif (t < 0) or (t >= 2**32):
            raise ValueError("Timestamp must be in range 0-2**32")
        else:
            self._timestamp = t

    @property
    def ssrc(self) -> int:
        return self._ssrc

    @ssrc.setter
    def ssrc(self, s: int) -> None:
        if type(s) is not int:
            raise AttributeError("SSRC value must be integer")
        elif (s < 0) or (s >= 2**32):
            raise ValueError("SSRC must be in range 0-2**32")
        else:
            self._ssrc = s

    @property
    def csrcList(self) -> CSRCList:
        return self._csrcList

    @property
    def payload(self) -> bytearray:
        return self._payload

    @payload.setter
    def payload(self, p: bytearray) -> None:
        if type(p) is not bytearray:
            raise AttributeError("Payload value must be bytearray")
        else:
            self._payload = p

    def fromBytearray(self, packet: bytearray) -> 'RTP':
        '''
        Populate instance from a bytearray.
        '''

        self.version = (packet[0] >> 6) & 3
        self.padding = ((packet[0] >> 5) & 1) == 1
        hasExtension = ((packet[0] >> 4) & 1) == 1
        csrcListLen = packet[0] & 0x0f

        self.marker = ((packet[1] >> 7) & 1) == 1
        self.payloadType = PayloadType(packet[1] & 0x7f)

        self.sequenceNumber = int.from_bytes(packet[2:4], byteorder='big')

        self.timestamp = int.from_bytes(packet[4:8], byteorder='big')

        self.ssrc = int.from_bytes(packet[8:12], byteorder='big')

        for x in range(csrcListLen):
            startIndex = 12 + (4*x)
            endIndex = 12 + 4 + (4*x)
            self.csrcList.append(
                int.from_bytes(packet[startIndex: endIndex], byteorder='big'))

        extStart = 12 + (4*csrcListLen)
        payloadStart = extStart

        if hasExtension:
            extLen = int.from_bytes(
                packet[extStart+2:extStart+4], byteorder='big')
            payloadStart += (extLen + 1) * 4
            self.extension = Extension().fromBytearray(
                packet[extStart:payloadStart])

        self.payload = packet[payloadStart:]

        return self

    def toBytearray(self) -> bytearray:
        '''
        Encode instance as a bytearray.
        '''

        packetLen = 12
        packetLen += 4 * len(self.csrcList)

        extensionStartIndex = packetLen
        payloadStartIndex = extensionStartIndex

        if self.extension is not None:
            payloadStartIndex += len(bytes(self.extension))
            packetLen = payloadStartIndex

        packetLen += len(self.payload)

        packet = bytearray(packetLen)

        packet[0] = self.version << 6
        packet[0] |= self.padding << 5
        packet[0] |= (self.extension is not None) << 4
        packet[0] |= len(self.csrcList)

        packet[1] = self.marker << 7
        packet[1] |= self.payloadType.value

        packet[2:4] = self.sequenceNumber.to_bytes(2, byteorder='big')

        packet[4:8] = self.timestamp.to_bytes(4, byteorder='big')

        packet[8:12] = self.ssrc.to_bytes(4, byteorder='big')

        for x in range(len(self.csrcList)):
            startIndex = 12 + (4*x)
            endIndex = 12 + 4 + (4*x)
            packet[startIndex: endIndex] = self.csrcList[x].to_bytes(
                4, byteorder='big')

        if self.extension is not None:
            packet[extensionStartIndex:payloadStartIndex] = bytes(
                self.extension)

        packet[payloadStartIndex:] = self.payload

        return packet

    def fromBytes(self, packet: bytes) -> 'RTP':
        '''
        Populate instance from bytes.
        '''
        return self.fromBytearray(bytearray(packet))

    def toBytes(self) -> bytes:
        '''
        Encode instance as bytes.
        '''
        return bytes(self.toBytearray())

    def __bytes__(self) -> bytes:
        return self.toBytes()
