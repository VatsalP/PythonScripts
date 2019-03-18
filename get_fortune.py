"""
Made this for reading fortude dat files
read more: man fortune
"""
import random
import struct
import sys

def read_dat_file(filename):
    """Reads the header and the offsets from dat file
    """
    with open(filename + '.dat', 'rb') as dat:
        """
            header created by strfile

            typedef struct {				/* information table */
            #define	VERSION		1
                unsigned long	str_version;		/* version number */
                unsigned long	str_numstr;		/* # of strings in the file */
                unsigned long	str_longlen;		/* length of longest string */
                unsigned long	str_shortlen;		/* length of shortest string */
            #define	STR_RANDOM	0x1			/* randomized pointers */
            #define	STR_ORDERED	0x2			/* ordered pointers */
            #define	STR_ROTATED	0x4			/* rot-13'd text */
                unsigned long	str_flags;		/* bit field for flags */
                unsigned char	stuff[4];		/* long aligned space */
            #define	str_delim	stuff[0]		/* delimiting character */
            } STRFILE
            Delimiter is padded with 3 bytes

            Also strfile writes all fields(ie header fields and offsets) in network byte order(big-endian)
            for more read: man strfile 
        """
        header = struct.unpack(">IIIIIcxxx", dat.read(24))
        offsets = [] # for offsets from dat file
        for i in range(header[1]+1): # str_numstr + 1 == no. of offsets (starting from 0 to str_numstr)
            offsets.append(struct.unpack(">I", dat.read(4)))
    return (header, offsets)

def get_fortune(filename):
    header, offsets = read_dat_file(filename)
    random_number = random.randint(1, header[1])
    with open(filename) as file:
        fortunes_all = file.read()
        fortune = fortunes_all[offsets[random_number-1][0]:offsets[random_number][0]-2]
    return fortune

if __name__ == '__main__':
    print(
        get_fortune(
            sys.argv[1]
        ),
        end=''
    )
