// Standalone logic test for TouchInput's pointer/ref-count algorithm.
// Android-specific wrapper is tested conceptually; this mirrors its transitions.
import java.util.*;
public final class TouchInputLogicTest {
  static final class State {
    Map<Integer,Integer> pointers = new HashMap<>();
    Map<Integer,Integer> counts = new HashMap<>(); int held;
    void set(int id,int next) {
      int old=pointers.getOrDefault(id,0), changed=old^next;
      for(int bit=0;bit<32;bit++){int f=1<<bit;if((changed&f)==0)continue;
        int n=counts.getOrDefault(f,0);
        if((next&f)!=0){counts.put(f,++n);held|=f;}
        else if(--n<=0){counts.remove(f);held&=~f;} else counts.put(f,n);
      }
      if(next==0)pointers.remove(id);else pointers.put(id,next);
    }
  }
  public static void main(String[] args) {
    State s=new State();
    s.set(10,1); s.set(11,1); if(s.held!=1)throw new AssertionError("shared hold");
    s.set(10,0); if(s.held!=1)throw new AssertionError("premature release");
    s.set(11,0); if(s.held!=0)throw new AssertionError("final release");
    s.set(10,3); s.set(11,2); s.set(10,1);
    if(s.held!=3)throw new AssertionError("overlap transition");
    s.set(11,0); if(s.held!=1)throw new AssertionError("independent bit");
    s.set(10,0); if(s.held!=0)throw new AssertionError("cleanup");
    System.out.println("PASS: shared holds, overlapping masks, independent release, cleanup");
  }
}
