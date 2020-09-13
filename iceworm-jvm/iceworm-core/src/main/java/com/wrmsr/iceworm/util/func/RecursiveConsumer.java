package com.wrmsr.iceworm.util.func;

import com.wrmsr.iceworm.util.Cell;

import java.util.function.Consumer;

@FunctionalInterface
public interface RecursiveConsumer<T>
{
    void accept(Consumer<T> fn, T arg);

    static <T> void acceptRecursive(RecursiveConsumer<T> fn, T arg)
    {
        Cell<Consumer<T>> rec = Cell.of(null);
        rec.set(recArg -> fn.accept(rec.get(), recArg));
        fn.accept(rec.get(), arg);
    }
}
