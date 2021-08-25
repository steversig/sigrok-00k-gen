##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2018 Steve R <steversig@virginmedia.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd
from .lists import *

class SamplerateError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 3
    id = 'ook_gen'
    name = 'OOK Gen'
    longname = 'On Off Keying Generator'
    desc = 'Generates ook from a file'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = ['ook']
    channels = (
        {'id': 'data', 'name': 'Data', 'desc': 'Data line'},
    )
    annotations = (
        ('info', 'Info'),
        ('nibbles', 'Nibbles'),
        ('bit', 'Bit'),
    )
    annotation_rows = (
        ('info', 'Info',(0,)),
        ('nibbles', 'Nibbles',(1,)),
        ('bits', 'Bits',(2,)),
     )
    options = (
        { 'id': 'type', 'desc': 'OOK Type', 'default': 'Oregon',
         'values': ('None','Oregon',) },
    )
        
    def __init__(self):
        self.reset()

    def reset(self):
        self.displayed = None

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        self.out_python = self.register(srd.OUTPUT_PYTHON)
        self.type = self.options['type']

    def putx(self, data):
        self.put(self.ss, self.es, self.out_ann, data)

    def putp(self, data):
        self.put(self.ss, self.es, self.out_python, data)

    def oregon_ook_gen(self,offset):
        start = offset
        for i in range(len(oregon_data)):
            nibbles = []
            encoded_bits = []
            n_len = 40  # nibble length in samples
            if oregon_data[i][2] == 'v2.1': # v2.1 has double bit pattern
                n_len = n_len * 2
            full_bit = int(n_len/4)
            half_bit = int(n_len/8)

            if oregon_data[i][2] == 'Orv2.1' or oregon_data[i][2] == 'OSV2': 
                oregon_data[i][2] = 'v2.1'
                s = oregon_data[i][0]
                if len(oregon_data[i][0]) % 2 == 0:
                    oregon_data[i][0] = "".join(["%s%s" % (s[x+1], s[x])
                                                for x in range(0, len(s), 2)])
                else:
                    last_char = oregon_data[i][0][-1]
                    oregon_data[i][0] = ("".join(["%s%s" % (s[x+1], s[x])
                                                for x in range(0, len(s)-1, 2)])
                                                + last_char)
                if oregon_data[i][0][0] == 'A': # strip the Sync Nibble off
                    oregon_data[i][0] = oregon_data[i][0][1:]
            if oregon_data[i][2] == 'OSV3':
                oregon_data[i][2] = 'v3'
            
            # add in preamble and sync
            if oregon_data[i][2] == 'v1':       # 12 1111 ... 
                preamble_sync = 'FFF|E1100|'
            elif oregon_data[i][2] == 'v2.1':   # 32 1010...
                preamble_sync = 'FFFFA'
            elif oregon_data[i][2] == 'v3':     # 24 1111...
                preamble_sync = 'FFFFFFA'
            ook = preamble_sync + oregon_data[i][0]

            pattern = ''
            in_pattern = False
            for j in range(len(ook)):  # create test data
                if '|' in ook[j]:
                    in_pattern = not in_pattern 
                    j_start = j
                    continue
                if not in_pattern:
                    nibbles.append([start, start + n_len, '', ook[j]])
                    if ook[j] != ' ':
                        nibble = "{0:04b}".format(int(ook[j], 16))
                        nibble = nibble[::-1] # reverse the bits
                    else:
                        nibble = 'EEEE'
                    for k in range(4):
                        if oregon_data[i][2] != 'v2.1':
                            encoded_bits.append([int(start + full_bit * k),
                                                 int(start+full_bit*k+full_bit),
                                                 nibble[k]])
                        else:
                            if nibble[k] == '0':
                                inv_bit = '1' 
                            else:
                                inv_bit = '0'
                            ss = int(start+full_bit*k)
                            encoded_bits.append([ss, ss + half_bit, inv_bit])
                            encoded_bits.append([ss + half_bit,
                                                 ss + full_bit,
                                                 nibble[k]])
                    start += n_len
                else:
                    pattern += ook[j]
                    if j+1 <= len(ook) and ook[j+1] == '|':
                        for k in range(len(pattern)):
                            encoded_bits.append([int(start + full_bit * k),
                                                int(start+full_bit*k+full_bit),
                                                pattern[k]])
                        nibbles.append([start,
                                         int(start + full_bit * len(pattern)),
                                        '', pattern])
                        start += int(full_bit * len(pattern))
                        pattern = ''
            
            for l in range(len(nibbles)):   # write nibbles to screen
                self.ss = nibbles[l][0]
                self.es = nibbles[l][1]
                self.putx([1, [nibbles[l][3]]])
            
            eb = encoded_bits
            for l in range(len(eb)):        # write bits to screen
                self.put(eb[l][0], eb[l][1], self.out_ann, [2, [eb[l][2]]])
                                            
            self.ss = eb[0][0]
            self.es = eb[len(eb)-1][1]
            self.putx([0, ['Oregon ' + oregon_data[i][2] + ' - ' +
                            oregon_data[i][1]]]) # comment to screen

            self.putp(eb)                   # send ook to stacked decoders
            
            start += offset
    
    def decode(self):
        while True:
            self.wait([{0: 'e'}, {'skip': 200}])
            offset = self.samplenum
            if not self.displayed:
                self.displayed = 1
                if self.type == 'Oregon':
                    self.oregon_ook_gen(offset)
            
