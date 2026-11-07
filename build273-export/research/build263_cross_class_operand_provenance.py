"""Build263: bytecode-backed symbolic operand expressions for 8 cross-class renderer calls.

Expressions are transcribed from javap instruction sequences and descriptor order.
They are not runtime values. Each expression carries an evidence interval and a
conservative status; locals/fields/resource indices are symbolic, not evaluated.
"""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research'
# Stack order is JVM invocation order: receiver (for invokevirtual), then descriptor args.
SITES=[
('b','public final void a(javax.microedition.lcdui.Graphics);',87,'component_7int',[
('receiver','this.a','PROVEN','66–70'),('graphics','arg1','PROVEN','70'),('int_1','this.d','PROVEN','71–75'),('int_2','this.e','PROVEN','75–79'),('int_3','local2','PROVEN','79'),('int_4','local3','PROVEN','80'),('int_5','this.c','PROVEN','81–85'),('int_6','0','PROVEN','85'),('int_7','0','PROVEN','86')]),
('b','public final void a(javax.microedition.lcdui.Graphics);',113,'leaf_4int',[
('receiver','this.a','PROVEN','98–102'),('graphics','arg1','PROVEN','102'),('int_1','this.d','PROVEN','103–107'),('int_2','local2','PROVEN','107'),('int_3','local3','PROVEN','108'),('int_4','this.c','PROVEN','109–113')]),
('b','public final void a(javax.microedition.lcdui.Graphics);',141,'composite_6int',[
('receiver','this.a','PROVEN','124–128'),('graphics','arg1','PROVEN','128'),('int_1','this.e','PROVEN','129–133'),('int_2','local2','PROVEN','133'),('int_3','local3','PROVEN','134'),('int_4','this.c','PROVEN','135–139'),('int_5','0','PROVEN','139'),('int_6','0','PROVEN','140')]),
('c','public final void a(javax.microedition.lcdui.Graphics);',280,'component_7int',[
('receiver','a[this.f]','PROVEN','242–249'),('graphics','arg1','PROVEN','250'),('int_1','0','PROVEN','251'),('int_2','this.b % a[this.f].a(0)','DERIVED','252–268'),('int_3','this.c','PROVEN','269–273'),('int_4','this.d','PROVEN','273–277'),('int_5','0','PROVEN','277'),('int_6','0','PROVEN','278'),('int_7','0','PROVEN','279')]),
('c','public final void a(javax.microedition.lcdui.Graphics);',304,'composite_6int',[
('receiver','a[0]','PROVEN','283–288'),('graphics','arg1','PROVEN','288'),('int_1','this.e','PROVEN','289–293'),('int_2','this.c','PROVEN','293–297'),('int_3','this.d','PROVEN','298–301'),('int_4','0','PROVEN','301'),('int_5','0','PROVEN','302'),('int_6','0','PROVEN','303')]),
('c','public final void a(javax.microedition.lcdui.Graphics);',382,'composite_6int',[
('receiver','a[1]','PROVEN','355–360'),('graphics','arg1','PROVEN','360'),('int_1','this.g','PROVEN','361–365'),('int_2','this.c + 90','DERIVED','366–372'),('int_3','this.d - 6','DERIVED','373–378'),('int_4','0','PROVEN','379'),('int_5','0','PROVEN','380'),('int_6','0','PROVEN','381')]),
('c','private void a(javax.microedition.lcdui.Graphics, byte[], int);',873,'composite_6int',[
('receiver','a[local5]','PROVEN','859–865'),('graphics','arg1','PROVEN','865'),('int_1','local2','PROVEN','866–867'),('int_2','local0','PROVEN','867–868'),('int_3','local4','PROVEN','868–870'),('int_4','0','PROVEN','870'),('int_5','0','PROVEN','871'),('int_6','0','PROVEN','872')]),
('g','public static void a(javax.microedition.lcdui.Graphics);',80,'composite_6int',[
('receiver','i.a(2)','PROVEN','27–34'),('graphics','arg0','PROVEN','35'),('int_1','0','PROVEN','61–63'),('int_2','local1 * 24','DERIVED','63–67'),('int_3','(local2 - 1) * 24 + static b','DERIVED','67–77'),('int_4','0','PROVEN','77'),('int_5','0','PROVEN','78'),('int_6','0','PROVEN','79')]),
]
rows=[]
for cls,method,off,fam,ops in SITES:
    for idx,(role,expr,status,evidence) in enumerate(ops):
        rows.append(dict(caller_class=cls,caller_method=method,callsite_offset=off,renderer_family=fam,stack_position=idx,operand_role=role,symbolic_expression=expr,evidence_status=status,evidence_offsets=evidence,runtime_value_known=False))
path=OUT/'build263_cross_class_operand_provenance.csv'
with path.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=[]
for cls,method,off,fam,ops in SITES:
    summary.append(dict(caller_class=cls,caller_method=method,callsite_offset=off,renderer_family=fam,operand_slots=len(ops),proven_operands=sum(x[2]=='PROVEN' for x in ops),derived_operands=sum(x[2]=='DERIVED' for x in ops),unknown_operands=sum(x[2]=='UNKNOWN' for x in ops),runtime_values_decoded=False))
with (OUT/'build263_operand_provenance_summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
print('callsites:',len(summary),'operand records:',len(rows))
print('PROVEN:',sum(r['evidence_status']=='PROVEN' for r in rows),'DERIVED:',sum(r['evidence_status']=='DERIVED' for r in rows),'UNKNOWN:',sum(r['evidence_status']=='UNKNOWN' for r in rows))
