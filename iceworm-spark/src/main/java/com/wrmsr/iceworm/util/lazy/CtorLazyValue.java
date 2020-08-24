package com.wrmsr.iceworm.util.lazy;

import java.util.function.Supplier;

public final class CtorLazyValue<T>
{
    private final Supplier<T> supplier;

    private volatile boolean isSet = false;
    private volatile T value = null;

    public CtorLazyValue(Supplier<T> supplier)
    {
        this.supplier = supplier;
    }

    public T get()
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
        return "CtorLazyValue{" +
                "supplier=" + supplier +
                ", isSet=" + isSet +
                ", value=" + value +
                '}';
    }
}
