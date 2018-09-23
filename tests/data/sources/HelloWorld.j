.bytecode 49.0
.class public HelloWorld
    .super java/lang/Object

    ;
    ; standard initializer (calls java.lang.Object's initializer)
    ;
    .method public <init>()V
        .limit locals 1
        .limit stack 2

        aload_0
        invokevirtual java/lang/Object/<init>()V
        return
    .end method

    ;
    ; main() - prints out Hello World
    ;
    .method public static main([Ljava/lang/String;)V
        .limit stack 2   ; up to two items can be pushed
        .limit locals 1

        ; push System.out onto the stack
        getstatic java/lang/System/out Ljava/io/PrintStream;

        ; push a string onto the stack
        ldc "Hello World!"

        ; call the PrintStream.println() method.
        invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V

        ; done
        return
    .end method
.end class