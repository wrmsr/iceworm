package com.wrmsr.iceworm.util;

import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Supplier;

public interface Cell<T>
{
    /*
    TODO:
     - actual optional
     - synchronized
    */

    T get();

    void set(T value);

    boolean isSet();

    default Supplier<T> toSupplier()
    {
        return this::get;
    }

    default Consumer<T> toConsumer()
    {
        return this::set;
    }

    default Optional<T> getOptional()
    {
        return isSet() ? Optional.of(get()) : Optional.empty();
    }

    final class DefaultImpl<T>
            implements Cell<T>
    {
        private T value;

        public DefaultImpl(T value)
        {
            this.value = value;
        }

        @Override
        public final T get()
        {
            return value;
        }

        @Override
        public final void set(T value)
        {
            this.value = value;
        }

        @Override
        public boolean isSet()
        {
            return true;
        }

        @Override
        public String toString()
        {
            return getClass().getSimpleName() + "{value=" + value + '}';
        }
    }

    static <T> Cell<T> of(T value)
    {
        return new DefaultImpl<>(value);
    }

    final class OptionalImpl<T>
            implements Cell<T>
    {
        private boolean isSet;
        private T value;

        @Override
        public T get()
        {
            if (!isSet) {
                throw new IllegalStateException();
            }
            return value;
        }

        @Override
        public void set(T value)
        {
            isSet = true;
            this.value = value;
        }

        @Override
        public boolean isSet()
        {
            return isSet;
        }
    }

    static <T> Cell<T> optional()
    {
        return new OptionalImpl<>();
    }

    final class SetOnceImpl<T>
            implements Cell<T>
    {
        private boolean isSet;
        private T value;

        @Override
        public T get()
        {
            if (!isSet) {
                throw new IllegalStateException();
            }
            return value;
        }

        @Override
        public void set(T value)
        {
            if (isSet) {
                throw new IllegalStateException();
            }
            isSet = true;
            this.value = value;
        }

        @Override
        public boolean isSet()
        {
            return isSet;
        }
    }

    static <T> Cell<T> setOnce()
    {
        return new SetOnceImpl<>();
    }
}
