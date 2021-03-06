package com.wrmsr.iceworm.dist;

import com.google.common.base.Charsets;
import com.google.common.collect.ImmutableList;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkState;
import static com.wrmsr.iceworm.util.MoreSystem.runSubprocessLines;

public class WriteGitRevision
{
    public static String readGitRev(Path git)
            throws IOException, InterruptedException
    {
        String head = new String(Files.readAllBytes(Paths.get(git.toString(), "HEAD")), Charsets.UTF_8).trim();
        String rev;
        if (head.startsWith("ref: ")) {
            String ref = head.substring(5);
            rev = new String(Files.readAllBytes(Paths.get(git.toString(), ref)), Charsets.UTF_8).trim();
        }
        else {
            rev = head;
        }
        return rev + "-injected";
    }

    public static String runGitRev()
            throws IOException, InterruptedException
    {
        List<String> lines = runSubprocessLines(
                ImmutableList.of(
                        "git",
                        "describe",
                        "--match=NeVeRmAtCh",
                        "--always",
                        "--abbrev=40",
                        "--dirty"
                ),
                3000,
                true);
        if (lines.size() < 1) {
            throw new IllegalStateException();
        }
        String rev = lines.get(0).trim();
        if (!rev.matches("[0-9a-fA-f]{40}(-dirty)?")) {
            throw new IllegalStateException(rev);
        }
        return rev;
    }

    public static void main(String[] args)
            throws Throwable
    {
        boolean write;
        if (args.length == 1) {
            checkArgument(args[0].equals("write"));
            write = true;
        }
        else {
            checkArgument(args.length == 0);
            write = false;
        }

        Path cwd = Paths.get(System.getProperty("user.dir"));
        checkState(cwd.getFileName().toString().equals("iceworm-core"));

        String parentName = cwd.getParent().getFileName().toString();
        checkState(parentName.equalsIgnoreCase("iceworm-jvm") || parentName.equalsIgnoreCase("build"));
        Path git = Paths.get(cwd.getParent().toString(), ".git");
        if (!git.toFile().exists()) {
            return;
        }

        String rev;
        if (Paths.get(git.toString(), "index").toFile().exists()) {
            rev = runGitRev();
        }
        else {
            rev = readGitRev(git);
        }

        if (write) {
            checkState(Paths.get(cwd.toString(), "target").toFile().exists());
            Files.write(
                    Paths.get(cwd.toString(), "target", "classes", "com", "wrmsr", "iceworm", "dist", ".revision"),
                    rev.getBytes(Charsets.UTF_8));
        }
        else {
            System.out.println(rev);
        }
    }
}
