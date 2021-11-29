# Copyright (C) 2005 Parasyte
# Copyright (C) 2021 Daniel K. O.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# This code is ported from the C code at http://n64dev.org/n64crc.html
# Based on uCON64's N64 checksum algorithm by Andreas Sterbenz

from binascii import crc32

def read32(data : bytearray, offset):
    return int.from_bytes(data[offset : offset+4],
                          byteorder='big')

def mask(x):
    return x & 0xffffffff

def rotl(val, s):
    return mask(val << s) | (val >> (32 - s))

def get_cic(data : bytearray):
    c = crc32(data[64:4096])
    if c == 0x6170a4a1:
        return 6101
    if c == 0x90bb6cb5:
        return 6102
    if c == 0x0b050ee0:
        return 6103
    if c == 0x98bc2c86:
        return 6105
    if c == 0xacc8580a:
        return 6106
    if c == 0x009e9ea3:
        return 7102
    return 6105

def get_crc_seed(cic):
    if cic in [6101, 6102, 7102]:
        return 0xf8ca4ddc
    if cic == 6103:
        return 0xa3886759
    if cic == 6105:
        return 0xdf26f436
    if cic == 6106:
        return 0x1fea617a
    return 1

def crc(data : bytearray):
    cic = get_cic(data)
    seed = get_crc_seed(cic)

    t1 = t2 = t3 = t4 = t5 = t6 = seed

    # CRC1/CRC2 are calculated from offset 0x1000 to 0x101000

    # Impl. note: XOR operations don't need to be masked to 32 bits.
    
    for offset in range(0x1000, 0x101000, 4):
        d = read32(data, offset)
        if mask(t6 + d) < t6:
            t4 = mask(t4 + 1)
        t6 = mask(t6 + d)
        t3 ^= d
        r = rotl(d, (d & 0x1f))
        t5 = mask(t5 + r)
        t2 ^= r if t2 > d else t6 ^ d

        if cic == 6105:
            t1 = mask(t1 + (d ^ read32(data, 0x750 + (offset & 0xff))))
        else:
            t1 = mask(t1 + (d ^ t5))

    if cic == 6103:
        return mask((t6 ^ t4) + t3), mask((t5 ^ t2) + t1)

    if cic == 6106:
        return mask((t6 * t4) + t3), mask((t5 * t2) + t1)

    return mask(t6 ^ t4 ^ t3), mask(t5 ^ t2 ^ t1)

def fixCRC(filename : str):
    with open(filename, "r+b") as f:
        rom = f.read(0x101000)

        cic = get_cic(rom)

        h1 = int.from_bytes(rom[16:20], byteorder='big')
        h2 = int.from_bytes(rom[20:24], byteorder='big')

        c1, c2 = crc(rom)

        print("BootChip: CIC-NUS-" + str(cic))

        if h1 != c1:
            f.seek(16)
            f.write(c1.to_bytes(4, byteorder="big"))
            print("CRC 1: 0x{:08X}  Calculated: 0x{:08X} (Bad, fixed)".format(h1, c1))
        else:
            print("CRC 1: 0x{:08X}  Calculated: 0x{:08X} (Good)".format(h1, c1))
        
        if h2 != c2:
            f.seek(20)
            f.write(c2.to_bytes(4, byteorder="big"))
            print("CRC 2: 0x{:08X}  Calculated: 0x{:08X} (Bad, fixed)".format(h2, c2))
        else:
            print("CRC 2: 0x{:08X}  Calculated: 0x{:08X} (Good)".format(h2, c2))