package com.wrmsr.iceworm.util.lazy;

import java.util.function.Supplier;

public final class SupplierLazyValue<T>
{
    private volatile boolean isSet = false;
    private volatile T value = null;

    public T get(Supplier<T> supplier)
    {
        if (!isSet) {
            synchronized (this) {
                if (!isSet) {
                    value = supplier.get();
                    isSet = true;
                }
            }
        }
        return value;
    }

    @Override
    public String toString()
    {
        return "SupplierLazyValue{" +
                "isSet=" + isSet +
                ", value=" + value +
                '}';
    }
}
