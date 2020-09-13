package com.wrmsr.iceworm.util.func;

@FunctionalInterface
public interface ThrowingFunction<T, R>
{
    R apply(T t)
            throws Exception;
}
