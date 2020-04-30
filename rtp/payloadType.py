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

from enum import IntEnum


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
