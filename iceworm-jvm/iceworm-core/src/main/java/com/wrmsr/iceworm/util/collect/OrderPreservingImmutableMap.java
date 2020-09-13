package com.wrmsr.iceworm.util.collect;

import com.google.common.collect.ImmutableMap;

import java.util.Collection;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.function.BiConsumer;

public final class OrderPreservingImmutableMap<K, V>
        extends AbstractUnmodifiableMap<K, V>
        implements Ordered
{
    private final ImmutableMap<K, V> map;

    public OrderPreservingImmutableMap(Map<K, V> map)
    {
        this.map = (map instanceof OrderPreservingImmutableMap) ? ((OrderPreservingImmutableMap<K, V>) map).map : ImmutableMap.copyOf(map);
    }

    @Override
    public String toString()
    {
        return "OrderPreservingImmutableMap{" +
                "map=" + map +
                '}';
    }

    @Override
    public boolean equals(Object o)
    {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        OrderPreservingImmutableMap<?, ?> that = (OrderPreservingImmutableMap<?, ?>) o;
        return Objects.equals(map, that.map);
    }

    @Override
    public int hashCode()
    {
        return Objects.hash(map);
    }

    @Override
    public int size()
    {
        return map.size();
    }

    @Override
    public boolean isEmpty()
    {
        return map.isEmpty();
    }

    @Override
    public boolean containsKey(Object key)
    {
        return map.containsKey(key);
    }

    @Override
    public boolean containsValue(Object value)
    {
        return map.containsValue(value);
    }

    @Override
    public V get(Object key)
    {
        return map.get(key);
    }

    @Override
    public Set<K> keySet()
    {
        return map.keySet();
    }

    @Override
    public Collection<V> values()
    {
        return map.values();
    }

    @Override
    public Set<Entry<K, V>> entrySet()
    {
        return map.entrySet();
    }

    @Override
    public V getOrDefault(Object key, V defaultValue)
    {
        return map.getOrDefault(key, defaultValue);
    }

    @Override
    public void forEach(BiConsumer<? super K, ? super V> action)
    {
        map.forEach(action);
    }
}
