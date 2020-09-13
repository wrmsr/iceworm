package com.wrmsr.iceworm.util;

public interface NoExceptAutoCloseable
        extends AutoCloseable
{
    @Override
    default void close()
    {
    }
}
