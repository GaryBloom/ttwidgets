"""
test_ttwidgets
==============

This runs a quick test of the expected output formatting from the module
to make sure it is installed and running.
"""

"""
Copyright 2020 Gary Michael Bloom

               mailto:bloominator@hotmail.com
               mailto:GaryBloomLaw@gmail.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import tkinter as tk
import unittest
import ttwidgets


class Test_PyVers(unittest.TestCase):

    def test_pyvers(self):
        self.assertTrue(ttwidgets.PyVers_f >= 3.1,
                        "Unsupported Python Version %s" % ttwidgets.PyVers_s)


class Test_fromDicts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_tag_attrs_fromDicts1(self):
        o_d = dict(family="Courier New", background='white', fg='blue', bd='2',
                   relief=tk.SOLID, funderline=1, foverstrike=0, underline=10)
        gen_text = ttwidgets.gen_tag_attrs(None, o_d, kmode='')
        # abbrev=False) # , debug=True)
        expected_text = 'family="Courier New" background=white fg=blue bd=2' \
                        ' relief=solid funderline=1 foverstrike=0 underline=10'
        if ttwidgets.PyVers_f < 3.6:  # False: # True: #
            gen_text = sorted(ttwidgets.split_attrs(gen_text))
            expected_text = sorted(ttwidgets.split_attrs(expected_text))
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromDicts2(self):
        o_d = dict(family='Courier New', background='white', fg='blue', bd='2',
                   relief=tk.SOLID, funderline=1, foverstrike=0, underline=10)
        gen_text = ttwidgets.gen_tag_attrs(options=o_d, kmode='alias')
        # abbrev=True) # , debug=True)
        expected_text = 'fam="Courier New" bg=white fg=blue bd=2 rel=solid ' \
                        'u=1 o=0 ul=10'
        if ttwidgets.PyVers_f < 3.6:  # False: # True: #
            gen_text = sorted(ttwidgets.split_attrs(gen_text))
            expected_text = sorted(ttwidgets.split_attrs(expected_text))
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromDicts3(self):
        o_d = dict(family='Courier New', background='white', fg='blue', bd='2',
                   relief=tk.SOLID, funderline=1, foverstrike=0, underline=10)
        gen_text = ttwidgets.gen_tag_attrs(None, o_d, kmode='option')
        # abbrev=True) # , debug=True)
        expected_text = 'family="Courier New" background=white foreground=' \
                        'blue borderwidth=2 relief=solid funderline=1 ' \
                        'foverstrike=0 underline=10'
        if ttwidgets.PyVers_f < 3.6:  # False: # True: #
            gen_text = sorted(ttwidgets.split_attrs(gen_text))
            expected_text = sorted(ttwidgets.split_attrs(expected_text))
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromDicts4(self):
        o_d = dict(background='white', fg='blue', bd='2', relief=tk.SOLID,
                   underline=10)
        f_d = dict(family='Courier New', underline=1, overstrike=0, )
        gen_text = ttwidgets.gen_tag_attrs(None, o_d, f_d,
                                           kmode='option')
        # abbrev=True) # , debug=True)
        expected_text = 'background=white foreground=blue borderwidth=2 ' \
                        'relief=solid family="Courier New" funderline=1 ' \
                        'foverstrike=0 underline=10'
        if True:  # ttwidgets.PyVers_f < 3.6: # False: #
            gen_text = sorted(ttwidgets.split_attrs(gen_text))
            expected_text = sorted(ttwidgets.split_attrs(expected_text))
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromDicts5(self):
        o_d = dict(background='white', foreground='blue', borderwidth='2',
                   relief=tk.SOLID, underline=10)
        f_d = dict(family='Courier New', underline=1, overstrike=0, )
        case = 'title'
        gen_text = ttwidgets.gen_tag_attrs(None, o_d, f_d, case,
                                           kmode='option')
        #                                  abbrev=True) # , debug=True)
        expected_text = 'background=white foreground=blue borderwidth=2 ' \
                        'relief=solid family="Courier New" funderline=1 ' \
                        'foverstrike=0 ' \
                        'underline=10 case=title'
        o_exp_d, f_exp_d, case_exp = ttwidgets.parse_tag_attrs(expected_text)
        if True:  # ttwidgets.PyVers_f < 3.6: # False: #
            gen_text = sorted(ttwidgets.split_attrs(gen_text))
            expected_text = sorted(ttwidgets.split_attrs(expected_text))
        self.assertEqual(gen_text, expected_text)
        self.assertEqual(o_d, o_exp_d)
        self.assertEqual(f_d, f_exp_d)
        self.assertEqual(case, case_exp)


class Test_fromWidget(unittest.TestCase):

    def test_get_tag_attrs_fromWidget1(self):
        but = ttwidgets.Button(bg='wheat',
                               text='<tag fg=red>red</tag> and <tag'
                               ' background=blue>blue</tag>')
        gen_text = but.gen_tag_attrs(kmode='', extend=True)
        # abbrev=True) # , debug=True)
        expected_text = ['background=wheat text="<tag fg=red>red</tag> and '
                         '<tag background=blue>blue</tag>"',
                         'foreground=red text=red',
                         'text=" and "',
                         'background=blue text=blue']
        if ttwidgets.PyVers_f < 3.6:  # False: # True: # False: #
            gen_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in gen_text]
            expected_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in expected_text]
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromWidget2(self):
        # toplevel = tk.Tk()
        but = ttwidgets.Button(bg='wheat',
                               text='<tag fg=red>red</tag> and '
                               '<tag background=blue>blue</tag>')
        gen_text = but.gen_tag_attrs(kmode='alias', extend=True)
        # abbrev=True) # , debug=True)
        expected_text = ['bg=wheat txt="<tag fg=red>red</tag> and <tag'
                         ' background=blue>blue</tag>"',
                         'fg=red txt=red',
                         'txt=" and "',
                         'bg=blue txt=blue']
        if ttwidgets.PyVers_f < 3.6:  # False: # True: # False: #
            gen_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in gen_text]
            expected_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in expected_text]
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromWidget3(self):
        # toplevel = tk.Tk()
        but = ttwidgets.Button(bg='wheat',
                               text='<tag fg=red>red</tag> and <tag '
                               'background=blue>blue</tag>')
        gen_text = but.gen_tag_attrs(kmode='option', extend=True)
        # abbrev=True) # , debug=True)
        expected_text = ['background=wheat text="<tag fg=red>red</tag> and '
                         '<tag background=blue>blue</tag>"',
                         'foreground=red text=red',
                         'text=" and "',
                         'background=blue text=blue']
        if ttwidgets.PyVers_f < 3.6:  # False: # True: # False: #
            gen_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in gen_text]
            expected_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in expected_text]
        self.assertEqual(gen_text, expected_text)

    def test_get_tag_attrs_fromWidget4(self):
        # toplevel = tk.Tk()
        but = ttwidgets.Button(bg='wheat',
                               text='<tag fg=red>red</tag> and <tag'
                               ' background=blue>blue</tag>')
        gen_text = but.gen_tag_attrs(kmode='option', extend=False)
        # abbrev=True) # , debug=True)
        expected_text = ['background=wheat text="<tag fg=red>red</tag> '
                         'and <tag background=blue>blue</tag>"',
                         'foreground=red', '', 'background=blue']
        # print('\n\n', pprint.pformat(gen_text))
        # print('\n\n', pprint.pformat(expected_text))
        if ttwidgets.PyVers_f < 3.6:  # False: # True: # False: #
            gen_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in gen_text]
            expected_text = \
                [sorted(ttwidgets.split_attrs(elem)) for elem in expected_text]
        self.assertEqual(gen_text, expected_text)


if __name__ == '__main__':
    unittest.main()
