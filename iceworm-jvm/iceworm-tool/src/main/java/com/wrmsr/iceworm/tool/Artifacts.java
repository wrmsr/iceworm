package com.wrmsr.iceworm.tool;

import com.google.common.base.Strings;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableSet;
import com.wrmsr.iceworm.util.Logger;
import io.airlift.resolver.ArtifactResolver;
import org.sonatype.aether.artifact.Artifact;
import org.sonatype.aether.artifact.ArtifactType;
import org.sonatype.aether.util.artifact.DefaultArtifact;

import java.io.File;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.stream.Collectors;

import static com.google.common.base.Preconditions.checkState;
import static com.google.common.collect.ImmutableList.toImmutableList;
import static com.google.common.collect.Lists.newArrayList;
import static com.google.common.collect.Sets.newHashSet;
import static java.util.Comparator.comparing;

public class Artifacts
{
    private static final Logger log = Logger.get(Artifacts.class);

    private Artifacts()
    {
    }

    public static void main(String[] args)
            throws Throwable
    {
        new Artifacts().run(args);
    }

    public void run(String[] args)
            throws Throwable
    {
        for (String logName : new String[] {"com.ning.http.client.providers.netty.NettyAsyncHttpProvider"}) {
            java.util.logging.Logger.getLogger(logName).setLevel(Level.WARNING);
        }

        // FIXME: META-INF/MANIFEST.MF Class-Path
        // https://docs.oracle.com/javase/8/docs/technotes/guides/jar/jar.html
        String m2Home = System.getenv("M2_HOME");
        if (Strings.isNullOrEmpty(m2Home)) {
            m2Home = new File(new File(System.getProperty("user.home")), ".m2").getAbsolutePath();
        }
        File repository = new File(new File(m2Home), "repository");
        File cwd = new File(System.getProperty("user.dir"));
        // File cwd = new File(System.getenv("PWD"));

        ArtifactResolver resolver = new ArtifactResolver(
                ArtifactResolver.USER_LOCAL_REPO,
                ImmutableList.of(ArtifactResolver.MAVEN_CENTRAL_URI));

        List<String> names = ImmutableList.of(
                "iceworm-core",
                "iceworm-spark",
                "iceworm-tool"
        );
        Set<String> localGroups = ImmutableSet.of(
                "com.wrmsr.iceworm"
        );

        Set<String> uncachedRepoPaths = newHashSet();
        for (String name : names) {
            log.info(name);

            String pom = name + "/pom.xml";

            File pomFile = new File(cwd, pom);
            List<Artifact> artifacts = resolver.resolvePom(pomFile);
            Map<Boolean, List<Artifact>> p = artifacts.stream().collect(Collectors.partitioningBy(a -> "org.slf4j".equals(a.getGroupId())));
            artifacts = newArrayList(p.getOrDefault(false, ImmutableList.of()));
            if (p.containsKey(true)) {
                List<Artifact> as = p.get(true);
                if (!as.isEmpty()) {
                    String v = as.stream().collect(Collectors.maxBy(comparing(Artifact::getVersion))).get().getVersion();
                    artifacts.addAll(resolver.resolveArtifacts(as.stream().map(
                            a -> new DefaultArtifact(
                                    a.getGroupId(),
                                    a.getArtifactId(),
                                    a.getClassifier(),
                                    a.getExtension(),
                                    v,
                                    a.getProperties(),
                                    (ArtifactType) null)
                    ).collect(toImmutableList())));
                }
            }

            List<File> files = newArrayList();
            for (Artifact a : artifacts) {
                if (localGroups.contains(a.getGroupId()) && new File(cwd, a.getArtifactId()).exists()) {
                    File localPath = new File(cwd, a.getArtifactId());
                    File file;
                    String rel;
                    if (a.getArtifactId().equals(name)) {
                        String jarFileName = a.getArtifactId() + "-" + a.getVersion() + ".jar";
                        file = new File(pomFile.getParentFile(), "target/" + jarFileName);
                        rel = a.getGroupId().replace(".", "/") + "/" + jarFileName;
                    }
                    else {
                        file = a.getFile();
                        rel = repository.toURI().relativize(file.toURI()).getPath();
                    }
                    checkState(file.exists());
                    // File localFile = new File(localPath, "target/" + file.getName());
                    // checkState(!rel.startsWith("/") && !rel.startsWith(".."));
                    log.info(file.toString());
                }
                else {
                    files.add(a.getFile());
                    log.info(a.getFile().toString());
                }
            }
        }
    }
}
