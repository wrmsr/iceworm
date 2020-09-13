package com.wrmsr.iceworm.util;

import static com.google.common.base.Preconditions.checkArgument;

public final class MoreBytes
{
    private MoreBytes()
    {
    }

    public static String toHex(byte[] bytes)
    {
        StringBuilder sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    public static byte[] fromHex(String string)
    {
        checkArgument(string.length() % 2 == 0);
        byte[] bytes = new byte[string.length() / 2];
        for (int i = 0; i < bytes.length; ++i) {
            bytes[i] = Byte.parseByte(string.substring(i * 2, (i + 1) * 2));
        }
        return bytes;
    }
}
