import unittest, zipfile, struct, os

def parse_section(payload):
    if len(payload)<8 or payload[:4] != bytes([0xdf,3,1,1]):
        raise ValueError("signature")
    p=6
    def count():
        nonlocal p
        if p+2>len(payload): raise ValueError("count")
        v=payload[p] | payload[p+1]<<8; p+=2
        return max(v if v<32768 else v-65536,0)
    def take(n):
        nonlocal p
        if n<0 or p+n>len(payload): raise ValueError("bounds")
        b=payload[p:p+n];p+=n;return b
    dims=take(count()*2)
    rec_count=count()
    records=take(rec_count*4)
    groups=count()
    counts=[];starts=[]
    for _ in range(groups):
        e=take(4);counts.append(e[0]);starts.append(e[2] | e[3]<<8)
        if starts[-1]>=32768: starts[-1]-=65536
    group_dims=take(groups*2)
    return dims,records,counts,starts,group_dims,p

class Build206PayloadTests(unittest.TestCase):
    def test_all_original_df03_payloads_parse(self):
        jar=os.path.join(os.path.dirname(__file__),"../original/DMR320x240-Celsius.jar")
        with zipfile.ZipFile(jar) as z:
            n=0
            for name in z.namelist():
                if not name.endswith(".f"): continue
                d=z.read(name); count=d[0]; base=1+8*count
                for i in range(count):
                    off,ln=struct.unpack_from("<II",d,1+i*8)
                    payload=d[base+off:base+off+ln]
                    if payload[:4]==bytes([0xdf,3,1,1]):
                        dims,records,counts,starts,gd,consumed=parse_section(payload)
                        self.assertEqual(len(records)%4,0)
                        self.assertEqual(len(gd),len(counts)*2)
                        for cnt,start in zip(counts,starts):
                            self.assertGreaterEqual(start,0)
                            self.assertLessEqual((start+cnt)*4,len(records))
                        n+=1
            self.assertEqual(n,94)
    def test_non_df03_rejected(self):
        with self.assertRaises(ValueError): parse_section(b"NOPE"+bytes(30))
    def test_truncated_dimension_table_rejected(self):
        with self.assertRaises(ValueError): parse_section(bytes([0xdf,3,1,1,0,0,2,0]))
    def test_record_table_truncation_rejected(self):
        with self.assertRaises(ValueError): parse_section(bytes([0xdf,3,1,1,0,0,0,0,1,0,1]))
    def test_group_table_truncation_rejected(self):
        with self.assertRaises(ValueError): parse_section(bytes([0xdf,3,1,1,0,0,0,0,0,0,1,0,1,0]))
if __name__=="__main__": unittest.main()
