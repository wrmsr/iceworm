import os


def test_jpype():
    os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_261.jdk/Contents/Home'
    import jpype
    jpype.startJVM(classpath=['lib/*', 'classes'], convertStrings=False)
    try:
        from jpype import java
        print(java.lang.System.getProperty('java.vendor'))
    finally:
        jpype.shutdownJVM()
