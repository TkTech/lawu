.class public HelloWorld
    .bytecode 49.0
    .super java/lang/Object

    ;
    ; standard initializer (calls java.lang.Object's initializer)
    ;
    .method public <init>()V
        .limit locals 1
        .limit stack 2

        aload_0
        invokevirtual java/lang/Object <init> ()V
        return
    .end method

    ;
    ; main() - prints out Hello World
    ;
    .method public static main([Ljava/lang/String;)V
        .limit locals 1
        .limit stack 2

        getstatic java/lang/System out Ljava/io/PrintStream;
        ldc "Hello World!"
        invokevirtual java/io/PrintStream println (Ljava/lang/String;)V

        return
    .end method
.end class
