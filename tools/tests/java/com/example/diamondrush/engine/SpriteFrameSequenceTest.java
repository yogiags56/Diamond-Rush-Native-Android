package com.example.diamondrush.engine;

public final class SpriteFrameSequenceTest {
    private static void eq(int a,int b){if(a!=b)throw new AssertionError(a+" != "+b);}
    private static void fails(Runnable r){try{r.run();throw new AssertionError("expected rejection");}catch(IllegalArgumentException ok){}}
    public static void main(String[] args) {
        SpriteFrameSequence s=new SpriteFrameSequence(8,100);
        eq(s.currentFrame(),0);
        s.advance(99); eq(s.currentFrame(),0);
        s.advance(1); eq(s.currentFrame(),1);
        s.advance(250); eq(s.currentFrame(),3);
        s.advance(500); eq(s.currentFrame(),0);
        s.advance(1000); eq(s.currentFrame(),2);
        s.reset(); eq(s.currentFrame(),0);
        fails(()->new SpriteFrameSequence(0,100));
        fails(()->new SpriteFrameSequence(8,0));
        fails(()->s.advance(-1));
        System.out.println("PASS: 10 sprite frame sequence tests");
    }
}
