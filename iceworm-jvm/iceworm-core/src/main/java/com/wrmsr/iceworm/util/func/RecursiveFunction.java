package com.wrmsr.iceworm.util.func;

import com.wrmsr.iceworm.util.Cell;

import java.util.function.Function;

@FunctionalInterface
public interface RecursiveFunction<T, R>
{
    R apply(Function<T, R> fn, T arg);

    static <T, R> R applyRecursive(RecursiveFunction<T, R> fn, T arg)
    {
        Cell<Function<T, R>> rec = Cell.of(null);
        rec.set(recArg -> fn.apply(rec.get(), recArg));
        return fn.apply(rec.get(), arg);
    }
}
