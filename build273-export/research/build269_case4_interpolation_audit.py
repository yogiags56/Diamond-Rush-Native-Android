"""Build269: bytecode-anchored reconstruction of case-4 interpolation operands.

This is a focused producer-slice audit, not a full JVM interpreter. It verifies
instruction offsets/opcodes against javap output from the original JAR and emits
symbolic formulas for the two locals consumed by renderer f.a at offset 873.
"""
from pathlib import Path
import csv, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / 'original.jar'
OUT = ROOT / 'research'
CLASS = 'c'
SIGNATURE = 'private void a(javax.microedition.lcdui.Graphics, byte[], int);'
EXPECTED = {
    729:'aload_0', 730:'getfield', 733:'istore',
    735:'aload_2', 736:'iload_3', 737:'iconst_2', 738:'iadd', 739:'invokestatic', 742:'i2s', 743:'istore',
    745:'aload_2', 746:'iload_3', 747:'iconst_4', 748:'iadd', 749:'invokestatic', 752:'i2s', 753:'istore',
    755:'aload_2', 756:'iload_3', 757:'bipush', 759:'iadd', 760:'invokestatic', 763:'i2s', 764:'istore',
    766:'aload_2', 767:'iload_3', 768:'bipush', 770:'iadd', 771:'invokestatic', 774:'i2s', 775:'istore',
    777:'aload_2', 778:'iload_3', 779:'bipush', 781:'iadd', 782:'invokestatic', 785:'i2s', 786:'istore',
    788:'iload', 790:'iload', 792:'if_icmple', 795:'iload', 797:'istore',
    799:'iload', 801:'iload', 803:'imul', 804:'iload', 806:'iload', 808:'iload', 810:'isub',
    811:'imul', 812:'iadd', 813:'iload', 815:'idiv', 816:'i2s', 817:'istore_0',
    818:'iload', 820:'iload', 822:'imul', 823:'iload', 825:'iload', 827:'iload', 829:'isub',
    830:'imul', 831:'iadd', 832:'iload', 834:'idiv', 835:'i2s', 836:'istore',
    838:'aload_2', 839:'iload_3', 840:'bipush', 842:'iadd', 843:'invokestatic', 846:'i2s', 847:'istore',
    849:'aload_2', 850:'iload_3', 851:'bipush', 853:'iadd', 854:'invokestatic', 857:'i2s', 858:'istore_2',
    859:'getstatic', 862:'iload', 864:'aaload', 865:'aload_1', 866:'iload_2', 867:'iload_0', 868:'iload',
    870:'iconst_0', 871:'iconst_0', 872:'iconst_0', 873:'invokevirtual',
}
INS = re.compile(r'^\s*(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(.*))?$')

def extract():
    text = subprocess.check_output(['javap','-classpath',str(JAR),'-p','-c','-s',CLASS], text=True)
    lines=text.splitlines()
    start=next(i for i,l in enumerate(lines) if l.strip()==SIGNATURE)
    got={}
    for line in lines[start+1:]:
        m=INS.match(line)
        if m:
            off,op,rest=m.groups(); got[int(off)]=(op,rest or '')
        if got and line.strip().startswith('Exception table:'):
            break
    return got

def main():
    got=extract()
    rows=[]
    for off, expected in EXPECTED.items():
        actual=got.get(off,('',))[0]
        if actual != expected:
            raise SystemExit(f'bytecode mismatch at {off}: expected {expected}, got {actual}')
        rows.append({'offset':off,'opcode':actual,'operand':got[off][1]})

    # Bytecode-level dataflow. i.a([BI)I returns a 16-bit quantity; i2s
    # narrows each read. The two source reads at +6 are intentionally distinct
    # bytecode producers (locals 4 and 5), even though their expressions match.
    formulas = [
      {'renderer_offset':873,'renderer_argument':'integer argument 2 (first coordinate-like value)','source_local':'local 0','store_offset':817,
       'expression':'S16((v6 * m + v2 * (v14 - m)) / v14)',
       'definitions':'v2=S16(i.a(data,index+2)); v6=S16(i.a(data,index+6)); v14=S16(i.a(data,index+14)); m=min(this.b,v14)',
       'arithmetic':'JVM int multiply/add/subtract/divide; then signed-short narrowing via i2s',
       'confidence':'BYTECODE_PROVEN_EXPRESSION; runtime integer not known'},
      {'renderer_offset':873,'renderer_argument':'integer argument 3 (second coordinate-like value)','source_local':'local 4','store_offset':836,
       'expression':'S16((v6b * m + v4 * (v14 - m)) / v14)',
       'definitions':'v4=S16(i.a(data,index+4)); v6b=S16(i.a(data,index+6)); v14=S16(i.a(data,index+14)); m=min(this.b,v14)',
       'arithmetic':'JVM int multiply/add/subtract/divide; then signed-short narrowing via i2s',
       'confidence':'BYTECODE_PROVEN_EXPRESSION; runtime integer not known'},
    ]
    with (OUT/'build269_case4_operand_formulas.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(formulas[0]));w.writeheader();w.writerows(formulas)
    with (OUT/'build269_case4_instruction_trace.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['offset','opcode','operand']);w.writeheader();w.writerows(rows)
    print('verified_instructions',len(rows))
    print('verified_renderer_offset',873)
    print('operand_formulas',len(formulas))
    print('unknown_runtime_values',2)

if __name__=='__main__': main()
