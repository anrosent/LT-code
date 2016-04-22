#!/usr/bin/env python3
"""Implementation of a Luby Transform encoder.

This is a type of fountain code, which deals with lossy channels by 
sending an infinite stream of statistically correllated packets generated
from a set of blocks into which the source data is divided. In this way, 
epensive retransmissions are unecessary, as the receiver will be able 
to reconstruct the file with high probability after receiving only 
slightly more blocks than one would have to transmit sending the raw
blocks over a lossless channel.

See 

D.J.C, MacKay, 'Information theory, inference, and learning algorithms'.
Cambridge University Press, 2003

for reference.
"""
import os.path
import argparse
import sys
import time

from lt import encoder, sampler

def run(fn, blocksize, seed, c, delta):
    """Run the encoder until the channel is broken, signalling that the 
    receiver has successfully reconstructed the file
    """

    for block in encoder.encode(fn, blocksize, seed, c, delta):
        sys.stdout.buffer.write(block)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("encoder")
    parser.add_argument('file', help='the source file to encode')
    parser.add_argument('blocksize', metavar='block-size', 
                                     type=int, 
                                     help='the size of each encoded block, in bytes')
    parser.add_argument('seed', type=int,
                                nargs="?",
                                default=2067261,
                                help='the initial seed for the random number generator')
    parser.add_argument('c', type=float,
                             nargs="?",
                             default=sampler.PRNG_C,
                             help='degree sampling distribution tuning parameter')
    parser.add_argument('delta', type=float,
                                 nargs="?",
                                 default=sampler.PRNG_DELTA,
                                 help='degree sampling distribution tuning parameter')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("File %s doesn't exist. Try again." % args.file, file=sys.stderr)
        sys.exit(1)
    
    try:
        run(args.file, args.blocksize, args.seed, args.c, args.delta)
    except (GeneratorExit, IOError):
        print("Decoder has cut off transmission. Fountain closed.", file=sys.stderr)
        sys.stdout.write = lambda s:None
        sys.stdout.flush = lambda:None
        sys.exit(0)
