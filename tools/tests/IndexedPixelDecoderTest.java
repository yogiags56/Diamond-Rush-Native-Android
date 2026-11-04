import com.example.diamondrush.engine.IndexedPixelDecoder;
import java.util.Arrays;
public final class IndexedPixelDecoderTest {
  static void eq(int[] a,int... b){if(!Arrays.equals(a,b))throw new AssertionError(Arrays.toString(a)+" != "+Arrays.toString(b));}
  static void fails(Runnable r){try{r.run();throw new AssertionError("expected rejection");}catch(IllegalArgumentException expected){}}
  public static void main(String[] args){
    int[] p={0xff000000,0xffffffff,0xffff0000,0xff00ff00,0xff0000ff,0xffffff00,0xffff00ff,0xff00ffff};
    eq(IndexedPixelDecoder.decode(22018,new byte[]{0,1,2},0,3,p),p[0],p[1],p[2]);
    eq(IndexedPixelDecoder.decode(5632,new byte[]{0x12,(byte)0x34},0,4,p),p[1],p[2],p[3],p[4]);
    eq(IndexedPixelDecoder.decode(1024,new byte[]{0x1b},0,4,p),p[0],p[1],p[2],p[3]);
    eq(IndexedPixelDecoder.decode(512,new byte[]{(byte)0xa5},0,8,p),p[1],p[0],p[1],p[0],p[0],p[1],p[0],p[1]);
    eq(IndexedPixelDecoder.decode(10225,new byte[]{0, (byte)0x83,2},0,4,p),p[0],p[2],p[2],p[2]);
    eq(IndexedPixelDecoder.decode(22258,new byte[]{0,1,(byte)0x83,2},0,4,p),p[1],p[2],p[2],p[2]);
    fails(()->IndexedPixelDecoder.decode(22018,new byte[]{9},0,1,p));
    fails(()->IndexedPixelDecoder.decode(22018,new byte[]{},0,1,p));
    fails(()->IndexedPixelDecoder.decode(5632,new byte[]{0},0,1,p));
    fails(()->IndexedPixelDecoder.decode(512,new byte[]{0},0,9,p));
    fails(()->IndexedPixelDecoder.decode(123,new byte[]{0},0,1,p));
    System.out.println("PASS: 11 indexed pixel decoder tests");
  }
}
