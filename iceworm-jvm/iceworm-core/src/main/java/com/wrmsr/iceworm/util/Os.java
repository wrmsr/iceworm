package com.wrmsr.iceworm.util;

import com.wrmsr.iceworm.util.lazy.SupplierLazyValue;

public enum Os
{
    LINUX,
    MAC,
    WINDOWS,
    UNKNOWN,
    ;

    public static Os fromName(String name)
    {
        if (name.startsWith("Linux") || name.startsWith("LINUX")) {
            return Os.LINUX;
        }
        else if (name.startsWith("Mac")) {
            return Os.MAC;
        }
        else if (name.startsWith("Windows")) {
            return Os.WINDOWS;
        }
        else {
            return UNKNOWN;
        }
    }

    private static final SupplierLazyValue<Os> current = new SupplierLazyValue<>();

    public static Os get()
    {
        return current.get(() -> fromName(System.getProperty("os.name", "")));
    }
}
