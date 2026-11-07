import unittest

def graph(counts, starts, records):
    edges=[]
    for group,count in enumerate(counts):
        for component in range(count):
            base=(starts[group]+component)*4
            if base < 0 or base+4 > len(records):
                raise ValueError("record bounds")
            child=records[base] & 255
            control=records[base+3] & 255
            if control & 0x10:
                if child >= len(counts): edges.append((group,child,component))
                else: edges.append((group,child,component))
    return edges

def cycles(node_count, edges):
    adj={i:[] for i in range(node_count)}
    for a,b,_ in edges:
        if b < node_count: adj[a].append(b)
    color=[0]*node_count; stack=[]; found=[]
    def visit(n):
        color[n]=1; stack.append(n)
        for m in adj[n]:
            if color[m]==0: visit(m)
            elif color[m]==1:
                i=stack.index(m); found.append(stack[i:]+[m])
        stack.pop(); color[n]=2
    for n in range(node_count):
        if color[n]==0: visit(n)
    return found

class CompositeGraphTests(unittest.TestCase):
    def test_nested_target_is_group_edge(self):
        data=bytes([2,0,0,0x10, 7,0,0,0])
        self.assertEqual(graph([1],[0],data),[(0,2,0)])
    def test_leaf_is_not_graph_edge(self):
        self.assertEqual(graph([1],[0],bytes([255,0,0,0])),[])
    def test_nested_cycle_detected(self):
        edges=[(0,1,0),(1,0,0)]
        self.assertEqual(cycles(2,edges),[[0,1,0]])
    def test_acyclic_chain(self):
        self.assertEqual(cycles(3,[(0,1,0),(1,2,0)]),[])
    def test_invalid_nested_target_retained_for_diagnostics(self):
        self.assertEqual(graph([1],[0],bytes([9,0,0,0x10])),[(0,9,0)])
    def test_truncated_payload_rejected(self):
        with self.assertRaises(ValueError): graph([1],[0],bytes([1,2,3]))
    def test_non_nested_control_bit_does_not_create_edge(self):
        self.assertEqual(graph([1],[0],bytes([0,0,0,0x0f])),[])
    def test_multiple_edges_preserve_component_order(self):
        data=bytes([1,0,0,0x10, 2,0,0,0x10])
        self.assertEqual(graph([2],[0],data),[(0,1,0),(0,2,1)])

if __name__ == "__main__": unittest.main()
