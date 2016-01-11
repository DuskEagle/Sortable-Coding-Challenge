import sys
import unittest

sys.path.append('../src')

from Normalizer import *

class NormalizerTest(unittest.TestCase):
    
    def testManufacturerNormalizer(self):
        exemplar = manufacturerNormalizer("Canon")
        self.assertEqual(manufacturerNormalizer("Canon Canada"), exemplar)
        self.assertEqual(manufacturerNormalizer("canon"), exemplar)
        self.assertEqual(manufacturerNormalizer("Canon-UK"), exemplar)
    
    def testDontOverNormalize(self):
        self.assertNotEqual(manufacturerNormalizer("Canon"), manufacturerNormalizer("Scanonical Big Company Name"))
    
    def testHewlettPackard(self):
        exemplar = manufacturerNormalizer("HP")
        self.assertEqual(manufacturerNormalizer("hp"), exemplar)
        self.assertEqual(manufacturerNormalizer("Hewlett Packard"), exemplar)
        self.assertEqual(manufacturerNormalizer("Hewlett-Packard"), exemplar)
    
    def testGenericNormalizer(self):
        exemplar = genericNormalizer("MoDeL")
        self.assertIn(exemplar, genericNormalizer("This is my camera model."))
        
    
    
