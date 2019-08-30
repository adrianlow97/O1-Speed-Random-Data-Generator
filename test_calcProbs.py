import pytest
import calcProbs

def test_calcProbs():
    testVals = {'A' : 300, 'B' : 20 , 'C' : 973}
    testVals = calcProbs.calcProbs(testVals)

    expected = {'A' : (300/1293) , 'B' : (20/1293) , 'C' : (973/1293)}
    print(testVals)
    assert testVals == expected
