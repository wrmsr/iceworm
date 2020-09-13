package com.wrmsr.iceworm.util.collect;

import javax.annotation.concurrent.Immutable;
import java.util.AbstractMap;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;

@Immutable
public abstract class AbstractUnmodifiableMap<K, V>
        extends AbstractMap<K, V>
{
    @Override
    public final void replaceAll(BiFunction<? super K, ? super V, ? extends V> function)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V putIfAbsent(K key, V value)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final boolean remove(Object key, Object value)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final boolean replace(K key, V oldValue, V newValue)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V replace(K key, V value)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V computeIfPresent(K key, BiFunction<? super K, ? super V, ? extends V> remappingFunction)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V compute(K key, BiFunction<? super K, ? super V, ? extends V> remappingFunction)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V merge(K key, V value, BiFunction<? super V, ? super V, ? extends V> remappingFunction)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V put(K key, V value)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final V remove(Object key)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final void putAll(Map<? extends K, ? extends V> m)
    {
        throw new UnsupportedOperationException();
    }

    @Override
    public final void clear()
    {
        throw new UnsupportedOperationException();
    }
}
