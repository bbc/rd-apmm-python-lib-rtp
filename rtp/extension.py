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
       startBits: bytearray = None,
       headerExtension: bytearray = None):

        self.startBits = bytearray(2)
        self.headerExtension = bytearray()

        if startBits is not None:
            self.startBits = startBits

        if headerExtension is not None:
            self.headerExtension = headerExtension

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
