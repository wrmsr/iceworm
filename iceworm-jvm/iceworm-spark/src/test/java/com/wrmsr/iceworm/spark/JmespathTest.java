package com.wrmsr.iceworm.spark;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import io.burt.jmespath.Expression;
import io.burt.jmespath.JmesPath;
import io.burt.jmespath.jcf.JcfRuntime;
import org.junit.Test;

public class JmespathTest
{
    @Test
    public void testJmespath() throws Throwable
    {
        JmesPath<Object> jmespath = new JcfRuntime();
        Expression<Object> expression = jmespath.compile("foo.bar.baz[2]");
        Object input = ImmutableMap.of(
                "foo", ImmutableMap.of(
                        "bar", ImmutableMap.of(
                                "baz", ImmutableList.of(
                                        0,
                                        1,
                                        2,
                                        3,
                                        4))));
        System.out.println(expression.search(input));
    }
}
