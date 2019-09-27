from enum import IntEnum
from collections import UserList
from typing import Union, Iterable


class LengthError(Exception):
    pass


class PayloadType(IntEnum):
    '''
    Types and type numbers from RFC 3551.
    Types are in the first instance named ``<encoding_name>``.
    Where multiple types exist for the same encoding name,
    types are named ``<encoding_name>_<clock_rate>Hz`` where multiple clock
    rates exist or ``<encoding_name>_<channels>chan`` where multiple numbers of
    channels exist. Where all are equal, the name is ``<encoding_name>_<PT>``.
    '''

    PCMU = 0
    RESERVED_1 = 1
    RESERVED_2 = 2
    GSM = 3
    G723 = 4
    DVI4_8000Hz = 5
    DVI4_16000Hz = 6
    LPC = 7
    PCMA = 8
    G722 = 9
    L16_2chan = 10
    L16_1chan = 11
    QCELP = 12
    CN = 13
    MPA = 14
    G728 = 15
    DVI4_11025Hz = 16
    DVI4_22050Hz = 17
    G729 = 18
    RESERVED_19 = 19
    UNASSIGNED_20 = 20
    UNASSIGNED_21 = 21
    UNASSIGNED_22 = 22
    UNASSIGNED_23 = 23
    UNASSIGNED_24 = 24
    CELB = 25
    JPEG = 26
    UNASSIGNED_27 = 27
    NV = 28
    UNASSIGNED_29 = 29
    UNASSIGNED_30 = 30
    H261 = 31
    MPV = 32
    MP2T = 33
    H263 = 34
    UNASSIGNED_35 = 35
    UNASSIGNED_36 = 36
    UNASSIGNED_37 = 37
    UNASSIGNED_38 = 38
    UNASSIGNED_39 = 39
    UNASSIGNED_40 = 40
    UNASSIGNED_41 = 41
    UNASSIGNED_42 = 42
    UNASSIGNED_43 = 43
    UNASSIGNED_44 = 44
    UNASSIGNED_45 = 45
    UNASSIGNED_46 = 46
    UNASSIGNED_47 = 47
    UNASSIGNED_48 = 48
    UNASSIGNED_49 = 49
    UNASSIGNED_50 = 50
    UNASSIGNED_51 = 51
    UNASSIGNED_52 = 52
    UNASSIGNED_53 = 53
    UNASSIGNED_54 = 54
    UNASSIGNED_55 = 55
    UNASSIGNED_56 = 56
    UNASSIGNED_57 = 57
    UNASSIGNED_58 = 58
    UNASSIGNED_59 = 59
    UNASSIGNED_60 = 60
    UNASSIGNED_61 = 61
    UNASSIGNED_62 = 62
    UNASSIGNED_63 = 63
    UNASSIGNED_64 = 64
    UNASSIGNED_65 = 65
    UNASSIGNED_66 = 66
    UNASSIGNED_67 = 67
    UNASSIGNED_68 = 68
    UNASSIGNED_69 = 69
    UNASSIGNED_70 = 70
    UNASSIGNED_71 = 71
    RESERVED_72 = 72
    RESERVED_73 = 73
    RESERVED_74 = 74
    RESERVED_75 = 75
    RESERVED_76 = 76
    UNASSIGNED_77 = 77
    UNASSIGNED_78 = 78
    UNASSIGNED_79 = 79
    UNASSIGNED_80 = 80
    UNASSIGNED_81 = 81
    UNASSIGNED_82 = 82
    UNASSIGNED_83 = 83
    UNASSIGNED_84 = 84
    UNASSIGNED_85 = 85
    UNASSIGNED_86 = 86
    UNASSIGNED_87 = 87
    UNASSIGNED_88 = 88
    UNASSIGNED_89 = 89
    UNASSIGNED_90 = 90
    UNASSIGNED_91 = 91
    UNASSIGNED_92 = 92
    UNASSIGNED_93 = 93
    UNASSIGNED_94 = 94
    UNASSIGNED_95 = 95
    DYNAMIC_96 = 96
    DYNAMIC_97 = 97
    DYNAMIC_98 = 98
    DYNAMIC_99 = 99
    DYNAMIC_100 = 100
    DYNAMIC_101 = 101
    DYNAMIC_102 = 102
    DYNAMIC_103 = 103
    DYNAMIC_104 = 104
    DYNAMIC_105 = 105
    DYNAMIC_106 = 106
    DYNAMIC_107 = 107
    DYNAMIC_108 = 108
    DYNAMIC_109 = 109
    DYNAMIC_110 = 110
    DYNAMIC_111 = 111
    DYNAMIC_112 = 112
    DYNAMIC_113 = 113
    DYNAMIC_114 = 114
    DYNAMIC_115 = 115
    DYNAMIC_116 = 116
    DYNAMIC_117 = 117
    DYNAMIC_118 = 118
    DYNAMIC_119 = 119
    DYNAMIC_120 = 120
    DYNAMIC_121 = 121
    DYNAMIC_122 = 122
    DYNAMIC_123 = 123
    DYNAMIC_124 = 124
    DYNAMIC_125 = 125
    DYNAMIC_126 = 126
    DYNAMIC_127 = 127

    @classmethod
    def _unassignedList(self) -> list:
        uList = list(range(20, 25))
        uList += [27]
        uList += list(range(29, 31))
        uList += list(range(35, 72))
        uList += list(range(77, 96))

        return uList

    @classmethod
    def _reservedList(self) -> list:
        _rList = list(range(1, 3))
        _rList += [19]
        _rList += list(range(72, 77))

        return _rList

    def isAudio(self) -> bool:
        '''
        Is instance media type audio. Note MP2T is AV and this will return
        ``True``.
        '''

        return (self.value <= 23) or (self.value == 33)

    def isVideo(self) -> bool:
        '''
        Is instance media type video. Note MP2T is AV and this will return
        ``True``.
        '''

        return (self.value >= 24) and (self.value <= 34)

    def isAV(self) -> bool:
        '''
        Is instance media type AV. This only applies to MP2T.
        '''

        return self.value == 33

    def isDynamic(self) -> bool:
        '''
        Is instance encoding name ``dynamic``.
        '''

        return self.value >= 96

    def isUnassigned(self) -> bool:
        '''
        Is instance encoding name ``unassigned``.
        '''

        return self.value in self._unassignedList()

    def isReserved(self) -> bool:
        '''
        Is instance encoding name ``reserved``.
        '''

        return self.value in self._reservedList()


