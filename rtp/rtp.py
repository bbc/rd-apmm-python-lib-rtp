from enum import IntEnum
from collections import UserList
from typing import Union, List, Iterable


class PayloadType(IntEnum):
    # Types and type numbers from RFC 3551.
    # Types are in the first instance named '<encoding_name>'.
    # Where multiple types exist for the same encoding name,
    # types are named '<encoding_name>_<clock_rate>Hz' where multiple clock
    # rates exist or '<encoding_name>_<channels>chan' where multiple numbers of
    # channels exist. Where all are equal, the name is '<encoding_name>_<PT>'.
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
        # MP2T (33) is AV so we return True
        return (self.value <= 23) or (self.value == 33)

    def isVideo(self) -> bool:
        # MP2T (33) is AV so we return True
        return (self.value >= 24) and (self.value <= 34)

    def isAV(self) -> bool:
        return self.value == 33

    def isDynamic(self) -> bool:
        return self.value >= 96

    def isUnassigned(self) -> bool:
        return self.value in self._unassignedList()

    def isReserved(self) -> bool:
        return self.value in self._reservedList()


class CSRCList(UserList):
    def __init__(self, inList=[]):
        map(self.csrcIsValid, inList)

        self += inList

    def __add__(self, value: Iterable[int]) -> 'CSRCList':
        newList = CSRCList(self)
        newList += value
        return newList

    def __iadd__(self, value: Iterable[int]) -> 'CSRCList':
        self.extend(value)

        return self

    def extend(self, value: Iterable[int]) -> None:
        map(self.append, value)

    def append(self, value: int) -> None:
        self.csrcIsValid(value)
        self.data.append(value)

    def insert(self, value: int, x: int) -> None:
        self.csrcIsValid(value)
        self.data.insert(value, x)

    def csrcIsValid(self, value: int) -> None:
        if type(value) != int:
            raise AttributeError
        elif (value < 0) or (value >= 2**32):
            raise ValueError


class Extension:
    def __init__(self):
        self.startBits = b''
        self.headerExtension = b''

    @property
    def startBits(self) -> bytes:
        return self._startBits

    @startBits.setter
    def startBits(self, s: bytes) -> None:
        if type(s) != bytes:
            raise AttributeError
        elif len(s) != 2:
            raise ValueError
        else:
            self._startBits = s

    @property
    def headerExtension(self) -> bytes:
        return self._headerExtension

    @headerExtension.setter
    def headerExtension(self, s: bytes) -> None:
        if type(s) != bytes:
            raise AttributeError
        else:
            self._headerExtension = s


class RTP:
    def __init__(self):
        self.version = 2
        self.padding = False
        self.extension = None
        self.marker = False
        self.payloadType = None
        self.sequenceNumber = 0
        self.timestamp = 0
        self.ssrc = 0
        self._csrcList = CSRCList()
        self.payload = b''

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
            raise AttributeError

    @property
    def extension(self) -> Union[Extension, None]:
        return self._extension

    @extension.setter
    def extension(self, e: Union[Extension, None]) -> None:
        if type(e) == Extension:
            self._extension = e
        else:
            raise AttributeError

    @property
    def marker(self) -> bool:
        return self._marker

    @marker.setter
    def marker(self, m: bool) -> None:
        if type(m) == bool:
            self._marker = m
        else:
            raise AttributeError

    @property
    def payloadType(self) -> PayloadType:
        return self._payloadType

    @payloadType.setter
    def payloadType(self, p: PayloadType) -> None:
        if type(p) == PayloadType:
            self._payloadType = p
        else:
            raise AttributeError

    @property
    def sequenceNumber(self) -> int:
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, s: int) -> None:
        if type(s) != int:
            raise AttributeError
        elif (s < 0) or (s >= 2**16):
            raise ValueError
        else:
            self._sequenceNumber = s

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, t: int) -> None:
        if type(t) != int:
            raise AttributeError
        elif (t < 0) or (t >= 2**32):
            raise ValueError
        else:
            self._timestamp = t

    @property
    def ssrc(self) -> int:
        return self._ssrc

    @ssrc.setter
    def ssrc(self, s: int) -> None:
        if type(s) != int:
            raise AttributeError
        elif (s < 0) or (s >= 2**32):
            raise ValueError
        else:
            self._ssrc = s

    @property
    def csrcList(self) -> List[CSRCList]:
        return self._csrcList

    @property
    def payload(self) -> bytes:
        return self._payload

    @payload.setter
    def payload(self, p) -> None:
        if type(p) != bytes:
            raise AttributeError
        else:
            self._payload = p

    def fromBitstream(self, bits):
        pass

    def toBitstream(self):
        pass
