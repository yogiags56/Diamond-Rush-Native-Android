package com.example.diamondrush.engine;

public final class DecodedSpritePixelsTest {
    private static void eq(int a,int b){if(a!=b)throw new AssertionError(a+" != "+b);}
    private static void fails(Runnable r){try{r.run();throw new AssertionError("expected rejection");}catch(IllegalArgumentException|IndexOutOfBoundsException ok){}}
    public static void main(String[] args) {
        int[] palette={0xff000000,0xffffffff,0xffff0000,0xff00ff00};
        DecodedSpritePixels s=DecodedSpritePixels.decode(2,2,
                IndexedPixelDecoder.MODE_RAW_INDEXED,
                new byte[]{0,1,2,3},0,palette);
        eq(s.width,2); eq(s.height,2);
        eq(s.pixelAt(0,0),palette[0]); eq(s.pixelAt(1,0),palette[1]);
        eq(s.pixelAt(0,1),palette[2]); eq(s.pixelAt(1,1),palette[3]);
        eq(s.argb.length,4);
        fails(()->DecodedSpritePixels.decode(0,2,22018,new byte[]{0},0,palette));
        fails(()->DecodedSpritePixels.decode(-1,2,22018,new byte[]{0},0,palette));
        fails(()->DecodedSpritePixels.decode(50000,50000,22018,new byte[]{0},0,palette));
        fails(()->s.pixelAt(2,0));
        System.out.println("PASS: 9 decoded sprite pixel tests");
    }
}