class CSRCList(UserList):
    '''
    A list of Contributing Source Identifiers (CSRCs). CSRCs are stored as
    integers. The list size and CSRC values are validated in accordance with
    RFC 3550. The list size is ``0-15``. CSRC values are ``0 <= x < 2**32``.
    '''

    def __init__(self, inList=[]):
        if len(inList) > 15:
            raise LengthError("CSRC list length too long. Max length is 15.")

        self.data = []

        for x in inList:
            self._csrcIsValid(x)
            self.data.append(x)

    def __add__(self, value: Iterable[int]) -> 'CSRCList':
        newList = CSRCList(self)
        newList += value
        return newList

    def __iadd__(self, value: Iterable[int]) -> 'CSRCList':
        self.extend(value)

        return self

    def extend(self, value: Iterable[int]) -> None:
        '''
        Extend the list by appending all the CSRCs from the iterable.
        '''

        if len(self.data) + len(list(value)) > 15:
            raise LengthError(
                "Extending would make CSRC list length too long. "
                "Max length is 15.")

        for x in value:
            self.append(x)

    def append(self, value: int) -> None:
        '''
        Add a CSRC to the end of the list.
        '''

        if len(self.data) == 15:
            raise LengthError(
                "Appending would make CSRC list length too long. "
                "Max length is 15.")

        self._csrcIsValid(value)

        self.data.append(value)

    def insert(self, i: int, x: int) -> None:
        '''
        Insert a CSRC at a given position. The first argument is the index of
        the element before which to insert, so ``a.insert(0, x)`` inserts at
        the front of the list, and ``a.insert(len(a), x)`` is equivalent to
        ``a.append(x)``.
        '''

        if (i < 0) or (i > len(self.data)) or (i >= 15):
            raise IndexError(
                "CSRC list index must be in range 0-15 and cannot leave gaps")
        self._csrcIsValid(x)

        self.data.insert(i, x)

    def _csrcIsValid(self, value: int) -> None:
        if type(value) != int:
            raise AttributeError(
                "CSRC values must be unsigned 32-bit integers")
        elif (value < 0) or (value >= 2**32):
            raise ValueError("CSRC values must be unsigned 32-bit integers")


class Extension:
    '''
    A data structure for storing RTP header extensions as defined by RFC 3550.

    Attributes:
        startBits (bytearray): The initial 16bits of the header extension. Must
            be 2 bytes long.
        headerExtension (bytearray): The main header extension bits. Must be a
            multiple of 4 bytes long.
    '''

    def __init__(self):
        self.startBits = bytearray(2)
        self.headerExtension = bytearray()

    def __eq__(self, other) -> bool:
        return (
            (type(self) == type(other)) and
            (self.startBits == other.startBits) and
            (self.headerExtension == other.headerExtension))

    @property
    def startBits(self) -> bytearray:
        return self._startBits

    @startBits.setter
    def startBits(self, s: bytearray) -> None:
        if type(s) != bytearray:
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
        if type(s) != bytearray:
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

    def __init__(self):
        self.version = 2
        self.padding = False
        self.marker = False
        self.payloadType = PayloadType.DYNAMIC_96
        self.sequenceNumber = 0
        self.timestamp = 0
        self.ssrc = 0
        self.extension = None
        self._csrcList = CSRCList()
        self.payload = bytearray()

    def __eq__(self, other) -> bool:
        return (
            (type(self) == type(other)) and
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
        if type(p) == bool:
            self._padding = p
        else:
            raise AttributeError("Padding value must be boolean")

    @property
    def extension(self) -> Union[Extension, None]:
        return self._extension

    @extension.setter
    def extension(self, e: Union[Extension, None]) -> None:
        if (type(e) == Extension) or (e is None):
            self._extension = e
        else:
            raise AttributeError(
                "Extension value type must be Extension or None")

    @property
    def marker(self) -> bool:
        return self._marker

    @marker.setter
    def marker(self, m: bool) -> None:
        if type(m) == bool:
            self._marker = m
        else:
            raise AttributeError("Marker value must be boolean")

    @property
    def payloadType(self) -> PayloadType:
        return self._payloadType

    @payloadType.setter
    def payloadType(self, p: PayloadType) -> None:
        if type(p) == PayloadType:
            self._payloadType = p
        else:
            raise AttributeError("PayloadType value must be PayloadType")

    @property
    def sequenceNumber(self) -> int:
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, s: int) -> None:
        if type(s) != int:
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
        if type(t) != int:
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
        if type(s) != int:
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
        if type(p) != bytearray:
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
