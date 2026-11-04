import com.example.diamondrush.engine.OriginalGameplayInput;

public final class OriginalGameplayInputTest {
    private static int checks;
    public static void main(String[] args) {
        check(OriginalGameplayInput.contains(1 | 4096, OriginalGameplayInput.MASK_4097));
        check(!OriginalGameplayInput.contains(8, OriginalGameplayInput.MASK_4097));
        check(OriginalGameplayInput.contains(2 | 262144, OriginalGameplayInput.MASK_262146));
        check(OriginalGameplayInput.contains(4 | 16384, OriginalGameplayInput.MASK_16388));
        check(OriginalGameplayInput.contains(8 | 65536, OriginalGameplayInput.MASK_65544));
        check(OriginalGameplayInput.contains(16 | 32768, OriginalGameplayInput.MASK_32784));
        check(OriginalGameplayInput.contains(16 | 128 | 256, OriginalGameplayInput.MASK_32944));
        check(OriginalGameplayInput.contains(16 | 64 | 32768, OriginalGameplayInput.MASK_33008));
        check(OriginalGameplayInput.contains(524288, OriginalGameplayInput.MASK_1048575));
        check(!OriginalGameplayInput.contains(1 << 22, OriginalGameplayInput.MASK_1048575));
        System.out.println("PASS: " + checks + " gameplay input mask checks");
    }
    private static void check(boolean ok) {
        checks++;
        if (!ok) throw new AssertionError("gameplay mask check " + checks);
    }
}
