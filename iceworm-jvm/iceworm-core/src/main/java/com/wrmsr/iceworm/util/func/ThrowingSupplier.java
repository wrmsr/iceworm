package com.wrmsr.iceworm.util.func;

import java.util.function.Supplier;

@FunctionalInterface
public interface ThrowingSupplier<T>
{
    T get()
            throws Exception;

    static <T> T rethrowingGet(ThrowingSupplier<T> supplier)
    {
        try {
            return supplier.get();
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    static <T> Supplier<T> rethrowing(ThrowingSupplier<T> supplier)
    {
        return () -> rethrowingGet(supplier);
    }
}
