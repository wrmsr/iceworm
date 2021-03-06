package com.wrmsr.iceworm.util.collect;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Sets;
import com.wrmsr.iceworm.util.MoreCollectors;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static com.wrmsr.iceworm.util.MoreCollectors.toImmutableSet;
import static java.util.function.Function.identity;

public final class Toposort
{
    private Toposort()
    {
    }

    public static <T> List<Set<T>> toposort(Map<T, Set<T>> data)
    {
        data = data.entrySet().stream().collect(
                MoreCollectors.toHashMap(
                        Map.Entry::getKey,
                        e -> e.getValue().stream().filter(v -> !v.equals(e.getKey())).collect(MoreCollectors.toHashSet())));

        Set<T> extraItemsInDeps = Sets.difference(data.values().stream()
                .flatMap(Set::stream)
                .collect(Collectors.toSet()), data.keySet());
        data.putAll(extraItemsInDeps.stream().collect(Collectors.toMap(identity(), k -> new HashSet<>())));

        ImmutableList.Builder<Set<T>> ret = ImmutableList.builder();
        while (true) {
            Set<T> step = data.entrySet().stream()
                    .filter(e -> e.getValue().isEmpty())
                    .map(Map.Entry::getKey)
                    .collect(toImmutableSet());
            if (step.isEmpty()) {
                break;
            }
            ret.add(step);

            data = data.entrySet().stream()
                    .filter(e -> !step.contains(e.getKey()))
                    .collect(
                            MoreCollectors.toHashMap(
                                    Map.Entry::getKey,
                                    e -> e.getValue().stream()
                                            .filter(d -> !step.contains(d))
                                            .collect(MoreCollectors.toHashSet())));
        }

        if (!data.isEmpty()) {
            throw new CycleException(data);
        }

        return ret.build();
    }

    @SuppressWarnings({"rawtypes"})
    public static final class CycleException
            extends RuntimeException
    {
        private static final long serialVersionUID = -4180455364328557214L;

        private final Map data;

        public CycleException(Map data)
        {
            this.data = data;
        }

        @Override
        public String toString()
        {
            return "CycleException{" +
                    "data=" + data +
                    '}';
        }

        public Map getData()
        {
            return data;
        }
    }
}
