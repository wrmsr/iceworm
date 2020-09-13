package com.wrmsr.iceworm.util.collect;

import java.util.stream.Stream;
import java.util.stream.StreamSupport;

public interface StreamableIterable<T>
        extends Iterable<T>
{
    default Stream<T> stream()
    {
        return StreamSupport.stream(spliterator(), false);
    }
}
