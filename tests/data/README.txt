 _   _____    ____          _           
| | |_   _|  / ___|___   __| | ___  ___ 
| |   | |   | |   / _ \ / _` |/ _ \/ __|
| |___| |   | |__| (_) | (_| |  __/\__ \
|_____|_|    \____\___/ \__,_|\___||___/
===========
anrosent
Completed for Brown University course cs168: Computer Networks.

    This is an implementation of a Luby Transform code in Python, consisting of two executables, one for each encoding and decoding files. The sampling code is pulled into a library shared between the two executables.

Encoding
-----------

    The encoding algorithm follows the given spec, so no innovations there. A few optimizations are made however. First, the CDF of the degree distribution, M(d), is precomputed for all degrees d = 1, ..., K. This CDF is represented as an array mapping index d => M(d), so sampling from the degree distribution mu(d) becomes a linear search through the CDF array looking for the bucket our random number on [0, 1) landed in. This random number is generated as specified using the linear congruential generator. 
    Second, the integer representation of all blocks is held in RAM for maximum speed in block sample generation. This is a limitation on the size of the file practically encoded on most computers, but this decision does not reach far into other parts of the design, and it can be easily addressed if necessary for better memory scalability.

Decoding
-----------
    
    The decoder is essentially a loop that reads the header, then the body, of each incoming block and conducts all possible steps in the belief propagation algorithm on a representation of the source node/check node graph that become possible given the new check node. This is done using an online algorithm, which computes the appropriate messages incrementally and passes them eagerly as the value of source nodes is resolved. Thus, the program will terminate once it has read only as many blocks is necessary in the stream to decode the file, and it seems to scale well as the file size, block size, and drop rate increase.

Usage
------------

    To run the encoder, invoke the following from the shell
    $ ./encoder <file> <blocksize> <seed> [c] [delta]

    To run the decoder, run the following
    $ ./decoder <drop-rate>
    where <drop-rate> is written as a decimal probability of a block being dropped in transmission
