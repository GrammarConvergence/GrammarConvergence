#!/usr/bin/python

import os, sys
import fnmatch
import subprocess
import filecmp

EXECUTABLE = os.path.join(os.getcwd(), 'run')

class TestHarness :
  def __init__(self) :
  	self.noPassed = 0
  	self.noFailed = 0
  	self.makeExecutable()

  @classmethod
  def makeExecutable(cls) :
    if not os.path.isfile(EXECUTABLE):
      retcode = subprocess.call('make',shell=True)
      assert retcode==0, '\tFAILED to make the parser'

  def testCode(self, retcode, testcase):
    if retcode > 0:
      print testcase, 'failed'
      self.noFailed += 1
    else:
      #print testcase, 'passed'
      self.noPassed += 1

  def testOneFile(self, root, filename) :
    testcase = os.path.join(root, filename)
    retcode = subprocess.call('%s < %s > /dev/null' % (EXECUTABLE, testcase), shell=True)
    self.testCode(retcode, testcase)

  def testDirectory(self, testDir):
    assert os.path.isdir(testDir), testDir + 'must be a directory'
    for root, dirs, files in os.walk( testDir ) :
      for filename in files :
        if filename.endswith('.py') :
          self.testOneFile(root, filename)

  def runTestCases(self, testPath):
    if os.path.isdir(testPath) :
    	self.testDirectory(testPath)
    elif os.path.isfile(testPath) :
    	self.testOneFile(os.getcwd(), testPath)

  def __str__(self) :
    return '\t%d test cases Passed\n\t%d test cases Failed' % (self.noPassed, self.noFailed)


if __name__ == '__main__':
  testcases = [ ]
  if len(sys.argv) <= 1 :
  	testcases = [os.path.join( os.getcwd(), '../testsuite-python-lib/Python-2.7.2')]
  else:
    testcases = sys.argv[1:]
  harness = TestHarness()
  for t in testcases :
  	harness.runTestCases(t)
  print harness

