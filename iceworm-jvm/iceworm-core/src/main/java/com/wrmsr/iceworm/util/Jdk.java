package com.wrmsr.iceworm.util;

import com.wrmsr.iceworm.util.lazy.SupplierLazyValue;

import java.lang.management.ManagementFactory;

public final class Jdk
{
    private Jdk()
    {
    }

    public static int parseSpecificationMajor(String spec)
    {
        String[] parts = spec.split("\\.");
        if (parts.length == 1) {
            return Integer.parseInt(spec);
        }
        else if (parts.length == 2 && parts[0].equals("1")) {
            return Integer.parseInt(parts[1]);
        }
        else {
            throw new IllegalArgumentException(spec);
        }
    }

    private static SupplierLazyValue<Integer> major = new SupplierLazyValue<>();

    public static int getMajor()
    {
        return major.get(() -> {
            String spec = System.getProperty("java.specification.version");
            return parseSpecificationMajor(spec);
        });
    }

    public static boolean isDebug()
    {
        return ManagementFactory.getRuntimeMXBean().getInputArguments().toString().indexOf("-agentlib:jdwp") > 0;
    }

    public static String getClasspath()
    {
        return System.getProperty("java.class.path");
    }
}
