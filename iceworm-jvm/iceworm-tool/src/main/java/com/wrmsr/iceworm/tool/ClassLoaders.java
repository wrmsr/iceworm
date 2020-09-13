package com.wrmsr.iceworm.tool;

import com.google.common.base.Joiner;
import com.google.common.base.Splitter;
import com.google.common.collect.ImmutableList;
import com.wrmsr.iceworm.util.Jdk;
import com.wrmsr.iceworm.util.Pair;
import com.wrmsr.iceworm.util.classloaders.ParentFirstClassLoader;
import io.airlift.resolver.ArtifactResolver;
import io.airlift.resolver.DefaultArtifact;
import org.sonatype.aether.artifact.Artifact;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.List;

import static com.wrmsr.iceworm.util.MoreCollectors.toImmutableList;
import static com.wrmsr.iceworm.util.MorePreconditions.checkSingle;

public class ClassLoaders
{
    public static List<Node> evaluateXPath(Document document, String xpathExpression)
    {
        XPathFactory xpathFactory = XPathFactory.newInstance();
        XPath xpath = xpathFactory.newXPath();
        List<Node> values = new ArrayList<>();
        try {
            XPathExpression expr = xpath.compile(xpathExpression);
            NodeList nodes = (NodeList) expr.evaluate(document, XPathConstants.NODESET);
            for (int i = 0; i < nodes.getLength(); i++) {
                values.add(nodes.item(i));
            }
        }
        catch (XPathExpressionException e) {
            throw new RuntimeException(e);
        }
        return values;
    }

    public static List<String> readPomDepCoords(File pomFile, Iterable<Pair<String, String>> groupArtifactPrefixPairs)
            throws IOException, ParserConfigurationException, SAXException
    {
        DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
        Document doc = dBuilder.parse(pomFile);

        //http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
        doc.getDocumentElement().normalize();

        List<String> coords = new ArrayList<>();

        for (Pair<String, String> pair : groupArtifactPrefixPairs) {
            String groupId = pair.first();
            String artifactPrefix = pair.second();

            Node node = checkSingle(evaluateXPath(doc,
                    "/project/dependencyManagement/dependencies/dependency" +
                            "[groupId='" + groupId + "' and starts-with(artifactId, '" + artifactPrefix + "')]"));

            String artifactId = null;
            String version = null;
            for (int i = 0; i < node.getChildNodes().getLength(); ++i) {
                Node child = node.getChildNodes().item(i);
                if (child.getNodeName().equals("artifactId")) {
                    artifactId = child.getTextContent();
                }
                else if (child.getNodeName().equals("version")) {
                    version = child.getTextContent();
                }
            }

            String coord = Joiner.on(":").join(groupId, artifactId, version);
            coords.add(coord);
        }

        return coords;
    }

    public static URL getFileUrl(File file)
    {
        try {
            return file.toURI().toURL();
        }
        catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) throws Throwable
    {
        ArtifactResolver resolver = new ArtifactResolver(
                ArtifactResolver.USER_LOCAL_REPO,
                ImmutableList.of(ArtifactResolver.MAVEN_CENTRAL_URI));

        File pomFile = new File("pom.xml");

        List<String> coords = readPomDepCoords(pomFile, ImmutableList.of(
                Pair.immutable("org.apache.parquet", "parquet-tools"))
        );

        List<Artifact> artifacts = resolver.resolveArtifacts(coords.stream().map(DefaultArtifact::new).collect(toImmutableList()));

        List<URL> cp = artifacts.stream()
                .map(Artifact::getFile)
                .map(ClassLoaders::getFileUrl)
                .collect(toImmutableList());

        System.out.println(cp);

        List<URL> classpath = ImmutableList.copyOf(Splitter.on(":").split(Jdk.getClasspath())).stream()
                .map(File::new)
                .map(ClassLoaders::getFileUrl)
                .collect(toImmutableList());

        ClassLoader cl = new ParentFirstClassLoader(
                cp,
                new URLClassLoader(
                        classpath.toArray(new URL[]{}),
                        ClassLoader.getSystemClassLoader().getParent()),
                ImmutableList.of(),
                ImmutableList.of(
                        "org.apache"
                ));

        Class<?> tc = cl.loadClass("com.wrmsr.iceworm.tool.ParquetThing");
        Thread.currentThread().setContextClassLoader(cl);
        tc.getDeclaredMethod("main", String[].class).invoke(null, new Object[]{new String[]{
                "barf",
        }});
    }
}
