package com.wrmsr.iceworm.util.func;

import java.util.function.Supplier;

@FunctionalInterface
public interface ThrowableThrowingSupplier<T>
{
    T get()
            throws Throwable;

    static <T> T throwableRethrowingGet(ThrowableThrowingSupplier<T> supplier)
    {
        try {
            return supplier.get();
        } catch (Exception e) {
            throw new RuntimeException(e);
        } catch (Throwable e) {
            Thread.currentThread().getUncaughtExceptionHandler().uncaughtException(Thread.currentThread(), e);
            throw new RuntimeException(e);
        }
    }

    static <T> Supplier<T> throwableRethrowing(ThrowableThrowingSupplier<T> supplier)
    {
        return () -> throwableRethrowingGet(supplier);
    }
}
