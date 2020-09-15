"""
TODO:
 - jdk find from omm spark
"""
import os.path

import pytest


JAVA_HOME = '/Library/Java/JavaVirtualMachines/jdk1.8.0_261.jdk/Contents/Home'


def test_jpype():
    os.environ['JAVA_HOME'] = JAVA_HOME
    import jpype
    jpype.startJVM(classpath=['lib/*'], convertStrings=False)
    try:
        from jpype import java
        print(java.lang.System.getProperty('java.vendor'))
    finally:
        jpype.shutdownJVM()


@pytest.mark.xfail
def test_jpype_tool():
    os.environ['JAVA_HOME'] = JAVA_HOME
    import jpype
    jpype.startJVM(
        classpath=[
            'lib/*',
            os.path.join(
                os.path.dirname(__file__),
                '../../iceworm-jvm/iceworm-tool/target/iceworm-tool-0.1-SNAPSHOT.jar',
            ),
        ],
        convertStrings=False,
    )
    try:
        ccls = jpype.JClass('java.lang.Class').forName('com.wrmsr.iceworm.tool.ClassLoaders')
        print(ccls)
        cls = jpype.JClass(ccls)
        print(cls)
        cls.main([])
    finally:
        jpype.shutdownJVM()
