"""
   Copyright 2020 Gary Michael Bloom
                  mailto:bloominator@hotmail.com
                  mailto:GaryBloomLaw@gmail.com

TTWidgets - Tagged-Text Multi-Font Enhanced Tkinter Widgets
=========

Package **TTWidgets** improves the Button, Label, and Listbox widgets of the
Tkinter library, and provides a bonus ToolTip widget, all with support for 
multiple fonts and visual schemes via *tagged-text* input.

The standard Tkinter Button and Label widgets are limited to a single set
of widget options (e.g. background/bg, foreground/fg, bitmap, cursor,
relief, etc), including a SINGLE FONT. With the **TTWidgets** enhancements,
*tagged text* can be passed in as text to create a compound widget, with
multiple fonts and visual option sets, that behaves like a simple widget.

The Button and Label implementations are complete.
The Listbox implementation is partial: there is no multi-font support, but 
the user can use the new 'text' option to pass in *tagged text* to define all
the elements with visual schemes.  The user can also pass *tagged text* to the
insert() method, and thereby skip the secondary call to itemconfig() for the
inserted element(s).
A full multi-font implementation of a Listbox may come later.

As a bonus, a ToolTip widget is included, which also accepts *tagged text*
as an input option, allowing the creation of colorful and multi-font ToolTips.

As a **TTWidgets** Button example:

    button = ttwidgets.TTButton(text="Isn't a <t case=title relief=raised bd=1 bg=white padx=2>button</t> with <tag bold fg=red bg=yellow>bold red on yellow text</tag> and \na <tag fg=blue funderline>hyperlink</tag> <tag relief=groove bd=2>groovy</tag> <tag bitmap=warning/>", command=lambda e=None: print("Released!"), bg='lightgray')

gives a Button with text "Isn't a Button with bold red on yellow text and
        a hyperlink groovy!", where:
- "Button" appears inside a raised button (with "title" case),
- "bold red on yellow text" is bold red text on a yellow background,
- "hyperlink" is blue and underlined,
- "groovy" is in a box with 'groove' relief, and
- "!" is a warning bitmap.

Here are two versions of the same button.  Which one would YOU rather use? :)

![exampleButton](https://user-images.githubusercontent.com/19311746/75097457-fa2e5b80-5578-11ea-9be4-016763568e50.jpg "Example TTButton")

For an overview of *tagged text*, please see the ttwidgets.TTWidget help.

This package includes the following:
    CLASSES:
        TTWidget    (base class for TTButton and TTLabel)
        TTButton    (inherits from TTWidget)
        TTLabel     (inherits from TTWidget)
        TTListbox   (inherits from Tkinter.Listbox)
        TTToolTip   (does not inherit, but uses a TTLabel)
    METHODS:    
        alias
        convert_font_dict_to_ttoptions_dict
        convert_ttoptions_dict_to_font_dict
        dump
        gen_tag_attrs
        get_font_dict
        get_named_font
        is_tagged_text
        pare_dict
        parse_tag_attrs
        quote
        split_attrs
        split_chunk
        split_dict_into_options_fontattrs_and_case
        split_tagged_text_into_chunks
        strip_tags
        unalias
        unmap
        update_named_font
        wrap_tagged_text


    Compatability:
        Py 3.4 - 3.9 is supported.
          (Runs on Py 3.1 - 3.3 but with some anomalies in TTListbox that were worked around)
        Py 3.0 and earlier are unsupported

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

from .ttwidgets import *

__version__ = "1.0.2"
