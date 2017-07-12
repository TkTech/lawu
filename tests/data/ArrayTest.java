public class ArrayTest {
    public int addOne(int x){
        return x + (isSomething(0) ? 0 : 1);
    }

    public static boolean isSomething(int z) {
        return true;
    }
}
