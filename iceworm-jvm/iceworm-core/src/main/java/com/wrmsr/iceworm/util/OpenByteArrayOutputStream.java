package com.wrmsr.iceworm.util;

import java.io.ByteArrayOutputStream;

public final class OpenByteArrayOutputStream
        extends ByteArrayOutputStream
{
    public OpenByteArrayOutputStream()
    {
    }

    public OpenByteArrayOutputStream(int size)
    {
        super(size);
    }

    public byte[] getBuf()
    {
        return buf;
    }
}
