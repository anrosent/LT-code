import sys
from struct import pack

from lt import sampler

def get_blocks(f, blocksize):
    """Block file byte contents into blocksize chunks, padding last one if necessary
    """

    f_bytes = f.read()
    blocks = [int.from_bytes(f_bytes[i:i+blocksize].ljust(blocksize, b'0'), sys.byteorder) 
            for i in range(0, len(f_bytes), blocksize)]
    return len(f_bytes), blocks


def encode(fn, blocksize, seed, c, delta):
    """Generates an infinite sequence of blocks to transmit
    to the receiver
    """

    # get file blocks
    with open(fn, 'rb') as f:
        filesize, blocks = get_blocks(f, blocksize)

    # init stream vars
    K = len(blocks)
    prng = sampler.PRNG(params=(K, delta, c))
    prng.set_seed(seed)

    # block generation loop
    while True:
        blockseed, d, ix_samples = prng.get_src_blocks()
        block_data = 0
        for ix in ix_samples:
            block_data ^= blocks[ix]

        # Generate blocks of XORed data in network byte order
        block = (filesize, blocksize, blockseed, int.to_bytes(block_data, blocksize, sys.byteorder))
        yield pack('!III%ss'%blocksize, *block)
