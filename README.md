# rtp

This python library provides a means to decode, encode, and interact with RTP packets. It is intended to be used together with other libraries that decode, encode, and interact with the payload bitstreams. This library does not provide any network functionality.

## Installation

```bash
pip install rtp
```

## Example usage
```python
from rtp import RTP, Extension, PayloadType
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
from rtp import RTP

decodedPayload = MyPayloadDecoder(
    RTP().fromBytearray(getNextPacket()).payload)

render(decodedPayload)
```

## Contributing
We desire that contributors of pull requests have signed, and submitted via email, a [Contributor Licence Agreement (CLA)](http://www.bbc.co.uk/opensource/cla/rfc-8759-cla.docx), which is based on the Apache CLA.

The purpose of this agreement is to clearly define the terms under which intellectual property has been contributed to the BBC and thereby allow us to defend the project should there be a legal dispute regarding the software at some future time.

If you haven't signed and emailed the agreement yet then the project owners will contact you using the contact info with the pull request.

## License
See [LICENSE](LICENSE).

## Authors

* James Sandford

For further information, contact <cloudfit-opensource@rd.bbc.co.uk>
