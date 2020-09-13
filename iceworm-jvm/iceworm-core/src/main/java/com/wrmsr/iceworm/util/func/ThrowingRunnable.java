package com.wrmsr.iceworm.util.func;

@FunctionalInterface
public interface ThrowingRunnable
{
    void run()
            throws Exception;
}
