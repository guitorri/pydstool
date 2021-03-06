#/usr/bin/env python

# Matthieu Brucher
# Last Change : 2007-08-22 14:01

from __future__ import absolute_import

import unittest
import numpy

from numpy.testing import assert_equal, assert_almost_equal
from PyDSTool.Toolbox.optimizers.line_search import GoldenSectionSearch


class Function(object):
  def __call__(self, x):
    return (x[0] - 2) ** 2 + (2 * x[1] + 4) ** 2

  def gradient(self, x):
    return numpy.array((2 * (x[0] - 2), 2 * (2 * x[1] + 4)))

class test_GoldenSectionSearch(unittest.TestCase):
  def test_create(self):
    lineSearch = GoldenSectionSearch(min_alpha_step = 0.0001)
    assert_equal(lineSearch.stepSize, 1.)

  def test_call(self):
    lineSearch = GoldenSectionSearch(min_alpha_step = 0.0001)
    state = {'direction' : numpy.ones((2))}
    function = Function()
    assert_almost_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.ones((2)) * 0.0001, decimal = 4)
    assert(state['alpha_step'] < 0.0001)

  def test_call_gradient_direction(self):
    lineSearch = GoldenSectionSearch(min_alpha_step = 0.0001)
    state = {'direction' : numpy.array((4, -8))}
    function = Function()
    assert_almost_equal(lineSearch(origin = numpy.zeros((2)), state = state, function = function), numpy.array((1.0588, -2.1176)), decimal = 4)
    assert_almost_equal(state['alpha_step'], 1.0588/4, decimal = 4)

if __name__ == "__main__":
  unittest.main()
