# rtp

This python library provides a means to decode, encode, and interact with RTP packets. It is intended to be used together with other libraries that decode, encode, and interact with the payload bitstreams. This library does not provide any network functionality.

## Example usage
```python
from rtp import *
from copy import deepcopy

baseRTP = RTP(
    marker=True,
    payloadType=PayloadType.L16_2chan,
    extension=Extension(
        startBits=getExtStartBits(),
        headerExtension=getExtBody()
        ),
    csrcList=getCSRCList()
)
thisRTPBitstream = thisRTP.toBytearray()

while runing:
    nextRTP = deepcopy(baseRTP)
    nextRTP.sequenceNumber += 1
    nextRTP.timestamp = getNextTimestamp()
    nextRTP.payload = getNextPayload()

    transmit(nextRTP)
```

```python
from rtp import *
decodedPayload = MyPayloadDecoder(
    RTP().fromBytearray(getNextPacket()).payload)

render(decodedPayload)
```
