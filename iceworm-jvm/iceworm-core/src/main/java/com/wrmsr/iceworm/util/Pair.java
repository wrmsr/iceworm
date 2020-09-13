package com.wrmsr.iceworm.util;

import java.util.Iterator;
import java.util.Map;
import java.util.Objects;

import static com.google.common.base.Preconditions.checkState;

public interface Pair<K, V>
        extends Map.Entry<K, V>
{
    K getFirst();

    V getSecond();

    default K first()
    {
        return getFirst();
    }

    default V second()
    {
        return getSecond();
    }

    default K getKey()
    {
        return getFirst();
    }

    default V getValue()
    {
        return getSecond();
    }

    final class Immutable<K, V>
            implements Pair<K, V>
    {
        private final K first;
        private final V second;

        public Immutable(K first, V second)
        {
            this.first = first;
            this.second = second;
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
            Immutable<?, ?> pair = (Immutable<?, ?>) o;
            return Objects.equals(first, pair.first) &&
                    Objects.equals(second, pair.second);
        }

        @Override
        public int hashCode()
        {
            return Objects.hash(first, second);
        }

        @Override
        public String toString()
        {
            return "Pair.Immutable{" +
                    "first=" + first +
                    ", second=" + second +
                    '}';
        }

        @Override
        public K getFirst()
        {
            return first;
        }

        @Override
        public V getSecond()
        {
            return second;
        }

        @Override
        public V setValue(V second)
        {
            throw new UnsupportedOperationException();
        }
    }

    static <K, V> Immutable<K, V> immutable(K first, V second)
    {
        return new Immutable<>(first, second);
    }

    static <K, V> Immutable<K, V> immutable(Map.Entry<K, V> entry)
    {
        return new Immutable<>(entry.getKey(), entry.getValue());
    }

    static <T> Immutable<T, T> immutable(Iterator<T> iterator)
    {
        T key = iterator.next();
        T value = iterator.next();
        checkState(!iterator.hasNext());
        return immutable(key, value);
    }

    static <T> Immutable<T, T> immutable(Iterable<T> iterable)
    {
        return immutable(iterable.iterator());
    }

    final class Mutable<K, V>
            implements Pair<K, V>
    {
        private K first;
        private V second;

        public Mutable(K first, V second)
        {
            this.first = first;
            this.second = second;
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
            Mutable<?, ?> pair = (Mutable<?, ?>) o;
            return Objects.equals(first, pair.first) &&
                    Objects.equals(second, pair.second);
        }

        @Override
        public int hashCode()
        {
            return Objects.hash(first, second);
        }

        @Override
        public String toString()
        {
            return "Pair.Mutable{" +
                    "first=" + first +
                    ", second=" + second +
                    '}';
        }

        @Override
        public K getFirst()
        {
            return first;
        }

        @Override
        public V getSecond()
        {
            return second;
        }

        public K setFirst(K first)
        {
            K old = this.first;
            this.first = first;
            return old;
        }

        public V setSecond(V second)
        {
            V old = this.second;
            this.second = second;
            return old;
        }

        @Override
        public V setValue(V second)
        {
            return setSecond(second);
        }
    }

    static <K, V> Mutable<K, V> mutable(K first, V second)
    {
        return new Mutable<>(first, second);
    }

    static <K, V> Mutable<K, V> mutable(Map.Entry<K, V> entry)
    {
        return new Mutable<>(entry.getKey(), entry.getValue());
    }

    static <T> Mutable<T, T> mutable(Iterator<T> iterator)
    {
        T key = iterator.next();
        T value = iterator.next();
        checkState(!iterator.hasNext());
        return mutable(key, value);
    }

    static <T> Mutable<T, T> mutable(Iterable<T> iterable)
    {
        return mutable(iterable.iterator());
    }
}
