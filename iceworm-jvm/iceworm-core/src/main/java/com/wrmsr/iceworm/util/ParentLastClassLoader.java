package com.wrmsr.iceworm.util;

import java.net.URL;
import java.net.URLClassLoader;
import java.util.List;

public class ParentLastClassLoader
        extends ClassLoader
{
    private ChildURLClassLoader childClassLoader;

    public ChildURLClassLoader getChildClassLoader()
    {
        return childClassLoader;
    }

    private static class FindClassClassLoader
            extends ClassLoader
    {
        public FindClassClassLoader(ClassLoader parent)
        {
            super(parent);
        }

        @Override
        public Class<?> findClass(String name)
                throws ClassNotFoundException
        {
            return super.findClass(name);
        }
    }

    public static class ChildURLClassLoader
            extends URLClassLoader
    {
        private FindClassClassLoader realParent;

        public ChildURLClassLoader(URL[] urls, FindClassClassLoader realParent)
        {
            super(urls, null);

            this.realParent = realParent;
        }

        public FindClassClassLoader getRealParent()
        {
            return realParent;
        }

        @Override
        public Class<?> findClass(String name)
                throws ClassNotFoundException
        {
            try {
                return super.findClass(name);
            } catch (ClassNotFoundException e) {
                return realParent.loadClass(name);
            }
        }
    }

    public ParentLastClassLoader(List<URL> classpath)
    {
        super(Thread.currentThread().getContextClassLoader());

        URL[] urls = classpath.toArray(new URL[classpath.size()]);

        childClassLoader = new ChildURLClassLoader(urls, new FindClassClassLoader(this.getParent()));
    }

    @Override
    protected synchronized Class<?> loadClass(String name, boolean resolve)
            throws ClassNotFoundException
    {
        try {
            return childClassLoader.findClass(name);
        } catch (ClassNotFoundException e) {
            return super.loadClass(name, resolve);
        }
    }
}
