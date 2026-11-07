import unittest

def decode(data, count, fmt):
    p=0; out=[]
    def take():
        nonlocal p
        if p>=len(data): raise ValueError('truncated')
        v=data[p]; p+=1; return v
    if fmt==22018:
        while len(out)<count: out.append(take())
    elif fmt==22258:
        while len(out)<count:
            token=take()
            if token>127:
                n=token-128
                if n<=0 or n>count-len(out): raise ValueError('bad literal count')
                out.extend(take() for _ in range(n))
            else:
                n=token
                if n<=0 or n>count-len(out): raise ValueError('bad repeat count')
                v=take(); out.extend([v]*n)
    else: raise ValueError('unsupported')
    return out,p

class Build208PixelFormatTests(unittest.TestCase):
    def test_5602_raw_indices(self):
        self.assertEqual(decode([0,1,2,255],4,22018),([0,1,2,255],4))
    def test_56f2_repeat_run(self):
        self.assertEqual(decode([3,7],3,22258),([7,7,7],2))
    def test_56f2_literal_run(self):
        self.assertEqual(decode([130,4,5],2,22258),([4,5],3))
    def test_56f2_mixed_runs(self):
        self.assertEqual(decode([2,9,130,3,4],4,22258),([9,9,3,4],5))
    def test_zero_run_rejected(self):
        with self.assertRaises(ValueError): decode([0,1],1,22258)
    def test_overrun_rejected(self):
        with self.assertRaises(ValueError): decode([130,1,2],1,22258)

if __name__=='__main__': unittest.main()
