package com.wrmsr.iceworm.spark;

import com.eclipsesource.v8.V8;
import com.eclipsesource.v8.V8Object;
import org.junit.Test;

import javax.script.Bindings;
import javax.script.ScriptContext;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.SimpleScriptContext;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class JsTest
{
    public static final String DEFAULT_TEMP_DIR_PREFIX = "iceworm";

    public static Path createTempDirectory(Optional<String> prefix)
            throws IOException
    {
        Path dir = Files.createTempDirectory(prefix.orElse(DEFAULT_TEMP_DIR_PREFIX));
        dir.toFile().deleteOnExit();
        return dir;
    }

    public static Path createTempDirectory(String prefix)
            throws IOException
    {
        return createTempDirectory(Optional.of(prefix));
    }

    public static Path createTempDirectory()
            throws IOException
    {
        return createTempDirectory(Optional.empty());
    }

    /*
    <dependency>
        <groupId>org.graalvm.js</groupId>
        <artifactId>js</artifactId>
        <version>20.0.0</version>
    </dependency>
    <dependency>
        <groupId>org.graalvm.js</groupId>
        <artifactId>js-scriptengine</artifactId>
        <version>20.0.0</version>
    </dependency>

    new ScriptEngineManager().getEngineByName("JavaScript");

    Map object = (Map) engine.eval("Object");
    Function<Object[], Object> method = (Function<Object[], Object>) object.get("assign");
    */

    @Test
    public void testJs()
            throws Throwable
    {
        //https://docs.oracle.com/javase/8/docs/technotes/guides/scripting/prog_guide/api.html
        //https://docs.oracle.com/javase/8/docs/technotes/guides/scripting/prog_guide/javascript.html

        ScriptEngineManager engineManager = new ScriptEngineManager();
        ScriptEngine engine = engineManager.getEngineByName("nashorn");

        engine.eval("print('Hello World!');");
        engine.eval("function add2(v) { return v + 2; }");
        engine.eval("add2(2)");
        // engine.eval("f(x)", );

        engine.put("x", "hello");
        // print global variable "x"
        // engine.eval("println(x);");
        // the above line prints "hello"

        // Now, pass a different script context
        ScriptContext newContext = new SimpleScriptContext();
        Bindings engineScope = newContext.getBindings(ScriptContext.ENGINE_SCOPE);

        // add new variable "x" to the new engineScope
        engineScope.put("x", "world");

        // execute the same script - but this time pass a different script context
        // engine.eval("println(x);", newContext);
    }

    @Test
    public void testV8()
            throws Throwable
    {
        V8 v8 = V8.createV8Runtime();
        V8Object object = v8.executeObjectScript("foo = {key: 'bar'}");

        String stringScript = v8.executeStringScript("'f'");
        System.out.println("Hello from Java! " + stringScript);

        Object result = object.get("key");
        assertTrue(result instanceof String);
        assertEquals("bar", result);
        object.release();

        v8.release();
    }
}
