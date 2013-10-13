import unittest
from lxml import etree
import os
import textwrap

import mock
from random import Random
from .response_xml_factory import StringResponseXMLFactory, CustomResponseXMLFactory
from . import test_system, new_loncapa_problem

import ipdb

class CapaShuffleTest(unittest.TestCase):

    def setUp(self):
        super(CapaShuffleTest, self).setUp()
        self.system = test_system()

    def test_with_solution(self):
        xml_str = textwrap.dedent("""
            <problem>
            <multiplechoiceresponse>
              <choicegroup type="MultipleChoice" shuffle="true">
                <choice correct="false" fixed="true">A</choice>
                <choice correct="false" fixed="true">B</choice>
                <choice correct="true" fixed="true">C</choice>
              </choicegroup>
            </multiplechoiceresponse>
            
            <solution>
            <div class="detailed-solution">
            <p>Explanation</p>

            <p>The release of the iPod allowed consumers to carry their entire music library with them in a </p>
            <p>format that did not rely on fragile and energy-intensive spinning disks.</p>

            </div>
            </solution>
            </problem>
        """)
        problem = new_loncapa_problem(xml_str)
        the_html = problem.get_html()
        self.assertRegexpMatches(the_html, r"<div>.*\[.*'A'.*'B'.*'C'.*\].*</div>.*")

    def test_with_multiple_solutions(self):
        xml_str = textwrap.dedent("""
            <problem gradiance="true">
                <p>What is the correct answer?</p>
                <multiplechoiceresponse>
                  <choicegroup type="MultipleChoice">
                    <choice correct="false">wrong-1</choice>
                    <choice correct="false">wrong-2</choice>
                    <choice correct="true" solutionid="solution1">correct-1</choice>
                    <choice correct="false">wrong-3</choice>
                    <choice correct="false">wrong-4</choice>
                    <choice correct="true" solutionid="solution2">correct-2</choice>
                  </choicegroup>
                </multiplechoiceresponse>

                <solution>
                <div class="detailed-solution" solutionid='solution1'>
                    <p>Explanation</p>

                    <p>This is the 1st solution</p>
                    <p>Not much to explain here, sorry!</p>
                </div>

                <div class="detailed-solution" solutionid="solution2">
                    <p>Explanation</p>

                    <p>This is the 2nd solution</p>
                </div>
                </solution>
            </problem>
        """)
        problem = new_loncapa_problem(xml_str)
        rnd = Random()
        ix = rnd.randint(0, 20)
        problem.seed = ix
        the_html = problem.get_html()

        print the_html
        self.assertEqual(1, 2)
        # self.assertRegexpMatches(the_html, r"<div>.*\[.*'A'.*'B'.*'C'.*\].*</div>.*")
