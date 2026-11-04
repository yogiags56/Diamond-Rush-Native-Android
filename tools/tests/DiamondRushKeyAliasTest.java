import com.example.diamondrush.ui.DiamondRushKeyMap;

public final class DiamondRushKeyAliasTest {
    public static void main(String[] args) {
        int[][] cases = {
            {98,262144},{102,16384},{103,32768},{104,65536},
            {106,512},{109,1024},{110,524288},{114,2048},
            {115,4096},{116,256},{118,131072},{121,8192},
            {120,0},{97,0},{-10,-10}
        };
        for (int[] pair : cases) {
            int got = DiamondRushKeyMap.toInputBit(pair[0]);
            if (got != pair[1]) throw new AssertionError(pair[0]+" -> "+got+" expected "+pair[1]);
        }
        System.out.println("PASS: " + cases.length + " key alias checks");
    }
}
