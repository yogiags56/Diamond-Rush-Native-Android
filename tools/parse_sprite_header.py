#!/usr/bin/env python3
"""Bounds-checked parser for the verified initial metadata prefix of Diamond Rush class-f payloads.

Mirrors the first three verified table groups and deliberately stops at byte
48 for the known gen0_section_00 fixture. Later fields are not generalized yet.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse, json

class FormatError(ValueError): pass
class Reader:
    def __init__(self, data): self.data, self.pos = data, 0
    def take(self, n, label):
        if n < 0 or self.pos + n > len(self.data):
            raise FormatError(f'{label}: need {n} bytes at {self.pos}, payload has {len(self.data)}')
        out=self.data[self.pos:self.pos+n]; self.pos+=n; return out
    def i16(self,label):
        b=self.take(2,label); v=b[0] | b[1]<<8
        return v-65536 if v>=32768 else v

@dataclass
class Header:
    payload_size:int
    table0_entries:int
    table1_records:int
    table2_records:int
    table2_aux_bytes:int
    metadata_end:int

def parse(data:bytes)->Header:
    r=Reader(data); r.take(6,'fixed prefix')
    n0=r.i16('table0 count')
    if n0<0: raise FormatError('negative table0 count')
    r.take(n0*2,'table0 short entries')
    n1=r.i16('table1 count')
    if n1<0: raise FormatError('negative table1 count')
    r.take(n1*4,'table1 four-byte records')
    n2=r.i16('table2 count')
    if n2<0: raise FormatError('negative table2 count')
    r.take(n2*4,'table2 byte/skip/short records')
    r.take(n2*2,'table2 auxiliary short table')
    return Header(len(data),n0,n1,n2,n2*2,r.pos)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('payload',type=Path); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try:
        h=parse(a.payload.read_bytes()); d=h.__dict__
        print(json.dumps(d,indent=2) if a.json else '\n'.join(f'{k}={v}' for k,v in d.items()))
    except (OSError,FormatError) as e: raise SystemExit(f'INVALID: {e}')
if __name__=='__main__': main()
