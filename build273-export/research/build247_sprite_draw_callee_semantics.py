"""Build247: inspect original f.a(Graphics, ...) callee semantics via javap."""
from pathlib import Path
import subprocess, re, csv
ROOT=Path(__file__).resolve().parents[1]
jar=ROOT/'original.jar'
text=subprocess.check_output(['javap','-classpath',str(jar),'-c','-p','f'],text=True)
methods={}
lines=text.splitlines()
i=0
while i<len(lines):
    m=re.match(r'  public final void a\(javax\.microedition\.lcdui\.Graphics(.*?)\);',lines[i])
    if m:
        sig=m.group(1); start=i; i+=1
        while i<len(lines) and not re.match(r'  (public|private|protected)',lines[i]): i+=1
        methods[sig]= '\n'.join(lines[start:i])
    else:i+=1
expected={
 ', int, int, int, int, int, int, int':'7-int',
 ', int, int, int, int, int, int':'6-int',
 ', int, int, int, int':'4-int',
}
assert all(k in methods for k in expected), methods.keys()
seven=methods[', int, int, int, int, int, int, int']
six=methods[', int, int, int, int, int, int']
four=methods[', int, int, int, int']
checks={
 '7-int reads composite offset table a:[S': 'Field a:[S' in seven and 'saload' in seven,
 '7-int reads component records c:[B': 'Field c:[B' in seven and 'baload' in seven,
 '7-int applies component flag transform and offsets': 'bipush        32' in seven and 'iload         6' in seven,
 '7-int delegates to 6-int recursive composite routine': 'Method a:(Ljavax/microedition/lcdui/Graphics;IIIIII)V' in seven,
 '6-int reads composite component count g:[B': 'Field g:[B' in six and 'if_icmpge' in six,
 '6-int iterates component reference table b:[S': 'Field b:[S' in six and 'saload' in six,
 '6-int reads nested component metadata h:[B': 'Field h:[B' in six,
 '6-int supports nested composite recursion': six.count('Method a:(Ljavax/microedition/lcdui/Graphics;IIIIII)V')>=1,
 '6-int dispatches leaf sprite to 4-int routine': 'Method a:(Ljavax/microedition/lcdui/Graphics;IIII)V' in six,
 '4-int resolves sprite dimensions from f:[B': 'Field f:[B' in four,
 '4-int draws image region': 'Graphics.drawRegion' in four,
}
assert all(checks.values()), checks
rows=[
 {'signature':'Graphics + 7 ints','role':'COMPOSITE_COMPONENT_ENTRY','evidence':'Indexes composite offset table; selects one component; applies component flags/offsets; delegates to six-int routine.','confirmed':True},
 {'signature':'Graphics + 6 ints','role':'COMPOSITE_GROUP_EXPANSION','evidence':'Reads group component count; iterates component refs; applies per-component offsets/flags; recurses for nested composites or delegates leaves to four-int routine.','confirmed':True},
 {'signature':'Graphics + 4 ints','role':'LEAF_SPRITE_DRAW','evidence':'Resolves sprite image/pixels and dimensions; calls Graphics.drawRegion with selected transform and destination coordinates.','confirmed':True},
]
out=ROOT/'research/build247_sprite_draw_callee_semantics.csv'
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
report=['Build247 original f.a(Graphics, ...) callee audit','',f'Original JAR: {jar.name}','']
report += [f'{"PASS" if v else "FAIL"}: {k}' for k,v in checks.items()]
report += ['', 'Confirmed call hierarchy:', 'Graphics + 7 ints → component selection/offset application → Graphics + 6 ints', 'Graphics + 6 ints → composite group expansion → recursive composite or Graphics + 4 ints', 'Graphics + 4 ints → leaf sprite image/pixel resolution → Graphics.drawRegion', '', 'Argument meaning is established structurally for the callee methods. Caller-side values at individual i.D()V callsites remain a separate provenance task.']
(ROOT/'research/build247_sprite_draw_callee_semantics.txt').write_text('\n'.join(report)+'\n')
print('\n'.join(report))
