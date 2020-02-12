public class TryCatch {
    public void test() {
        try {
         int i = 1 / 0;
        } catch(ArithmeticException e) {
            return;
        } catch(Exception e) {
            return;
        }
    }
}
