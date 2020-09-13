package com.wrmsr.iceworm.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.OptionalLong;
import java.util.concurrent.TimeUnit;

public final class MoreSystem
{
    private MoreSystem()
    {
    }

    public static OptionalLong getPid()
    {
        try {
            Class<?> cls = Class.forName("java.lang.ProcessHandle");
            Object current = cls.getDeclaredMethod("current").invoke(null);
            long pid = (long) cls.getDeclaredMethod("pid").invoke(current);
            return OptionalLong.of(pid);
        }
        catch (ReflectiveOperationException e) {
            return OptionalLong.empty();
        }
    }

    public static String shellEscape(String s)
    {
        return "'" + s.replace("'", "'\"'\"'") + "'";
    }

    public static List<String> runSubprocessLines(List<String> command, long timeoutMillis, boolean inheritStderr)
            throws IOException, InterruptedException
    {
        ProcessBuilder pb = new ProcessBuilder().command(command);
        if (inheritStderr) {
            pb.redirectError(ProcessBuilder.Redirect.INHERIT);
        }

        Process process = pb.start();
        process.getOutputStream().close();

        List<String> lines = new ArrayList<>();
        Thread thread = new Thread(() -> {
            BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            try {
                while (!Thread.currentThread().isInterrupted() && (line = br.readLine()) != null) {
                    lines.add(line);
                }
            }
            catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
        thread.setDaemon(true);
        thread.start();

        process.waitFor(timeoutMillis, TimeUnit.MILLISECONDS);
        if (process.exitValue() != 0) {
            throw new IllegalStateException(Integer.toString(process.exitValue()));
        }

        thread.interrupt();
        thread.join(timeoutMillis);

        return lines;
    }
}
