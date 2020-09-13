package com.wrmsr.iceworm.util.classloaders;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.Iterables;
import com.google.common.collect.Iterators;

import java.io.IOException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;

import static com.google.common.base.Preconditions.checkNotNull;

public class ParentFirstClassLoader
        extends URLClassLoader
{
    private final List<String> hiddenClasses;
    private final List<String> parentFirstClasses;
    private final List<String> hiddenResources;
    private final List<String> parentFirstResources;

    public ParentFirstClassLoader(
            List<URL> urls,
            ClassLoader parent,
            Iterable<String> hiddenClasses,
            Iterable<String> parentFirstClasses)
    {
        this(urls,
                parent,
                hiddenClasses,
                parentFirstClasses,
                Iterables.transform(hiddenClasses, ParentFirstClassLoader::classNameToResource),
                Iterables.transform(parentFirstClasses, ParentFirstClassLoader::classNameToResource));
    }

    public ParentFirstClassLoader(
            List<URL> urls,
            ClassLoader parent,
            Iterable<String> hiddenClasses,
            Iterable<String> parentFirstClasses,
            Iterable<String> hiddenResources,
            Iterable<String> parentFirstResources)
    {
        super(urls.toArray(new URL[0]), checkNotNull(parent));
        this.hiddenClasses = ImmutableList.copyOf(hiddenClasses);
        this.parentFirstClasses = ImmutableList.copyOf(parentFirstClasses);
        this.hiddenResources = ImmutableList.copyOf(hiddenResources);
        this.parentFirstResources = ImmutableList.copyOf(parentFirstResources);
    }

    @Override
    protected Class<?> loadClass(String name, boolean resolve)
            throws ClassNotFoundException
    {
        synchronized (getClassLoadingLock(name)) {
            Class<?> cachedClass = findLoadedClass(name);
            if (cachedClass != null) {
                return resolveClass(cachedClass, resolve);
            }

            if (!isParentFirstClass(name)) {
                try {
                    Class<?> clazz = findClass(name);
                    return resolveClass(clazz, resolve);
                }
                catch (ClassNotFoundException ignored) {
                }
            }

            if (!isHiddenClass(name)) {
                try {
                    Class<?> clazz = getParent().loadClass(name);
                    return resolveClass(clazz, resolve);
                }
                catch (ClassNotFoundException ignored) {
                }
            }

            if (isParentFirstClass(name)) {
                Class<?> clazz = findClass(name);
                return resolveClass(clazz, resolve);
            }

            throw new ClassNotFoundException(name);
        }
    }

    private Class<?> resolveClass(Class<?> clazz, boolean resolve)
    {
        if (resolve) {
            resolveClass(clazz);
        }
        return clazz;
    }

    private boolean isParentFirstClass(String name)
    {
        for (String nonOverridableClass : parentFirstClasses) {
            if (name.startsWith(nonOverridableClass)) {
                return true;
            }
        }
        return false;
    }

    private boolean isHiddenClass(String name)
    {
        for (String hiddenClass : hiddenClasses) {
            if (name.startsWith(hiddenClass)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public URL getResource(String name)
    {
        if (!isParentFirstResource(name)) {
            URL url = findResource(name);
            if (url != null) {
                return url;
            }
        }

        if (!isHiddenResource(name)) {
            URL url = getParent().getResource(name);
            if (url != null) {
                return url;
            }
        }

        if (isParentFirstResource(name)) {
            URL url = findResource(name);
            if (url != null) {
                return url;
            }
        }

        return null;
    }

    @Override
    public Enumeration<URL> getResources(String name)
            throws IOException
    {
        List<Iterator<URL>> resources = new ArrayList<>();

        if (!isParentFirstResource(name)) {
            Iterator<URL> myResources = Iterators.forEnumeration(findResources(name));
            resources.add(myResources);
        }

        if (!isHiddenResource(name)) {
            Iterator<URL> parentResources = Iterators.forEnumeration(getParent().getResources(name));
            resources.add(parentResources);
        }

        if (isParentFirstResource(name)) {
            Iterator<URL> myResources = Iterators.forEnumeration(findResources(name));
            resources.add(myResources);
        }

        return Iterators.asEnumeration(Iterators.concat(resources.iterator()));
    }

    private boolean isParentFirstResource(String name)
    {
        for (String nonOverridableResource : parentFirstResources) {
            if (name.startsWith(nonOverridableResource)) {
                return true;
            }
        }
        return false;
    }

    private boolean isHiddenResource(String name)
    {
        for (String hiddenResource : hiddenResources) {
            if (name.startsWith(hiddenResource)) {
                return true;
            }
        }
        return false;
    }

    private static String classNameToResource(String className)
    {
        return className.replace('.', '/');
    }
}
