package com.wrmsr.iceworm.spark;

import com.google.protobuf.util.JsonFormat;
import com.wrmsr.iceworm.Iceworm;
import org.junit.Test;

public class ProtoTest
{
    @Test
    public void testProto()
            throws Throwable
    {
        Iceworm._Stub stub = Iceworm._Stub.newBuilder()
                .setData("hi")
                .build();
        System.out.println(stub);

        String json = JsonFormat.printer().print(stub);
        System.out.println(json);

        Iceworm._Stub.Builder bld = Iceworm._Stub.newBuilder();
        JsonFormat.parser().ignoringUnknownFields().merge(json, bld);

        Iceworm._Stub stub2 = bld.build();
        System.out.println(stub2);
    }
}
