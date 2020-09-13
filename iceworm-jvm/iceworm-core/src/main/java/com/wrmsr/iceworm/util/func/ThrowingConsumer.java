package com.wrmsr.iceworm.util.func;

import java.util.function.Consumer;

@FunctionalInterface
public interface ThrowingConsumer<T>
{
    void accept(T t)
            throws Exception;

    static <T> void rethrowingAccept(ThrowingConsumer<T> consumer, T t)
    {
        try {
            consumer.accept(t);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    static <T> Consumer<T> rethrowing(ThrowingConsumer<T> consumer)
    {
        return (t) -> rethrowingAccept(consumer, t);
    }
}
