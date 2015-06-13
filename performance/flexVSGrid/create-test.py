#!/usr/bin/python

import getopt, sys

def main():

    limit = int(sys.argv[1])
    className = sys.argv[2]
    start = 100
    increment = 100
    fileNamePrefix = 'test-%s' % className
    testSuite = 'standalone'
    typeOfTest = 'HTML'

    opts, args = getopt.getopt(sys.argv[3:],"h:s:i:p:u:t:", ["help","start=","inc=",
                                                             "prefix=","suite=","type"])
    for o, a in opts:
        if o in ("-s", "--start"):
            start = int(a)
        if o in ("-i", "--inc"):
            increment = int(a)
        if o in ("-u", "--suit"):
            testSuite = str(a)
        if o in ("-st", "--type"):
            typeOfTest = str(a)
        if o in ("-p", "--prefix"):
            fileNamePrefix = str(a)

    if (10000 < limit or limit < 0) or \
       (className and className not in ('grid', 'flex')) or \
       (testSuite and testSuite not in ('standalone', 'chrome', 'webkit')) or \
       (typeOfTest and typeOfTest not in ('HTML', 'JS')) or \
       (start < 0 or start > limit) or (increment < 0 or increment > 500):
        usage()

    createTestFiles(fileNamePrefix, className, limit, testSuite, typeOfTest, start, increment)


def createTestFiles(fileNamePrefix, className, limit, testSuite, typeOfTest, start, increment):

    for i in range (start, limit+1, increment):

        f = open(fileNamePrefix + '-%04d.html' % i, 'w')
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('    <head>\n')
        f.write('        <title>Comparison of layout performance between Flexbox and Grid layout</title>\n')
        f.write('        <link rel="stylesheet" href="resources/create-flex-VS-grid-tests.css" TYPE="text/css"></link>\n')
        if testSuite in ('chrome', 'webkit'):
            f.write('        <script src="../../resources/runner.js"></script>')
        if typeOfTest is 'JS':
            f.write('        <script src=\"resources/create-flex-VS-grid-tests.js\"></script>\n')
        f.write('    </head>\n')
        f.write('    <body>\n')
        if typeOfTest is 'HTML':
            staticHTMLBody(f, className, i)
            if testSuite in ('chrome', 'webkit'):
                performanceTestSuiteScript(f)
        elif typeOfTest in ('chrome', 'webkit'):
            preformanceSuiteJSBody(f, className, i)
        else:
            standaloneJSBody(f, className, i)
        f.write('    </body>\n')
        f.write('</html>\n')


def staticHTMLBody(f, className, numberOfElements):

    for i in range(0, numberOfElements):
        f.write('        <div class="%s">\n' % className)
        f.write('            <div class="i1">Item 1</div>\n')
        f.write('            <div class="i2">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</div>\n')
        f.write('            <div class="i3">Item 3 longer</div>\n')
        f.write('        </div>\n')


def standaloneJSBody(f, className, numberOfElements):

    f.write('        <script>\n')
    f.write('            window.testFunction = createFlexVSGridTestFunction(%d, "%s");</script>\n' % (numberOfElements, className))
    f.write('            testFunction();')
    f.write('        </script>\n')


def preformanceSuiteJSBody(f, className, numberOfElements):

    f.write('        <script>\n')
    f.write('            PerfTestRunner.measureTime({\n')
    f.write('                description: "Measure layout performance of 200 grid blocks.",\n')
    f.write('                run: createFlexVSGridTestFunction(%d, "%s")\n' % (numberOfElements, className))
    f.write('            });\n')
    f.write('        </script>\n')


def preformanceSuiteScript(f, className, numberOfElements):

    f.write('        <script>\n')
    f.write('            var index = 0;\n')
    f.write('            PerfTestRunner.measureTime({\n')
    f.write('                description: "Measure layout performance of 200 grid blocks.",\n')
    f.write('                run: function() {\n')
    f.write('                    document.body.style.width = ++index % 2 ? "99%" : "98%";\n')
    f.write('                    PerfTestRunner.forceLayoutOrFullFrame();\n')
    f.write('                }\n')
    f.write('            });\n')
    f.write('        </script>\n')


def usage():

    print 'Usage: limit className [options]'
    print '    limit: Number of elements. Positive integer (max 9999). '
    print '    className: either "grid" or "flex".'
    print '    --start=, -s : Initial number of elements when creating a range of tests. Positive integer (max limit).'
    print '    --inc=, -i : Increment of elements when creating a range of tests. Positive integer (max 500).'
    print '    --prefix=, -p : prefix for the test file name. A "-%04d.html" sufix will be added. Default is "test-%s", where %s will be filled with "className").'
    print '    --suite=, -u : test suite indicator. Available options are "chrome", "webkit" or "standalone" (default).'
    print '    --type=, -t: type of generated HTML body test. Available options are "HTML" or "JS" (default).'
    sys.exit(2)


if __name__ == "__main__":
    main()
