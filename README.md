LT-code
=======

This is an implementation of a Luby Transform code in Python, consisting of two executables, one for each encoding and decoding files. These are thin wrappers around a core stream/file API.

See _D.J.C, MacKay, 'Information theory, inference, and learning algorithms. Cambridge University Press, 2003_

## Encoding

The encoding algorithm follows the given spec, so no innovations there. A few optimizations are made however. First, the CDF of the degree distribution, M(d), is precomputed for all degrees d = 1, ..., K. This CDF is represented as an array mapping index d => M(d), so sampling from the degree distribution mu(d) becomes a linear search through the CDF array looking for the bucket our random number on \[0, 1) landed in. This random number is generated as specified using the linear congruential generator. 

Second, the integer representation of all blocks is held in RAM for maximum speed in block sample generation. This is a limitation on the size of the file practically encoded on most computers, but this decision does not reach far into other parts of the design, and it can be easily addressed if necessary for better memory scalability.

```python
from sys import stdout
from lt import encode

# Stream a fountain of 1024B blocks to stdout
block_size = 1024
with open(filename, 'rb') as f:
    for block in encode.encoder(f, block_size):
        stdout.buffer.write(block)
```

## Decoding
    
The decoder reads the header, then the body, of each incoming block and conducts all possible steps in the belief propagation algorithm on a representation of the source node/check node graph that become possible given the new check node. This is done using an online algorithm, which computes the appropriate messages incrementally and passes them eagerly as the value of source nodes is resolved. Thus, the decoder will finish decoding once it has read only as many blocks is necessary in the stream to decode the file, and it seems to scale well as the file size, and block size increase.

```python
from sys import stdin
from lt import decode

# Block to fully decode transmission incoming on stdin
data = decode.decode(stdin.buffer)

# Feed the decoder as blocks come in
decoder = decode.LtDecoder()
for block in decode.read_blocks(some_stream):
    decoder.consume_block(block)
    if decoder.is_done():
       break 

# Write bytes payload to stream
decoder.stream_dump(some_out_stream)

# Get entire transmission as bytes
data = decoder.bytes_dump()
```
## Commandline Usage

    To run the encoder, invoke the following from the shell
    $ ./bin/encoder <file> <blocksize> <seed> [c] [delta]

    To run the decoder, run the following
    $ ./bin/decoder 
