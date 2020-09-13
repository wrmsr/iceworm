package com.wrmsr.iceworm.util.func;

import java.util.function.Consumer;

@FunctionalInterface
public interface ThrowableThrowingConsumer<T>
{
    void accept(T t)
            throws Throwable;

    static <T> void throwableRethrowingAccept(ThrowableThrowingConsumer<T> consumer, T t)
    {
        try {
            consumer.accept(t);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
        catch (Throwable e) {
            Thread.currentThread().getUncaughtExceptionHandler().uncaughtException(Thread.currentThread(), e);
            throw new RuntimeException(e);
        }
    }

    static <T> Consumer<T> throwableRethrowing(ThrowableThrowingConsumer<T> consumer)
    {
        return (t) -> throwableRethrowingAccept(consumer, t);
    }
}
