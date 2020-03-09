"""
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

For an overview of *tagged text*, please see help(ttwidgets.TTWidget).

This package includes the following:

    CLASSES:

        TTWidget (base class for TTButton and TTLabel)
        TTButton
        TTLabel
        TTListbox
        TTToolTip

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
        update_named_font
        wrap_tagged_text

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

import sys
import platform
PyMajorVers_i = sys.version_info[0]
if PyMajorVers_i == 3:
    import tkinter as tk
    from tkinter import font as tk_font
    from tkinter import scrolledtext as tk_scrolledtext
elif PyMajorVers_i == 2:
    import Tkinter as tk
    import tkFont as tk_font
    import ScrolledText as tk_scrolledtext
import collections
import io
import pprint
import re
import string
import textwrap

PyVers_f = float("{0}.{1}{2}".format(*sys.version_info[:3]))
PyVers_s = "{0}.{1}.{2}".format(*sys.version_info[:3])
Platform_s = platform.system()
sentinel = object()
sentinel_d = {}

if Platform_s == "Darwin":
    RMB = 2
else:
    RMB = 3
B1_Motion_s = "<B1-Motion>"
Bx_Motion_s = "<B%d-Motion>" % RMB
Button_1_s = "<Button-1>"
Button_x_s = "<Button-%d>" % RMB
ButtonRelease_1_s = "<ButtonRelease-1>"
ButtonRelease_x_s = "<ButtonRelease-%d>" % RMB

Chunk = collections.namedtuple("Chunk", "tag attrs text")
TAG, ATTRS, TEXT = range(3)

debug_mode_b = False

b_seqs = (
    B1_Motion_s,
    Bx_Motion_s,
)
SHIFT_KEY = 0x0001  # 1
CAPS_LOCK = 0x0002
CTRL_KEY = 0x0004  # 4
# ALT_L     = 0x0008
MOD1 = 0x0008  # NUMLOCK
NUM_LOCK = 0x0010
# ALT_R     = 0x0080
MOUSE_B1 = 0x0100  # 256
MOUSE_B2 = 0x0200
MOUSE_B3 = 0x0400  # 1024
ALT_KEY = 0x20000  # 131072 #

tk_default_fonts_t = ("TkDefaultFont", "TkTextFont", "TkFixedFont")
_named_fonts_d = {k: None for k in tk_default_fonts_t}

activebackground_as = abg_s = "abg"  # unofficial alias
activebackground_s = "activebackground"  # Widget option not in Frame
activeforeground_as = afg_s = "afg"  # unofficial alias
activeforeground_s = "activeforeground"  # Widget option not in Frame
activestyle_as = as_s = "as"
activestyle_s = "activestyle"  # Listbox option
anchor_as = anc_s = "anc"
anchor_s = "anchor"  # Widget option not in Frame
background_as = bg_s = "bg"  # alias
background_s = "background"
borderwidth_as = bd_s = "bd"  # alias
borderwidth_s = "borderwidth"
bitmap_as = bit_s = "bit"
bitmap_s = "bitmap"  # Widget option not in Frame
bold_as = b_s = "b"
capitalize_as = cap_s = "cap"
capitalize_s = "capitalize"
case_as = cas_s = "cas"
case_s = "case"
class_as = cls_s = "cls"
class_s = "class"  # Frame option not in Button/Label
colormap_as = cm_s = "cm"
colormap_s = "colormap"  # Frame option not in Button/Label
command_as = cmd_s = "cmd"  # unoffical alias for command
command_s = "command"  # Button option not in Label
compound_as = cpd_s = "cpd"
compound_s = "compound"  # Widget option not in Frame
container_as = ctr_s = "ctr"
container_s = "container"  # Frame option not in Button/Label
cursor_as = cur_s = "cur"
cursor_s = "cursor"
default_as = def_s = "def"
default_s = "default"  # Button option not in Label
disabledforeground_as = dfg_s = "dfg"  # unofficial alias
disabledforeground_s = "disabledforeground"  # Widget option not in Frame
expand_s = "expand"  # pack option
exportselection_as = es_s = "es"
exportselection_s = "exportselection"  # Listbox option
family_as = fam_s = "fam"
family_s = "family"
fill_s = "fill"  # pack option
font_as = fon_s = "fon"
font_s = "font"  # Widget option not in Frame
foreground_as = fg_s = "fg"  # alias
foreground_s = "foreground"  # Widget option not in Frame
foverstrike_as = o_s = "o"
foverstrike_s = "foverstrike"
frame_s = "frame"
funderline_as = u_s = "u"
funderline_s = "funderline"
height_as = h_s = "h"
height_s = "height"
highlightbackground_as = hlb_s = "hlb"  # unoffical alias
highlightbackground_s = "highlightbackground"
highlightcolor_as = hlc_s = "hlc"  # unoffical alias
highlightcolor_s = "highlightcolor"
highlightthickness_as = hlt_s = "hlt"  # unoffical alias
highlightthickness_s = "highlightthickness"
image_as = img_s = "img"
image_s = "image"  # Widget option not in Frame
in_s = "in"  # pack option
ipadx_as = ipx_s = "ipx"
ipadx_s = "ipadx"  # pack option
ipady_as = ipy_s = "ipy"
ipady_s = "ipady"  # pack option
italic_as = i_s = "i"
justify_as = jus_s = "jus"
justify_s = "justify"  # Widget option not in Frame
listvariable_as = lv_s = "lv"
listvariable_s = "listvariable"  # Listbox only
lower_as = lo_s = "lo"
lower_s = "lower"
overrelief_as = or_s = "or"
overrelief_s = "overrelief"  # Button option not in Label
overstrike_s = "overstrike"
padx_as = px_s = "px"
padx_s = "padx"
pady_as = py_s = "py"
pady_s = "pady"
relief_as = rel_s = "rel"
relief_s = "relief"
repeatdelay_as = rd_s = "rd"
repeatdelay_s = "repeatdelay"  # Button option not in Label
repeatinterval_as = ri_s = "ri"
repeatinterval_s = "repeatinterval"  # Button option not in Label
selectbackground_as = sbg_s = "sbg"  # for Listbox use, but not official
selectbackground_s = "selectbackground"  # Listbox only
selectborderwidth_as = sbd_s = "sbd"
selectborderwidth_s = "selectborderwidth"  # Listbox only
selectforeground_as = sfg_s = "sfg"  # for Listbox use, but not official
selectforeground_s = "selectforeground"  # Listbox only
selectmode_as = sm_s = "sm"
selectmode_s = "selectmode"
setgrid_as = sg_s = "sg"
setgrid_s = "setgrid"
side_s = "side"  # pack option
size_as = sz_s = "sz"
size_s = "size"
slant_as = sl_s = "sl"
slant_s = "slant"
state_as = sta_s = "sta"
state_s = "state"  # Widget option not in Frame
swapcase_as = sw_s = "sw"
swapcase_s = "swapcase"
takefocus_as = tf_s = "tf"
takefocus_s = "takefocus"
text_as = txt_s = "txt"
text_s = "text"  # Widget option not in Frame
textvariable_as = tv_s = "tv"
textvariable_s = "textvariable"  # Widget option not in Frame
title_as = ti_s = "ti"
title_s = "title"
underline_as = ul_s = "ul"
underline_s = "underline"  # Widget option not in Frame
upper_as = up_s = "up"
upper_s = "upper"
visual_s = "visual"  # Frame option not in Button/Label
weight_as = wt_s = "wt"
weight_s = "weight"
width_as = w_s = "w"
width_s = "width"
wraplength_as = wl_s = "wl"
wraplength_s = "wraplength"  # Widget option not in Frame
xscrollcommand_as = xsc_s = "xsc"
xscrollcommand_s = "xscrollcommand"  # Listbox only
yscrollcommand_as = ysc_s = "ysc"
yscrollcommand_s = "yscrollcommand"  # Listbox only


ttfont_dict_keys = (
    family_s,
    size_s,
    weight_s,
    slant_s,
    funderline_s,
    foverstrike_s,
)

font_dict_keys = (
    family_s,
    size_s,
    weight_s,
    slant_s,
    underline_s,
    overstrike_s,
)

case_dict_keys = (case_s, upper_s, lower_s, title_s, swapcase_s, capitalize_s)

event_types = (
    "Activate",
    "B1-",
    "B2-",
    "B3-",
    "B4-",
    "B5-",
    "Button-",
    "ButtonPress-",
    "ButtonRelease-",
    "Colormap",
    "Configure",
    "Deactivate",
    "Destroy",
    "Enter",
    "Expose",
    "FocusIn",
    "FocusOut",
    "Key",
    "KeyPress",
    "KeyRelease",
    "Leave",
    "Map",
    "Motion",
    "MouseWheel",
    "Property",
    "Return",
    "Unmap",
    "Visibility",
)

_widget_option_aliases_d = {
    activebackground_as: activebackground_s,
    activeforeground_as: activeforeground_s,
    activestyle_as: activestyle_s,
    anchor_as: anchor_s,
    bold_as: tk_font.BOLD,
    bg_s: background_s,  # OFFICIAL
    bd_s: borderwidth_s,  # OFFICIAL
    bitmap_as: bitmap_s,
    capitalize_as: capitalize_s,
    case_as: case_s,
    command_as: command_s,
    compound_as: compound_s,
    cursor_as: cursor_s,
    default_as: default_s,
    disabledforeground_as: disabledforeground_s,
    exportselection_as: exportselection_s,
    family_as: family_s,
    font_as: font_s,
    fg_s: foreground_s,  # OFFICIAL
    height_as: height_s,
    highlightbackground_as: highlightbackground_s,
    highlightcolor_as: highlightcolor_s,
    highlightthickness_as: highlightthickness_s,
    image_as: image_s,
    ipadx_as: ipadx_s,
    ipady_as: ipady_s,
    italic_as: tk_font.ITALIC,
    justify_as: justify_s,
    listvariable_as: listvariable_s,
    lower_as: lower_s,
    foverstrike_as: foverstrike_s,
    overrelief_as: overrelief_s,
    padx_as: padx_s,
    pady_as: pady_s,
    relief_as: relief_s,
    repeatdelay_as: repeatdelay_s,
    repeatinterval_as: repeatinterval_s,
    size_as: size_s,
    selectbackground_as: selectbackground_s,
    selectborderwidth_as: selectborderwidth_s,
    selectforeground_as: selectforeground_s,
    slant_as: slant_s,
    state_as: state_s,
    swapcase_as: swapcase_s,
    takefocus_as: takefocus_s,
    title_as: title_s,
    text_as: text_s,
    textvariable_as: textvariable_s,
    funderline_as: funderline_s,
    underline_as: underline_s,
    upper_as: upper_s,
    width_as: width_s,
    weight_as: weight_s,
    wraplength_as: wraplength_s,
    xscrollcommand_as: xscrollcommand_s,
    yscrollcommand_as: yscrollcommand_s,
}

_widget_option_unaliases_d = {}

label_override_d = {borderwidth_s: "0", padx_s: "0", pady_s: "0"}


def __init_widget_option_unaliases_d():
    if not _widget_option_unaliases_d:
        update_d = {v: k for k, v in _widget_option_aliases_d.items()}
        # update_d.update(**{funderline_s:'u', 'foverstrike':'o'})
        _widget_option_unaliases_d.update(**update_d)


def _flesh_config(widget, cfg, **kw):
    # make sure all font, case, and aliases are rep
    defaults_d = kw.pop("defaults", {})
    _ = kw.pop("pared", False)  # UNUSED pared_b
    d = cfg.copy()
    od = {}
    if isinstance(widget, (TTButton, TTLabel)):
        def_font = widget._widget_config(font_s)[-2]
    elif isinstance(widget, TTListbox):
        def_font = widget.config(font_s)[-2]
    elif isinstance(widget, TTToolTip):
        def_font = "TkDefaultFont"
    else:
        return cfg
    def_font_d = tk_font.Font(font=def_font)
    if text_s not in cfg:
        text = widget.text if hasattr(widget, text_s) else ""
        d[text_s] = (text_s, "", "", "", text)
    if case_s not in cfg:
        case = widget.case if hasattr(widget, case_s) else ""
        d[case_s] = (case_s, "", "", "", case)
    for k in ttfont_dict_keys:
        if k not in d:
            fk = k[1:] if k in (funderline_s, foverstrike_s) else k
            if hasattr(widget, "font_d"):
                val = widget.font_d.get(fk)
            else:
                val = ""
            d[k] = (k, "", "", def_font_d[fk], val)
    for k, v in kw.items():
        d[k] = (k, "", "", v[0], v[1])
    for k in sorted(d.keys()):
        od[k] = d[k]
    for k, v in defaults_d.items():
        od[k] = od[k][:3] + (v,) + od[k][4:]
    return od


def _func_name(levels=1):
    import inspect

    current_frame = inspect.currentframe()
    while levels > 0:
        current_frame = current_frame.f_back
        levels -= 1
    return current_frame.f_code.co_name


def _get_case_func(case):
    return lambda s: getattr(s, case)() if case else s


def _get_class_keys(cls):
    w = cls()
    cls_keys = w.keys()
    w.destroy()
    return cls_keys


def _get_pared_cfg(cfg, index=-1, **kw):
    index = kw.get("index", index)
    return {k: v[index] for k, v in cfg.items() if len(v) == 5}


def _is_tk_def_font(f):
    return str(f) in tk_default_fonts_t


def _merge_dicts(d1, *dX):  # for Py2
    m_d = collections.OrderedDict(d1)
    for d in dX:
        m_d.update(d)
    return m_d


def _print_cfg(widget, **kwargs):
    for key, val in kwargs.items():
        setattr(widget, "_print_cfg_{key}_b".format(key=key), val)


def _print_out(widget, text_w, *args, **kwargs):
    output = io.StringIO()
    both_b = kwargs.pop("both", kwargs.pop("all", False))
    screen_b = kwargs.pop(
        "screen", getattr(widget, "_print_cfg_screen_b", False)
    )  # True)) #
    text_b = kwargs.pop(text_s, getattr(widget, "_print_cfg_text_b", True))
    raise_b = kwargs.pop("Raise", False)
    if both_b:
        screen_b = text_b = True
    stringy = ""
    if text_w and text_b:
        if kwargs:
            print(*args, file=output, **kwargs)
            stringy = output.getvalue()
            text_w.insert(tk.END, stringy)
        elif widget:
            stringy = " ".join([str(a) for a in args]) + "\n"
            widget.after_idle(text_w.insert, tk.END, stringy)
        text_w.see(tk.END)
    if (screen_b or not text_w) and args and widget:
        widget.after_idle(
            lambda *a: print(*args, **kwargs)
        )
    if raise_b:
        print(*args, file=output, **kwargs)
        stringy = output.getvalue()
        raise Exception(stringy)
    return stringy


def alias(option=None):
    """Get the alias of a particular TTWidgets OPTION.

    Returns a 1-3 letter alias for any OPTION used in this module.
    'bd', 'bg', and 'fg' are the only official Tkinter option aliases, but
    this module assigns aliases to all options. For example, 'abg' is used
    for 'activebackground', 'anc' for 'anchor', etc.

    Returns the entire dict of option-to-alias mappings if no OPTION is given.

    In general, the alias of an option is:
       * for simple words, the first three letters (e.g. 'anc' for 'anchor',
         'cur' for 'cursor') unless there is a common abbreviation for the
         word (like 'cmd' for 'command', 'cpd' for 'compound', 'wt' for
         'weight', etc.), and
       * for compound-word options, the first letter of each word (i.e. 'abg'
         for 'activebackground', 'rd' for 'repeatdelay', etc.)

    When creating tagged text to pass into a TTWidget, all aliases are
    recognized and can be used in lieu of the full option name.

    TTWidgets also extends the standard widget options with special options
    relating to font attributes and text case:

        The font options are:

            family
            size
            weight
            slant
            funderline
            foverstrike

        The text case options are:

            case=<one of the below>
            upper
            lower
            title
            swapcase

    Call this routine without any options to access the entire dict of
    aliases, which is as follows:

        activebackground    ABG
        activeforeground    AFG
        activestyle         AS          (for Listbox)
        anchor              ANC
        bold                B           (custom for font)
        background          BG (official)
        borderwidth         BD (official)
        bitmap              BIT
        capitalize          CAP         (custom for case)
        case                CAS         (custom for case)
        class               CLS
        command             CMD
        compound            CPD
        cursor              CUR
        default             DEF
        disabledforeground  DFG
        exportselection     ES          (for Listbox)
        family              FA          (custom for font)
        font                FON
        foreground          FG (official)
        foverstrike         O           (custom for font)
        funderline          U           (custom for font)
        height              H
        highlightbackground HLB
        highlightcolor      HLC
        highlightthickness  HLT
        italic              I           (custom for font)
        image               IMG
        ipadx               IPX
        ipady               IPY
        justify             JUS
        listvariable        LV
        lower               LO          (custom for case)
        overrelief          OR
        padx                PX
        pady                PY
        relief              REL
        repeatdelay         RD
        repeatinterval      RI
        size                SZ          (custom for font)
        selectbackground    SBG         (for listbox)
        selectborderwidth   SBD         (for listbox)
        selectforeground    SFG         (for listbox)
        slant               SL
        state               STA
        swapcase            SW          (custom for case)
        takefocus           TF
        title               TI          (custom for case)
        text                TXT
        textvariable        TV
        underline           UL
        upper               UP          (custom for case)
        weight              WT
        width               W
        wraplength          WL
        xscrollcommand      XSC         (for Listbox)
        yscrollcommand      YSC         (for Listbox)
    """
    result = option
    if option is None:
        result = TTWidget.widget_option_unaliases_d
    elif len(option) > 3:
        resolved = TTWidget.widget_option_unaliases_d.get(option)
        if resolved:
            result = resolved
    return result


def convert_font_dict_to_ttoptions_dict(d):
    """
    Convert dict D keys 'underline' and 'overstrike' to 'funderline' and
    'foverstrike'.

    Returns a new dict.

    Prepares a font dict to be merged with a TTWidget options dict by
    converting keys 'underline' and 'overstrike' to 'funderline' and
    'foverstrike' to avoid collisions with the standard Tkinter widget
    'underline' option.
    """
    return {
        ("f" + k if k in (underline_s, overstrike_s) else k): v
        for k, v in d.items()
    }


def convert_ttoptions_dict_to_font_dict(d):
    """Strip the leading 'f' from the 'funderline' and 'foverstrike' dict D
    keys.

    Returns a new dict.

    Prepares a new dict with standard font attribute keys that can be used to
    create or modify a Tkinter font.
    """
    return {
        (k[1:] if k in (funderline_s, foverstrike_s) else k): v
        for k, v in d.items()
    }


def dump(widget, *a, **kw):
    """Dump a TTWidgets WIDGET, showing info about the parent Frame and all child
    Label widgets used to represent the compound TTWidgets WIDGET.

    See each TTWidget's custom dump method for details.
    """
    try:
        return widget.dump(*a, **kw)
    except AttributeError:
        pass


def gen_tag_attrs(widget=None, options_d=None, font=None, case=None, **kwargs):
    """Generate a Tagged-Text ATTRibutes_STRing for use in a tagged-text
        segment/chunk:  <tag ATTRibutes_STRing>text</tag> .

    Returns a single tagged-text string if no widget is passed in.
    Returns a list of tagged-text strings if a widget is passed in:
        a base widget string followed by each child widget's string.

    Arguments:
        WIDGET:     a widget from which to extract a list of tag attributes,
                    including Tkinter options, font, and case information
        OPTIONS_D:  dict of widget options, such as bg, fg, etc
        FONT:       can be named font, tuple, or font attributes dict
                    (as from the .actual() method)
        CASE:       the desired case (upper, lower, title, swapcase)

    Keyword Arguments:
        case:       keyword version of CASE arg
        extend:     include 'text' as an attribute in the output. (Default
                    is False.)
        font:       keyword version of FONT arg
        index:      return the attributes of a particular child widget when
                    WIDGET is given
        kmode:      whether to use aliases. 'a' for aliases, 'o' for options.
        options:    keyword version of OPTIONS_D arg
        pare:       when generating widget output, remove parent and default
                    values from the child attributes strings.
        recurse:    whether to recurse into the children of WIDGET. Default
                    is True.
        text:       a Text widget for outputting debug info
        widget:     keyword version of WIDGET arg. Set to None to ignore a
                    calling widget

    Notes: The Tkinter widget options are not completely disjoint from the
    TTWidget font attributes due to the commonly used 'underline'. A single
    OPTIONS_D dict can be used, but the overlap must be handled.  This is done
    by treating the font attributes 'underline' and 'overstrike' as special
    cases.  The 'underline' and 'overstrike' font attribute keys can be used
    in the font dict. But, they are changed to 'funderline' and
    'foverstrike' when merged with the TTWidget options into a single dict.
    This allows Tkinter options to co-exist with TTWidget (non-Tkinter)
    options in a single dict.

    So, if you want to pass the 'underline' Tkinter widget option, use
    'underline' in OPTIONS_D.  If you want to access the FONT 'underline'
    attribute, use 'funderline' in OPTIONS_D or 'underline' in FONT.  And font
    'overstrike' is handled similarly: 'foverstrike' in OPTIONS_D and
    'overstrike' in FONT.
    """
    auto_b = kwargs.get("auto", False)
    case = kwargs.get(case_s, case)
    extend_b = kwargs.get("extend", False)
    font = kwargs.pop("font", font or {})
    index_i = kwargs.pop("index", None)
    kmode_s = kwargs.get("kmode", "")  # a=alias, o=options, ''=unchanged
    options_d = kwargs.pop("options", options_d or {})
    pare_b = kwargs.get("pare", True)
    widget = kwargs.pop("widget", widget)
    text_w = kwargs.get(text_s, None)
    recurse_b = kwargs.pop("recurse", widget and isinstance(widget, TTWidget))
    fmt_s = ""
    font_d = {}
    w_font_d, w_options_d = {}, {}
    if index_i is not None and widget is None:
        raise Exception("Cannot set 'index' when 'widget' is None")
    if widget:  # and isinstance(widget, TTWidget): #
        excludes_t = () if widget.emulation_b else ()
        w_options_d = {
            k: v[-1]
            for k, v in widget.config().items()
            if len(v) == 5 and str(v[-1]) != str(v[-2]) and k not in excludes_t
        }
        try:
            w_options_d[case_s] = widget.case
        except AttributeError:
            pass
        w_font = widget.cget(font_s)  # w_options_d.pop(font_s, None)
        w_font_d = get_font_dict(w_font) if w_font else {}
        if pare_b and w_font_d:
            def_w_font = widget.config(font_s)[-2]
            def_w_font_d = get_font_dict(def_w_font)
            w_font_d = pare_dict(w_font_d, def_w_font_d)
    if font:
        if isinstance(font, str):
            try:
                font = tk_font.nametofont(font)
            except tk.TclError:
                pass
        elif type(font) in (list, tuple):
            font = tk_font.Font(font=font)
        if isinstance(font, tk_font.Font):
            font = font.actual()
        if isinstance(font, dict):
            font_d = font
    if case:  # is not None:
        options_d = _merge_dicts(options_d, dict(case=case))
    d = _merge_dicts(
        w_options_d,
        convert_font_dict_to_ttoptions_dict(w_font_d),
        options_d,
        convert_font_dict_to_ttoptions_dict(font_d),
        kwargs,
    )
    bad_opts = []
    for key, val in d.items():
        key = key.lower()
        if key in ("auto", "extend", "kmode", "pare",):  # text_s, ): #
            continue
        key2, key3, key4 = key[:2], key[:3], key[:4]
        kalias = alias(key)
        koption = unalias(key)
        if kmode_s:
            if kmode_s[0] == "a":  # alias
                keyout = kalias
                kfunc = alias
                auto_cpd, auto_bd = compound_as, bd_s
            elif kmode_s[0] == "o":  # option
                keyout = koption
                kfunc = unalias
                auto_cpd, auto_bd = compound_s, borderwidth_s  # bd_s #
        else:
            keyout = key
            kfunc = str
            auto_cpd, auto_bd = compound_s, borderwidth_s  # bd_s #
        if val:
            val = quote(val)
        if (
                key3 in (bg_s, background_s[:3], fg_s, foreground_s[:3])
                or key2 == underline_s[:2]
                or kalias in (bg_s, fg_s, underline_as)
        ):
            fmt_s += "%s=%s " % (keyout, val)
        elif key2 in (bitmap_s[:2], image_s[:2],) or kalias in (
                bitmap_as,
                image_as,
        ):
            fmt_s += "%s=%s " % (keyout, val)
            if auto_b and "%s=" % auto_cpd not in fmt_s:
                fmt_s += "%s=%s " % (auto_cpd, tk.CENTER)
        elif key3 in (bd_s, borderwidth_s[:3],):
            if "%s=%s " % (auto_bd, 1) in fmt_s:
                if val != 1:
                    fmt_s = fmt_s.replace(
                        "%s=%s " % (auto_bd, 1), "%s=%s " % (keyout, val)
                    )
            else:
                fmt_s += "%s=%s " % (keyout, val)
        elif key4 in (compound_s[:4],) or kalias == compound_as:
            if "%s=%s " % (auto_cpd, tk.CENTER) in fmt_s:
                if val != tk.CENTER:
                    fmt_s = fmt_s.replace(
                        "%s=%s " % (auto_cpd, tk.CENTER),
                        "%s=%s " % (keyout, val),
                    )
            else:
                fmt_s += "%s=%s " % (keyout, val)
        elif key3 == cursor_s[:3]:
            fmt_s += "%s=%s " % (keyout, val)
        elif key3 == font_s[:3]:
            fmt_s += "%s=%s " % (keyout, get_named_font(val))
        elif key2 in (relief_s[:2],):
            fmt_s += "%s=%s " % (keyout, val)
            if auto_b and "%s=" % auto_bd not in fmt_s:
                fmt_s += "%s=%s " % (auto_bd, 1)
        # special for TTListbox
        elif key[:7] in (
                sbg_s,
                selectbackground_s[:7],
                sbd_s,
                selectborderwidth_s[:7],
                sfg_s,
                selectforeground_s[:7],
        ):
            fmt_s += "%s=%s " % (keyout, val)
        # special for fonts
        elif key2 in (family_s[:2],):
            fmt_s += "%s=%s " % (keyout, val)
        elif key2 in (size_s[:2],):
            fmt_s += "%s=%s " % (keyout, val)
        elif key2 in (weight_s[:2],):
            fmt_s += "%s=%d " % (
                kfunc(tk_font.BOLD),
                1
                if isinstance(val, str) and val.lower() == tk_font.BOLD
                else 0,
            )
        elif key2 == slant_s[:2]:
            fmt_s += "%s=%d " % (
                kfunc(tk_font.ITALIC),
                1
                if isinstance(val, str) and val.lower() == tk_font.ITALIC
                else 0,
            )
        elif key3 in (funderline_as, funderline_s[:3]):
            fmt_s += "%s=%d " % (
                kfunc(funderline_s),
                1 if str(val) in ("1", "True") else 0,
            )
        elif key3 in (foverstrike_as, foverstrike_s[:3]):
            fmt_s += "%s=%d " % (
                kfunc(foverstrike_s),
                1 if str(val) in ("1", "True") else 0,
            )
        # special "case" implementation
        elif key3 == case_s[:3]:
            fmt_s += "%s=%s " % (kfunc(case_s), val)
        elif key2 == upper_s[:2] or key3 == capitalize_s[:3]:
            fmt_s += "%s=%s " % (kfunc(upper_s), val)
        elif key2 in (lower_s[:2], title_s[:2], swapcase_s[:2]):
            fmt_s += "%s=%s " % (keyout, val)
        elif key in ():
            bad_opts.append((key, val))
        elif key in (text_s, text_as):
            if extend_b or widget:
                fmt_s += "%s=%s " % (keyout, val)
        else:
            # bad_opts.append((key, val))
            fmt_s += "%s=%s " % (keyout, val)
    if bad_opts:
        _print_out(
            widget,
            text_w,
            "EXCEPTION: UNEXPECTED TAG ATTRS: %r" % bad_opts,
            Raise=True,
        )
    fmt = fmt_s.strip()
    if widget and isinstance(widget, TTWidget) and recurse_b:
        fmt = [
            fmt,
        ]
        for _, gathering in widget._get_kids(items=True):
            child = gathering["label"]
            case = gathering.get(case_s, "")
            kid_options = {
                k: v[-1]
                for k, v in child.config().items()
                if len(v) == 5
                and str(v[-1]) != str(v[-2])
                and (k, v[-1]) not in w_options_d.items()
                and not (k in label_override_d and str(v[-1]) == "0")
            }  #
            cf = kid_options.pop(font_s, None)
            cdf = child.config(font_s)[-2]
            if cf != cdf:
                c_font_d = pare_dict(get_font_dict(cf), get_font_dict(cdf))
            else:
                c_font_d = {}
            if case:
                kid_options.update(case=case)
            fmt.append(
                gen_tag_attrs(options=kid_options, font=c_font_d, **kwargs)
            )
    return fmt if index_i is None else fmt[index_i]


def get_font_dict(f):
    """Return a dict of font attributes for font F.

    Standard font attributes include: family, size, weight, slant, underline,
    overstrike.
    """
    return tk_font.Font(font=f).actual()


def get_named_font(f, **kw):
    """Return the name of a named font that matches the font attributes of
    the inputted font F and optional updates in KW.

    This routine stores a dict of named fonts so that they are not
    garbage-collected.  It returns the name of an existing font on match,
    and creates/adds a new font to the dict when there is no match.

    Optional updates in 'kw' are the standard font attributes:
        family
        size
        weight
        slant
        underline
        overstrike
    """
    if _named_fonts_d.get("TkDefaultFont") is None:
        for name in list(_named_fonts_d.keys()):
            _named_fonts_d[name] = tk_font.nametofont(name)
    #
    if f:
        fo = tk_font.Font(font=f)
        f_d = fo.actual()
        if kw:
            fo.config(**kw)
            f_d.update(**kw)
        for nf in _named_fonts_d:
            nf_d = tk_font.nametofont(nf).actual()
            if f_d == nf_d:
                return _named_fonts_d[nf]
        # didn't find it, so store created
        _named_fonts_d[str(fo)] = fo
        return fo
    return None


def is_tagged_text(text):
    """Indicate whether TEXT is tagged text.

    Returns True if TEXT contains attribute tags, False if plain text.
    """
    return len(text) > len(strip_tags(text))


def pare_dict(d, ref, strict_b=False, **kw):
    """Pare down a dict D according to a reference dict REF.

    Returns a dict, a pared-down version of D. Any item in D that matches
            an item in REF is removed from the output dict.

    Arguments:
        D:          the dict to be pared down
        REF:        a reference dict to be used for paring
        STRICT_B:   determines the paring mode.
                    If False, the output is as described above.
                    If True, all keys in D not in REF are also removed.
    """
    strict_b = kw.get("strict", strict_b)
    if strict_b:
        return {k: v for k, v in d.items() if k in ref and v != ref.get(k)}
    return {k: v for k, v in d.items() if k not in ref or v != ref.get(k)}


def parse_tag_attrs(tag_str, options_d=None, font_d=None, case="", **kwargs):
    """
    Splits tagged-text tag attributes from TAG_STR into standard Tkinter and
    custom TTWidgets widget options.

    Returns a tuple of three elements (by default):
        options dict:   contains Tkinter widget options
        font dict       contains TTWidget font attributes
        case string:    contains TTWidget case string
    Returns a single attribute (if keyword 'attr' is given)

    Arguments:
        OPTIONS_D:  optional starting state for the returned options dict
                    * gets updated if passed in
        FONT_D:     optional starting state for the returned font dict
                    * gets updated if passed in
        CASE:     optional starting state for the returned case string

    Keyword Arguments:
        attr:       a single attribute to return
    """
    attr_b = kwargs.pop("attr", "")
    auto_b = kwargs.pop("auto", False)
    font_d = kwargs.pop("font_d", font_d or {})
    options_d = kwargs.pop("options_d", options_d or {})
    case = kwargs.pop("case", case)
    widget = kwargs.pop("widget", None)
    text_w = kwargs.pop(text_s, None)
    bad_opts = []
    # INTs: height repeatdelay repeatinterval underline width; size fun fov
    for keyval in split_attrs(tag_str):
        if "=" in keyval:
            key, val = keyval.split("=")
            val = unquote(val)
        elif keyval:
            key, val = keyval, None
        else:
            continue
        key = key.lower()
        key2, key3, key4 = key[:2], key[:3], key[:4]
        lowval = val.lower() if val else val
        key = unalias(key)
        kalias = alias(key)
        if val == "None":  # in ('False', 'None') #
            pass
        elif key3 in (
                bg_s,
                background_s[:3],
                fg_s,
                foreground_s[:3],
        ) or kalias in (bg_s, fg_s):
            options_d.update(**{key: val})
        elif key2 in (bitmap_s[:2], image_s[:2],) or kalias in (
                bitmap_as,
                image_as,
        ):
            options_d.update(**{key: val})
            if auto_b and compound_s not in options_d:
                options_d.update(compound=tk.CENTER)
        elif key3 in (bd_s, borderwidth_s[:3],) or kalias == bd_s:
            options_d.update(borderwidth=val)
        elif key4 in (command_s[:4], compound_s[:4],) or kalias in (
                command_as,
                compound_as,
        ):
            options_d.update(**{key: val})
        elif (
                key2 in (height_s[:2], width_s[:2])
                or key3 in (repeatdelay_s[:3], repeatinterval_s[:3])
                or kalias
                in (height_as, width_as, repeatdelay_as, repeatinterval_as)
        ):
            options_d.update(**{key: int(val)})
        elif (
                key2 in (cursor_s[:2],)
                or key3 == font_s[:3]
                or kalias in (cursor_as, font_as)
        ):
            options_d.update(**{key: val})
        elif key2 in ("r", relief_s[:2],) or kalias == relief_as:
            options_d.update(relief=val)
            if auto_b and borderwidth_s not in options_d and val != tk.FLAT:
                options_d.update(borderwidth=str(1))
        elif key2 == underline_s[:2] or kalias == underline_as:
            options_d.update(underline=-1 if val is None else int(val))
        # special for TTListbox
        elif key[:7] in (
                sbg_s,
                selectbackground_s[:7],
                sfg_s,
                selectforeground_s[:7],
        ) or kalias in (selectbackground_as, selectforeground_as):
            options_d.update(**{key: val})
        # special for fonts
        elif key2 in (family_s[:2],) or kalias == family_as:
            font_d[family_s] = val
        elif key2 in (size_s[:2],) or kalias == size_as:
            try:
                font_d[size_s] = int(val)
            except ValueError:
                _print_out(
                    widget,
                    text_w,
                    "EXCEPTION: ERROR Setting Font Size to %r" % val,
                    Raise=True,
                )
        elif key3 in (bold_as, tk_font.BOLD[:3]) or kalias == bold_as:
            font_d[weight_s] = (
                tk_font.BOLD
                if str(val) not in ("0", "False",)
                else tk_font.NORMAL
            )
        elif key2 in (weight_s[:2],) or kalias == weight_as:
            font_d[weight_s] = val
        elif key2 in (italic_as, tk_font.ITALIC[:2]) or kalias == italic_as:
            font_d[slant_s] = (
                tk_font.ITALIC
                if str(val) not in ("0", "False",)
                else tk_font.ROMAN
            )
        elif key2 in (slant_s[:2],) or kalias == slant_as:
            font_d[slant_s] = val
        elif (
                key3 in (funderline_as, funderline_s[:3])
                or kalias == funderline_as
        ):
            font_d[underline_s] = 1 if str(val) not in ("0", "False",) else 0
        elif (
                key3 in (foverstrike_as, foverstrike_s[:3])
                or kalias == foverstrike_as
        ):
            font_d[overstrike_s] = 1 if str(val) not in ("0", "False",) else 0
        # special "case" implementation
        elif key3 in (case_s[:3],) or kalias == case_as:
            for s in (upper_s, capitalize_s, lower_s, title_s, swapcase_s):
                if s.startswith(lowval):
                    case = s if s != capitalize_s else upper_s
                    break
        elif (
                key2 == upper_s[:2]
                or key3 in (capitalize_s[:3],)
                or kalias in (upper_as, capitalize_as)
        ):
            if str(val) not in ("0", "False",):
                case = upper_s
        elif key2 in (lower_s[:2],) or kalias == lower_as:
            if str(val) not in ("0", "False",):
                case = lower_s
        elif key2 == title_s[:2] or kalias == title_as:
            if str(val) not in ("0", "False",):
                case = title_s
        elif key2 == swapcase_s[:2] or kalias == swapcase_as:
            if str(val) not in ("0", "False",):
                case = swapcase_s
        elif key in ():
            bad_opts.append((key, val))
        else:
            options_d.update(**{key: val})
    if bad_opts:
        _print_out(
            widget,
            text_w,
            "EXCEPTION: UNEXPECTED TAG ATTRS: %r" % bad_opts,
            Raise=True,
        )
    if attr_b:
        return (
            case
            if attr_b == case_s
            else options_d.get(attr_b, font_d.get(attr_b))
        )
    return options_d, font_d, case


def quote(s):
    """Ensure that any string S with white space is enclosed in quotes."""
    if isinstance(s, str):
        if " " in s or len(s.split()) > 1:
            start, end = s[0], s[-1]
            if start != end or start not in ('"', "'"):
                q1s, q1d, q3s, q3d = "'", '"', 3 * "'", 3 * '"'
                if q1d not in s:
                    s = q1d + s + q1d
                elif q1s not in s:
                    s = q1s + s + q1s
                elif q3d not in s:
                    s = q3d + s + q3d
                elif q3s not in s:
                    s = q3s + s + q3s
    return s


def split_attrs(s):
    """Split (an attributes) string S into elements, preserving quoted fields.

    Returns a list of strings.

    For example:
        split_attrs('family="Courier New" size=16 bold')
            yields:
        ['family="Courier New"', 'size=16', 'bold']
    """
    patt0 = r"\s*=\s*"
    if not sentinel_d.get("repatt0"):
        sentinel_d.update(repatt0=re.compile(patt0))
    s = sentinel_d["repatt0"].sub("=", s)
    outfields = []
    quoted_b = ""
    partial = []
    for f in re.split(r"(\s+)", s)[::-1]:
        if not quoted_b and f.endswith(('"', "'")):
            quoted_b = f[-1]
            partial.append(f)
        elif not quoted_b:
            if not f.isspace():
                outfields.append(f)
        else:  # quoted
            partial.append(f)
            if quoted_b in f:
                complete = "".join(partial[::-1])
                outfields.append(complete)
                partial = []
                quoted_b = ""
    if quoted_b:
        raise Exception("Imbalanced Quotes")
    return outfields[::-1]


def split_chunk(chunk):
    """Split a CHUNK of tagged text into the tag, attributes, and text.

    Returns a tuple of tag string, attributes string, and text string.

    Note that:
    - the 'tag' and 'attributes' strings may be empty if the CHUNK consists of
      only plain text,
    - the 'attributes' string may be empty if there were no attributes passed,
    and
    - the 'text' string may be empty.
    """
    if not sentinel_d.get("repatt2"):
        patt2 = r"<(t(?:ag)?)\s*([^>]*)>([^>]*)</t(?:ag)?>"
        sentinel_d.update(repatt2=re.compile(patt2, flags=re.IGNORECASE))
    # Chunk = collections.namedtuple('Chunk', 'tag attrs text')
    if chunk.lower().startswith("<t") and chunk.endswith("/>"):
        chunk_split = chunk.split(None, 1)  # [1][:-2]
        tag, attrs = chunk_split[0][1:], chunk_split[1][:-2]
        options_d, font_d, case = parse_tag_attrs(attrs)  # , attr=text_s) #
        text = options_d.pop(text_s, "")
        new_attrs = gen_tag_attrs(options=options_d, font=font_d, case=case)
        chunk = "<{tag} {new_attrs}>{text}</{tag}>".format(
            tag=tag, new_attrs=new_attrs, text=text
        )
    matches = sentinel_d["repatt2"].findall(chunk)
    result = (
        Chunk(*matches[0])
        if len(matches) == 1
        else Chunk("", "", chunk)
        if chunk
        else ()
    )
    return result


def split_dict_into_options_fontattrs_and_case(d):
    """Split a TTWidgets options dict D into a standard Tkinter options dict,
    a TTWidgets font attributes dict, and a TTWidgets case string.

    Returns a tuple of two dicts and a string.

    Note that font keys 'funderline' and 'foverstrike' in the TTWidgets
    options dict are changed to 'underline' and 'overstrike' in the fonts
    dict.
    """
    c_d = {
        case_s: (v if k == case_s else k)
        for k, v in d.items()
        if k in case_dict_keys
    }
    f_d = {
        (k[1:] if k in (funderline_s, foverstrike_s) else k): v
        for k, v in d.items()
        if k in ttfont_dict_keys
    }
    o_d = {
        k: v
        for k, v in d.items()
        if k not in ttfont_dict_keys + case_dict_keys
    }
    return o_d, f_d, c_d.get(case_s, "")


def split_tagged_text_into_chunks(text):
    """Split the tagged TEXT into separate chunks, each of which may be used to
    create a child widget.

    Returns a list of chunks, where each chunk includes:
    - an optional tag
    - optional attributes
    - optional text
    """
    if not sentinel_d.get("repatt1"):
        patt1 = r"(<t(?:ag)?.*?(?<=/)(?:t(?:ag)?)?>)"
        sentinel_d.update(
            repatt1=re.compile(patt1, flags=re.IGNORECASE | re.DOTALL)
        )
    return [chunk for chunk in sentinel_d["repatt1"].split(text) if chunk]


def strip_tags(text):
    """Strip away all tags from TEXT and return the printable text.

    Returns a string without any tagging information.
    """
    return "".join(
        [
            split_chunk(chunk).text
            for chunk in split_tagged_text_into_chunks(text)
        ]
    )


def unalias(opt=None):
    """Expand a TTWidget alias OPT into the full Tkinter or TTWidget option.

    Returns a string if OPT is given.
    Returns a dict of all alias-to-option mappings if OPT is not given.

    See help(ttwidgets.alias) for the full list of alias mappings.
    """
    if 1 <= len(opt) <= 3:
        resolved = TTWidget.widget_option_aliases_d.get(opt)
        if resolved:
            opt = resolved
    return TTWidget.widget_option_aliases_d if opt is None else opt


def unmap(widget):
    """Unmap a mapped WIDGET."""
    result = False
    if widget and widget.winfo_exists() and widget.winfo_ismapped():
        result = True
        geom_mgr = widget.winfo_manager()
        if geom_mgr == "grid":
            widget.grid_forget()
        elif geom_mgr == "pack":
            widget.pack_forget()
        elif geom_mgr == "place":
            widget.place_forget()
        else:
            result = False
    return result


def unquote(s):
    """Remove any enclosing quotes for S."""
    if isinstance(s, str) and len(s) > 1:
        if s[0] in ('"', "'") and s[-1] == s[0]:
            q = s[0]
            if len(s) >= 6 and s[0:3].count(q) == 3 and s[-3:].count(q) == 3:
                count = 3
            else:
                count = 1
            s = s[count:-count]
    return s


def update_named_font(name, **options):
    """Update a named font NAME with OPTIONS.

    Returns the updated named font.

    This can be used to update any named font, including the default Tkinter
    fonts, and so should be used with care.
    """
    try:
        font = tk_font.nametofont(name)
    except tk.TclError:
        font = None
    if font:
        _, font_d, _ = split_dict_into_options_fontattrs_and_case(options)
        font.config(**font_d)
        _named_fonts_d[str(font)] = font
    return font


def wrap_tagged_text(text, count=0):
    """Wrap TEXT according to the given character COUNT.

    Returns a text string with newlines inserted to cause text wrapping.
    """
    # break only on white space, ignoring label breaks
    wrapped_text = text
    if count <= 0:
        return text
    divs = [
        split_chunk(chunk) for chunk in split_tagged_text_into_chunks(text)
    ]
    # total_length = sum([len(div.text) for div in divs])  # UNUSED
    total_string = "".join([div.text for div in divs])
    final_nl_b = total_string.endswith("\n")
    total_lines = total_string.splitlines()
    wrapped_s = "\n".join(
        [textwrap.fill(s, count) for s in total_lines]
    ) + ("\n" if final_nl_b else "")
    # now have to map the wrapped_string to the divs!
    insert_pts = []
    divx = x = tl = wi = 0
    div = divs[divx]
    dl = len(div.text)
    for tsc in total_string:
        if wrapped_s[wi] != tsc:
            insert_pts.append([wi, divx, x, tl + x, tsc.isspace()])
            if not tsc.isspace():
                wi += 1
        wi += 1
        x += 1
        if x >= dl:
            tl += dl
            x = 0
            divx += 1
            try:
                div = divs[divx]
                if div:
                    try:
                        dl = len(div.text)
                    except AttributeError:
                        pass
            except IndexError:
                pass
    if insert_pts:
        divs_l = [list(div) for div in divs]
        for ipt in insert_pts[::-1]:
            _, divx, x, _, sp = ipt
            divs_l[divx][TEXT] = "{0}\n{1}".format(
                divs[divx][TEXT][:x],
                divs[divx][TEXT][x + 1 if sp else x:],
            )
        divs_t = [Chunk(*div) for div in divs_l]
        chunks = [
            (
                "<t {0}>{1}</t>".format(div.attrs, div.text)
                if div.attrs
                else div.text
            )
            for div in divs_t
            if div and div.text
        ]
        wrapped_text = "".join(chunks)
    return wrapped_text


class TTWidget(tk.Frame):
    """
    Implement a Compound Widget accepting Tagged Text used to generate
    multiple child Labels inside a parent Frame to support multiple fonts and
    visual schemes.

        Tagged Text consists of one or more Sections (or "Chunks") of text.
        Each new Section/Chunk starts a new Label.
        Each new line starts a new Label.
        Sections/Chunks can either be:
            plain text,
            OR
            tagged text, declared in HTML-like format:
                with separate start and end tags, as in:
                    <tag attr1="value1">text</tag>
                OR
                with a single tag, as in:
                    <tag attr1="value1" attr2="value2" text="some text" />
        Sections support the following Label widget options [shown with
        (Alias)]:
                background      (BG)
                bitmap          (BIT)
                borderwidth     (BD)
                compound        (CPD)
                cursor          (CUR)
                font            (FON)
                foreground      (FG)
                image           (IMG)
                relief          (REL)
                text            (TXT)
                underline       (UL)
        Special Font-specific attributes support has been added for:
                family          (FAM)
                size            (SZ)
                bold or weight  (B or WT)
                italic or slant (I or SL)
                underline       (U)
                overstrike      (O)
        Special Case modification has also been added:
            case (CAS), with values:
                upper or capitalize (UP or CAP)
                lower               (LO)
                swapcase            (SW)
                title               (TI)

    Example:

        '''Example Tags: <TAG BOLD="1">Bold</TAG>, Normal, <TAG
        ITALIC="1">Italic</TAG>, and <TAG FAMILY="Courier New"
        FOREGROUND="red">Red</TAG>'''

        Note that:
            'tag' can be abberviated to 't'.
            Single-word attribute values need not be enclosed in quotes.
            Values default to '1' if no '=' is given.
            Attribute aliases are supported.
            Tags and attributes are case-insensitive.

        So, the above could be shortened to:

        '''Example Tags: <t b>Bold</t>, Normal, <t i>Italic</t>, and
        <t fam="Courier New" fg=red>Red</t>'''


    The TTWidget is meant to act exactly like a regular Tkinter Button/Label,
    other than the special formatting accepted in the 'text' attribute.

    Implementation:
        Implemented:
            OPTIONS:
                activebackground
                activeforeground
                anchor
                background
                -bg
                bitmap
                borderwidth
                -bd
                command                 (Button only, not Label)
                compound
                cursor
                default                 (Button only, not Label)
                disabledforeground
                font
                foreground
                -fg
                image
                justify
                overrelief              (Button only, not Label)
                padx
                pady
                relief
                repeatdelay             (Button only, not Label)
                repeatinterval          (Button only, not Label)
                state
                text
                textvariable
                underline
                wraplength
            METHODS:
                flash()                 (both Button and Label)
                invoke()                (Button only, not Label)
        Partially Implemented
            Button options:
                Passed to Parent Frame:
                    height
                    highlightbackground
                    highlightcolor
                    highlightthickness
                    takefocus
                    width
                Passed to child Labels:
                    wraplength
        Not Implemented:
                N/A

    Notes:
        + Through the config() method, the user has strong control over all the
          underlying child widgets.

    Known Issues:
        - Windows function is better than Darwin and Linux
        - Bug: image centered under a multi-text text is obscured by the text's
          labels by default. may require rework via Canvas, but can be worked
          around by incorporating the image into a label along with the
          corresponding text.
    Ignored:
        - Widget width is not set "properly" (charCnt * width of "0")
          for text-only widgets. (less relevant due to "native" mode.
    """

    widget_option_aliases_d = _widget_option_aliases_d
    widget_option_unaliases_d = _widget_option_unaliases_d

    OPTIONS_NOT_IMPLEMENTED = ()
    #
    #
    opts_in_button_not_in_label = (
        command_s,
        default_s,
        overrelief_s,
        repeatdelay_s,
        repeatinterval_s,
    )
    methods_in_button_not_in_label = "flash invoke"
    opts_in_label_not_in_button = ()
    opts_in_frame_not_in_widget = (
        class_s,
        colormap_s,
        container_s,
        visual_s,
    )
    #
    opts_in_checkandradiobutton_not_in_button = (
        "indicatoron",
        "offrelief",
        "selectcolor",
        "selectimage",
        "variable",
    )
    methods_in_checkandradiobutton_not_in_button = "deselect select"
    opts_in_checkbutton_not_in_button = (
        opts_in_checkandradiobutton_not_in_button
        + ("offvalue", "onvalue",)
    )
    methods_in_checkbutton_not_in_button = "toggle"
    opts_in_radiobutton_not_in_button = (
        opts_in_checkandradiobutton_not_in_button + ("value",)
    )  #
    opts_in_listbox_not_in_button = ()
    methods_in_listbox_not_in_button = (
        "activate bbox curselection delete get index insert itemcget"
        " itemconfig nearest scan_dragto scan_mark see select_anchor"
        " select_clear select_includes select_set selection_anchor"
        " selection_clear selection_includes".split()
    )
    #
    widget_opts_to_base_cfg = (
        bitmap_s,
        borderwidth_s,
        compound_s,
        cursor_s,
        height_s,
        highlightbackground_s,
        highlightcolor_s,
        highlightthickness_s,
        image_s,
        relief_s,
        takefocus_s,
        width_s,
    )
    widget_opts_to_base_pack = (padx_s, pady_s)
    widget_opts_to_kids_cfg = (
        activebackground_s,
        activeforeground_s,
        disabledforeground_s,
        foreground_s,
        font_s,
        justify_s,
        state_s,
        wraplength_s,
    )
    widget_opts_to_kids_pack = ()  # should be empty
    widget_opts_to_base_and_kids = (
        anchor_s,
        background_s,
    )
    widget_opts_req_procreation = (bitmap_s, compound_s, image_s, text_s)
    widget_opts_for_custom_impl = widget_opts_req_procreation + (
        state_s,
        textvariable_s,
        underline_s,
    )  # not passed to Frame
    widget_opts_to_base = (
        widget_opts_to_base_cfg + widget_opts_to_base_pack
    )
    widget_opts_to_kids = (
        widget_opts_to_kids_cfg + widget_opts_to_kids_pack
    )
    #
    button_def_options = None
    label_def_options = None
    frame_def_options = None
    #
    #
    frame_pack_def_options_d = {
        anchor_s: tk.CENTER,
        expand_s: False,
        fill_s: tk.NONE,
        in_s: None,
        ipadx_s: 0,
        ipady_s: 0,
        padx_s: 0,
        pady_s: 0,
        side_s: tk.TOP,
    }

    priority_lists = [
        (image_s, bitmap_s, text_s),
        (textvariable_s, text_s),
    ]

    event_types_requiring_recursion = (
        e for e in event_types if e.startswith("B")
    )
    event_types_precluding_recursion = (
        e for e in event_types if e not in event_types_requiring_recursion
    )

    _instances = []

    _internal_bound_event_patterns_ = (
        "<Enter>",
        "<B1-Enter>",
        "<B%d-Enter>" % RMB,
        "<Leave>",
        "<B1-Leave>",
        "<B%d-Leave>" % RMB,
        "<Button-1>",
        "<ButtonRelease-1>",
        "<Button-%d>" % RMB,
        "<ButtonRelease-%d>" % RMB,
        "<B1-Motion>",
        "<B%d-Motion>" % RMB,
    )
    _internal_bound_event_types_ = (
        "Button",
        "ButtonRelease",
        "Enter",
        "Leave",
        "Motion",
    )

    default_debug = False

    @classmethod
    def __delete__(cls, self):
        found_b = self in cls._instances
        if found_b:
            cls._instances.remove(self)
        return found_b

    def __init__(self, master=None, widget=None, widget_class=None, **options):
        # store_b = not (widget)  # UNUSED
        super().__init__(master)
        self._kids = collections.OrderedDict()
        if widget and widget_class is None:
            self.widget_class = type(widget)
        if widget_class is None:
            widget_class = tk.Label
        self.widget_class = widget_class
        self.widget = widget or self.widget_class(self)
        if TTWidget.button_def_options is None:
            TTWidget.button_def_options = self._get_widget_default_options(
                tk.Button
            )
        if TTWidget.label_def_options is None:
            TTWidget.label_def_options = self._get_widget_default_options(
                tk.Label
            )
        if TTWidget.frame_def_options is None:
            TTWidget.frame_def_options = self._get_widget_default_options(
                tk.Frame
            )
        if TTWidget.widget_option_aliases_d is None:
            TTWidget.widget_option_aliases_d = _widget_option_aliases_d.copy()
            for key in self.widget.keys():
                if (
                        key not in TTWidget.widget_option_aliases_d
                        and key not in
                        TTWidget.widget_option_aliases_d.values()
                ):
                    TTWidget.widget_option_aliases_d[key[:3]] = key
            TTWidget.widget_option_unaliases_d = {
                v: k for k, v in TTWidget.widget_option_aliases_d.items()
            }
            TTWidget.widget_option_unaliases_d.update(
                **{background_s: bg_s, foreground_s: fg_s, borderwidth_s: bd_s}
            )
        #
        frame_options = {
            k: v[-1]
            for k, v in self._widget_config().items()
            if len(v) == 5 and k in self.frame_def_options
        }
        super().config(**frame_options)
        self._base_cfg = {}
        self._base_pack = {}
        self.command = None
        self.emulation_b = True
        self.font_d = {}
        # w_font = self._widget_cget(font_s)
        # self.font = get_named_font(w_font, create=True, modify=False)
        self.observer = None
        self.textvariable = None
        self.debug_text = options.pop("debug_text", None)
        #
        self.options, self.font_d = options, {}
        for opt, val in list(self._reorder_dict(self.options).items()) + list(
                self.font_d.items()
        ):  #
            self.config(**{opt: val, "init": True, "abstain": True})
        procreate_options = {}
        #
        self._kids = self._procreate(**procreate_options)
        self.font_d = tk_font.Font(font=self._widget_cget(font_s)).actual()
        toplevel = self.winfo_toplevel()
        if not hasattr(toplevel, "__TTWidget_d"):
            toplevel.__TTWidget_d = {}
        self._toplevelstorage = toplevel.__TTWidget_d[str(self)] = {}
        #
        self._prev_widget = None
        #
        self._depressed_w = None
        self._fired_b = None
        self._resolved_depressed = None
        self.after_id = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._from_base_class = type(obj)
        obj._index_ = len(cls._instances)
        cls._instances.append(obj)
        return obj

    def __repr__(self):
        options = {
            k: v[-1]
            for k, v in self._widget_config().items()
            if len(v) == 5 and str(v[-1]) != str(v[-2])
        }
        frame_options = {
            k: v[-1]
            for k, v in super().config().items()
            if len(v) == 5
            and str(v[-1]) != str(v[-2])
            and k in self._widget_config().keys()
        }
        if frame_options:
            options = _merge_dicts(options, frame_options)
        return "TTButton({0}, {1}, **{2})".format(self.master, None, options)

    def __str__(self):
        return super().__str__()

    def _activate(self, **kwargs):
        store_b = kwargs.get("store", True)
        for kid in self._get_kids():
            kid.config(state=tk.ACTIVE)
        bg = self._widget_cget(activebackground_s)
        self._base_config(bg=bg)
        if store_b:
            self._widget_config(state=tk.ACTIVE)
        return bg

    def _base_config(self, **options):
        debug_b = options.get("debug", False)
        if debug_b:
            self._print(
                "\n_BASE_CONFIG(self={self},  **{options})".format(
                    self=self, options=options
                )
            )
        _ = options.pop("caller", "")  # UNUSED caller
        debug_b = options.pop("debug", False)
        frames_b = options.pop("frames", True)  # False) #
        base_opts = {
            k: v
            for k, v in options.items()
            if k in (bg_s, background_s, cursor_s)
        }
        if frames_b:
            for frame in [
                    getattr(self, "_compoundframe", None),
                    getattr(self, "_textframe", None),
            ] + getattr(self, "_subframes", []):
                if frame and frame.winfo_exists():
                    frame.config(**base_opts)
        return super().config(**options)

    def _check_attributes(self, *args, **kwargs):
        default = kwargs.get(default_s, None)
        for attr in args:
            if not hasattr(self, attr):
                setattr(self, attr, default)

    def _child_config(self, child, **options):
        debug_b = options.get("debug", False)
        if debug_b:
            self._print(
                "\n_CHILD_CONFIG(self={self}, child={child}\n  **{options})"
                "".format(
                    child=child, self=self, options=options
                )
            )
        _ = options.pop("caller", "")  # UNUSED caller
        debug_b = options.pop("debug", False)
        kids_d = options.pop("kids", self._kids)
        vals_d = kids_d.get(str(child))
        if vals_d:
            if "options" not in vals_d:
                vals_d["options"] = {}
            if font_s in options:
                font = options.pop("font")
                font_d = tk_font.Font(font=font).actual()
            else:
                font_d = {}
            attrs = vals_d.get("attrs")
            l_font_d = vals_d.get("font_d", {})
            font_d = _merge_dicts(l_font_d, font_d)
            if attrs:
                options, font_d, _ = self.parse_tag_attrs(
                    attrs, options, font_d
                )
            if font_d:
                font = child.font = tk_font.Font(**font_d)
                options["font"] = str(font)
                vals_d["font_d"] = font_d
            vals_d["options"].update(**options)
        return child and child.winfo_exists() and child.config(**options)

    @staticmethod
    def _config_pared(widget):
        return {
            k: v[-2:]
            for k, v in widget.config().items()
            if len(v) == 5 and str(v[-2]) != str(v[-1])
        }

    def _disable(self, **kw):
        store_b = kw.get("store", True)
        bg = self._widget_cget(background_s)
        self._base_config(bg=bg)
        for kid in self._get_kids():
            kid.config(state=tk.DISABLED)
        if store_b:
            self._widget_config(state=tk.DISABLED)
        return bg

    def _discipline_family(self, **kw):
        reorder_b = kw.pop("reorder", False)  # True) #
        if reorder_b:
            super().lift()
            kids = self._get_kids(**kw)
            for kid in kids:
                kid.lift()
        self._widget_bind("<Enter>", self._enter, recurse=False, **kw)
        self._widget_bind("<Leave>", self._leave, recurse=False, **kw)
        if self.widget_class == tk.Button:
            self._widget_bind(
                "<Button-1>", self._press, recurse=True, **kw
            )  # ) #'+',
            self._widget_bind(
                "<ButtonRelease-1>", self._release, recurse=True, **kw
            )  # ) # '+',
        self._widget_rebind_externals(**kw)

    def _enable(self, **kw):
        store_b = kw.get("store", True)
        for kid in self._get_kids():
            kid.config(state=tk.NORMAL)
        bg = self._widget_cget(background_s)
        self._base_config(bg=bg)
        if store_b:
            self._widget_config(state=tk.NORMAL)
        return bg

    def _enter(self, event=None, **kw):
        bx_state = kw.get(
            "bx_state",
            getattr(event, state_s, 0) & (MOUSE_B1 | MOUSE_B2 | MOUSE_B3),
        )
        debug_b = kw.get("debug", self.default_debug)
        if event and self != event.widget:
            if debug_b:
                self._print(
                    "_ENTERing: IGNORED! DISPARITY/CHILD! Self={s}, Event={e}"
                    ", event.widget={ew}, bx_state={bx}".format(
                        s=self,
                        e=event,
                        ew=event.widget if event else "N/A",
                        bx=bx_state,
                    )
                )
            return
        if debug_b:
            self._print(
                "_ENTERing: Self={s}, Event={e}, event.widget={ew}, "
                "bx_state={bx}".format(
                    s=self,
                    e=event,
                    ew=event.widget if event else "N/A",
                    bx=bx_state,
                )
            )
        if bx_state:
            if self._widget_cget(state_s) == tk.NORMAL:
                self._activate()
                relief = tk.SUNKEN  # self._widget_cget(relief_s)
                tk.Frame.config(self, relief=relief)
        else:
            overrelief = (
                self._widget_cget(overrelief_s)
                if self.widget_class == tk.Button
                else None
            )
            if overrelief:
                super().config(relief=overrelief)
            if (
                    platform.system() != "Windows"
                    and self._widget_cget(state_s) == tk.NORMAL
            ):
                self._activate()
        return

    @classmethod
    def _event_gen(cls, widget, seq):
        if widget and isinstance(widget, cls):
            return widget.event_generate(seq)
        return None
        
    @staticmethod
    def _get_case_func(case):
        return lambda s: getattr(s, case)() if case else s

    def _get_current_widget_from_event(self, event, **kw):
        resolve_b = kw.get("resolve", False)
        # caller = kw.get("caller", "")  # UNUSED
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if resolve_b and widget:
            widget = self._resolve_widget(widget)
        return widget

    def _get_kids(self, *args, **kwargs):
        items_b = kwargs.get("items", False)
        kids_d = kwargs.get("kids", self._kids)
        name_b = kwargs.get("name", False)
        if name_b:
            return list(kids_d.keys())
        if items_b:
            return kids_d.items()
        if args:
            arg0 = args[0]
            return kids_d[arg0]["label"] if arg0 in kids_d else None
        return [vals["label"] for vals in kids_d.values()]

    def _get_frame_def_opts(self):
        return {
            k: v
            for k, v in self.frame_def_options.items()
            if k not in self.opts_in_frame_not_in_widget
        }

    def _get_opts_for_base(self):
        return {
            k: v
            for k, v in self.options.items()
            if k
            in (
                self.widget_opts_to_base_cfg
                + self.widget_opts_to_base_and_kids
            )
            and k in self.frame_def_options
        }  # opts_in_frame_not_in_widget}

    def _get_opts_for_kids(self):
        return {
            k: v
            for k, v in self.options.items()
            if k
            in (
                self.widget_opts_to_kids_cfg
                + self.widget_opts_to_base_and_kids
            )
            and not k.startswith(text_s)
        }

    @staticmethod
    def _get_widget_default_options(cls):
        widget = cls()
        options = {k: v[-2] for k, v in widget.config().items() if len(v) == 5}
        widget.destroy()
        return options

    def _indicate_default(self, on_b=None, bd=None, color=None, **kwargs):
        if isinstance(self, TTLabel):
            return False
        on_b = kwargs.get("on", on_b)
        bd = kwargs.get(bd_s, bd)
        color = kwargs.get("color", color)
        if on_b is None:
            default = self._widget_cget(default_s)
            on_b = default == tk.ACTIVE
        if bd is None:
            bd = self._widget_config(highlightthickness_s)[-2]
        if color is None:
            color = self._widget_config(highlightcolor_s)[-2]
        if on_b:
            super().config(
                {
                    highlightbackground_s: color,
                    highlightcolor_s: color,
                    highlightthickness_s: bd,
                }
            )
        else:
            super().config({highlightthickness_s: 0})
        return True

    def _is_mine(self, other):
        result = other in self._get_kids()
        if not result and other:
            result = other in [
                getattr(self, "_compoundframe", None),
                getattr(self, "_textframe", None),
            ] + getattr(self, "_subframes", [])
        return result

    def _leave(self, event=None, **kw):
        bx_state = kw.get(
            "bx_state",
            getattr(event, state_s, 0) & (MOUSE_B1 | MOUSE_B2 | MOUSE_B3),
        )
        debug_b = kw.get("debug", self.default_debug)  # False) # True) #
        if event and self != event.widget:
            if debug_b:
                self._print(
                    "_LEAVing: IGNORED! DISPARITY/CHILD! Self={s}, Event={e},"
                    " event.widget={ew}, bx_state={bx}".format(
                        s=self,
                        e=event,
                        ew=event.widget if event else "N/A",
                        bx=bx_state,
                    )
                )
            return
        if debug_b:
            self._print(
                "_LEAVing: Self={s}, Event={e}, event.widget={ew}, "
                "bx_state={bx}".format(
                    s=self,
                    e=event,
                    ew=event.widget if event else "N/A",
                    bx=bx_state,
                )
            )
        overrelief = (
            self._widget_cget(overrelief_s)
            if self.widget_class == tk.Button
            else None
        )
        if bx_state:
            if self._widget_cget(state_s) == tk.ACTIVE:
                self._enable()
                relief = self._widget_cget(relief_s)
                tk.Frame.config(self, relief=relief)
        else:
            if overrelief:
                relief = self._widget_cget(relief_s)
                tk.Frame.config(self, relief=relief)
            if (
                    platform.system() != "Windows"
                    and self._widget_cget(state_s) == tk.ACTIVE
            ):
                self._enable()
        return

    def _motion(self, event=None, **kw):
        """Simulate an Enter/Leave event when a mouse button is down."""
        debug_b = kw.get("debug", self.default_debug)
        if self == event.widget:
            return  # skipping for frame. only need for kids.
        if not hasattr(self, "_prev_widget"):
            self._prev_widget = None
        current_widget = self._get_current_widget_from_event(event)
        resolved_current = self._resolve_widget(current_widget)
        resolved_previous = self._resolve_widget(self._prev_widget)
        # event_widget = self._resolve_widget(event.widget) # UNUSED
        if debug_b:
            self._print(
                "{fn} Self={s}, Event.Widget={ew} Event.Num={n} EVENT={e}"
                " **{kw}, CURRENT={c}".format(
                    fn=_func_name().upper(),
                    s=self,
                    ew=event.widget,
                    n=event.num,
                    e=repr(event),
                    kw=kw,
                    c="SAME"
                    if current_widget == event.widget
                    else current_widget
                    if current_widget
                    else "NONE",
                )
            )
        bx_state = event.state & (MOUSE_B1 | MOUSE_B2 | MOUSE_B3)
        if bx_state and resolved_current != resolved_previous:
            if resolved_previous == self:
                # self._event_gen(self, '<Leave>')
                self._leave(bx_state=bx_state)
            if resolved_current == self:
                # self._event_gen(self, '<Enter>')
                self._enter(bx_state=bx_state)
        self._prev_widget = current_widget

    def _pack_anchored_frame(self, frame, **kwargs):
        def __pad_frame(self, frame, **kwargs):
            debug_b = kwargs.pop("debug", False)
            padx = kwargs.pop(padx_s, None)
            pady = kwargs.pop(pady_s, None)
            text_b = kwargs.pop(text_s, None)
            graphic_b = kwargs.pop("graphic", None)
            if debug_b:
                print('Text_b is ', text_b, ', Graphic_b ', graphic_b)
            if padx is None or pady is None:
                bd = str(self._widget_cget(borderwidth_s))
                padx = str(self._widget_cget(padx_s))
                pady = str(self._widget_cget(pady_s))
                if text_b:
                    font = tk_font.Font(font=self._widget_cget(font_s))
                    w, h = font.measure("0"), font.metrics("linespace")
                    padx = 10 * w // 20  # 20 #
                    pady = 10 * h // 60  # 50 #
                    if debug_b:
                        print("FONT METRICS:", font, w, h, padx, pady)
                else:
                    pass
                ipadx = bd
                ipady = bd
            if frame:
                frame.config(padx=padx, pady=pady)
                if self.winfo_ismapped():
                    self.pack_configure(ipadx=bd, ipady=bd)
            if debug_b:
                print("PADDING IS ", repr(padx), repr(pady))
            return padx, pady, ipadx, ipady

        anchor = kwargs.pop(anchor_s, tk.CENTER)
        anchor = anchor if anchor != tk.CENTER else None
        frame.grid(row=0, column=0, sticky=anchor)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        __pad_frame(self, frame, **kwargs)

    def _press(self, event=None, **kw):
        debug_b = kw.get("debug", self.default_debug)
        num = kw.get("num", getattr(event, "num", -1))
        event_widget = self._resolve_widget(event.widget)
        if debug_b:
            self._print(
                "_PRESS: B{n} Self={s}, Event.Widget={ew}, Event={e}".format(
                    n=num, s=self, ew=event.widget, e=event
                )
            )
        if self._widget_cget(state_s) == tk.DISABLED:
            return None
        self._depressed_w = event.widget
        self._resolved_depressed = event_widget
        if not hasattr(self, "_bx_bindings"):
            setattr(self, "_bx_bindings", {})
        if self == event.widget:
            for mod in ("B1", "B%d" % RMB):
                self._widget_bind(
                    "<%s-Enter>" % mod, self._enter, recurse=False
                )
                self._widget_bind(
                    "<%s-Leave>" % mod, self._leave, recurse=False
                )
        elif self._is_mine(event.widget):  # REBIND after Procreation?
            if self._bx_bindings:
                bind_widget = self._bx_bindings.pop("widget", None)
                if self._valid_widget(bind_widget):
                    for seq, funcid in self._bx_bindings.items():
                        bind_widget.unbind(seq, funcid)
            self._bx_bindings["widget"] = event.widget
            self._bx_bindings[B1_Motion_s] = event.widget.bind(
                B1_Motion_s, self._motion
            )
            self._bx_bindings[Bx_Motion_s] = event.widget.bind(
                Bx_Motion_s, self._motion
            )
        else:
            pass
        self._fired_b = False
        self.config(relief=tk.SUNKEN, store=False)
        repeatdelay = self._widget_cget(repeatdelay_s)
        if repeatdelay:
            self.after_id = self.after(int(repeatdelay), self._repeat_click)
        return self._activate()

    def _print(self, *args, **kwargs):
        return _print_out(
            self, getattr(self, "debug_text", None), *args, **kwargs
        )

    def _procreate(self, master=None, **options):
        """Create the child widgets that comprise the compound widget.

        Returns a dict of information about the child widgets.

        Note that a single widget is used internally to store state
        information.  If only a single child widget would be created, the
        creation of the child widget is skipped and the internal state widget
        is mapped instead.
        """
        bind_b = options.pop("bind", False)
        debug_b = options.pop("debug", self.default_debug)
        if debug_b:
            self._print("PROCREATING for {0}!".format(self))
        suppress_f = options.pop("suppress", False)
        text = options.pop(text_s, None)
        if text is not None:
            self._update_text(text)
            return {}
        for child in self.winfo_children():
            if child != self.widget:
                child.destroy()
        font = self.options.get(font_s, {})
        if not font:
            font = self._widget_cget(font_s)
        if font:
            try:  # if type(font) in (tuple, str):
                font = tk_font.Font(font=font)
            except tk.TclError:
                font = None
            except NameError:
                font = None
            base_font_d = font.actual() if font else {}
        else:
            base_font_d = {}
        if self._widget_cget(textvariable_s):
            textvariable = self._widget_cget(textvariable_s)
            text = textvariable.get()
        else:
            text = self._widget_cget(text_s)
        text_b = text
        text_chunks = [
            tc for tc in split_tagged_text_into_chunks(text_b) if tc
        ]
        self.emulation_b = is_tagged_text(text_b) and len(text_chunks) > 1
        self.native_b = not self.emulation_b
        if not self.emulation_b:
            # use the widget instead of procreating
            self._kids = {}
            font_d = {}
            temp_font = None
            case = ""
            if text_b and is_tagged_text(text_b):
                _tag, chunk_tags, chunk_text = split_chunk(text_b)
                options, font_d, case = self.parse_tag_attrs(
                    chunk_tags, self.options.copy(), base_font_d.copy()
                )
                if font_d:
                    temp_font = tk_font.Font(**font_d)
                    options[font_s] = temp_font
                case_func = self._get_case_func(case)
                chunk_text = case_func(chunk_text)
            else:
                chunk_tags, chunk_text = "", text_b
            options[text_s] = chunk_text
            #
            super().config(**self._get_frame_def_opts())
            self.widget.config(**options)
            self.widget.tagged = text_b
            self.widget.text = chunk_text
            self.widget.case = case
            # if self.widget.winfo_ismapped():
            #     "complain that already mapped?"
            self.widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.widget.lift()
            if debug_mode_b:
                self.widget.config(bg="magenta")
            self._widget_rebind_externals()
            return {}
        # create the emulated widget
        # if not self.widget.winfo_ismapped():
        #     "complain that it is not mapped and should have been?"
        self.widget.pack_forget()
        super().config(**self._get_opts_for_base())
        #
        image = self._widget_cget(image_s)
        if image:
            bitmap = ""
        else:
            bitmap = self._widget_cget(bitmap_s)
        graphic_b = image or bitmap
        compound = self._widget_cget(compound_s)  # for graphic
        if graphic_b:
            if compound == tk.NONE:
                text_b = ""
        else:
            text_b = text_b or ""
        # compound_b = compound if text_b and graphic_b else ""  # UNUSED
        if not options:
            options = _merge_dicts(
                self._get_opts_for_kids(),
                label_override_d,
                {compound_s: compound},
            )
        frame_options = {
            k: v for k, v in options.items() if k in self.frame_def_options
        }
        grow = 1 if compound == tk.BOTTOM else 0
        gcol = 1 if compound == tk.RIGHT else 0
        trow = 1 if compound == tk.TOP else 0
        tcol = 1 if compound == tk.LEFT else 0
        gathering = collections.OrderedDict()
        self._textframe = None
        self._subframes = []
        self._compoundframe = tk.Frame(self)
        if text_b and is_tagged_text(text_b) and len(text_chunks) > 1:
            text = text_b
            wraplength = self.winfo_fpixels(self._widget_cget(wraplength_s))
            if wraplength > 0:
                # w_font = tk_font.Font(font=self._widget_cget(font_s))#UNUSED
                wfont_W = font.measure("0")
                # wfont_H = font.metrics("linespace")  # UNUSED
                wrapchars = max(wraplength // wfont_W, 1)
                text = wrap_tagged_text(text_b, wrapchars)
            #
            if debug_b:
                self._print("TEXT is {0!r}".format(text))
            chunks = split_tagged_text_into_chunks(text)
            if debug_b:
                self._print("CHUNKS are %r" % chunks)
            row = column = 0
            self._textframe = tk.Frame(self._compoundframe)
            self._subframes = [tk.Frame(self._textframe)]
            for chunk in chunks:
                if debug_b:
                    self._print("CHUNK is %r" % chunk)
                if not chunk:
                    continue
                _tag, chunk_tags, chunk_text = split_chunk(chunk)
                label_options, font_d, case = self.parse_tag_attrs(
                    chunk_tags, options.copy(), base_font_d.copy()
                )
                if font_d:
                    temp_font = tk_font.Font(**font_d)
                    label_options[font_s] = temp_font
                else:
                    temp_font = None
                case_func = self._get_case_func(case)
                chunk_lines = chunk_text.splitlines(1) or [
                    "",
                ]
                if debug_b:
                    self._print("CHUNK_LINES is %r" % chunk_lines)
                line_cnt = len(chunk_lines)
                for i, line in enumerate(chunk_lines):
                    orig_line = line
                    line = case_func(line)
                    end_nl_f = line.endswith("\n")
                    if end_nl_f:
                        line = line[:-1]
                    lab = tk.Label(self, text=line, **label_options)
                    gathering[str(lab)] = dict(
                        label=lab,
                        index=len(gathering),
                        type=text_s,
                        row=row,
                        column=column,
                        text1=orig_line,
                        text2=line,
                        attrs=chunk_tags,
                        font_d=font_d,
                        font=temp_font,
                        options=label_options,
                        case=case,
                    )
                    if not suppress_f:
                        lab.pack(
                            in_=self._subframes[-1],
                            side=tk.LEFT,
                            fill=tk.BOTH,
                            expand=True,
                        )
                    if debug_b:
                        self._print(
                            "PUTTING %r at %d,%d" % (line, row, column)
                        )
                    if bind_b and self.widget_class == tk.Button:
                        lab.bind("<Button-1>", self._press)
                        lab.bind("<ButtonRelease-1>", self._release)
                    if i < line_cnt - 1 or end_nl_f:
                        self._subframes.append(tk.Frame(self._textframe))
            layout_options = dict(row=trow, column=tcol,)
            anchor = self._widget_cget(anchor_s)
            justify = self._widget_cget(justify_s)
            if justify != tk.CENTER:
                sticky = tk.E if justify == tk.RIGHT else tk.W
                layout_options.update(**{"sticky": sticky})
            if debug_mode_b:
                super().config(
                    highlightthickness=2,
                    highlightcolor="magenta",
                    highlightbackground="magenta",
                    bg="cyan",
                )
            if debug_mode_b:
                self._textframe.config(
                    highlightthickness=2,
                    highlightcolor="teal",
                    highlightbackground="teal",
                )
            self._textframe.grid(
                in_=self._compoundframe, row=trow, column=tcol
            )
            self._textframe.config(**frame_options)
            for f in self._subframes:
                f.grid(**layout_options)
                f.config(**frame_options)
                if debug_mode_b:
                    f.config(
                        highlightthickness=2,
                        highlightcolor="magenta",
                        highlightbackground="magenta",
                    )
                layout_options["row"] += 1
            underline = self._widget_cget(underline_s)
            if underline >= 0:
                self._underline(underline, gathering)
        if (
                graphic_b
                or not self.emulation_b
                and (
                    not text_b
                    or not is_tagged_text(text_b)
                    or len(text_chunks) == 1
                )
        ):
            key = None
            gathered = {}
            font_d = {}
            temp_font = None
            if graphic_b:
                key = image_s if image else bitmap_s
                options = _merge_dicts({key: graphic_b}, options)
                gathered = {"type": key, "data": graphic_b, "options": options}
            if not self.emulation_b:
                if not text_b:
                    chunk_tags, chunk_text = "", ""
                elif is_tagged_text(text_b):
                    _tag, chunk_tags, chunk_text = split_chunk(text_b)
                    options, font_d, case = self.parse_tag_attrs(
                        chunk_tags, options, base_font_d.copy()
                    )
                    if font_d:
                        temp_font = tk_font.Font(**font_d)
                        options[font_s] = temp_font
                    case_func = self._get_case_func(case)
                    chunk_text = case_func(chunk_text)
                else:
                    chunk_tags, chunk_text = "", text_b
                options[text_s] = chunk_text
                gathered.update(
                    text=options[text_s],
                    options=options,
                    text1=text_b,
                    text2=chunk_text,
                    attrs=chunk_tags,
                    font_d=font_d,
                    font=temp_font,
                )
                key = text_s if key is None else compound_s
            gl = tk.Label(self, **options)
            text_rows = (
                len(self._subframes) if hasattr(self, "_subframes") else 1
            )
            layout_options = dict(
                in_=self._compoundframe, row=grow, column=gcol
            )
            rowspan = (
                text_rows if compound in (tk.LEFT, tk.RIGHT, tk.CENTER) else 1
            )
            if rowspan:
                layout_options.update(rowspan=rowspan)
            anchor = self._widget_cget(anchor_s)
            if anchor != tk.CENTER:
                layout_options.update(**{"sticky": anchor})
            gl.grid(**layout_options)
            gathered.update(label=gl, index=len(gathering), type=key)
            gathering[str(gl)] = gathered
            for kid in self._get_kids(kids=gathering):
                if kid != gl:
                    gl.lower(kid)
        self._compoundframe.config(**frame_options)
        anchor = self._widget_cget(anchor_s)
        self._pack_anchored_frame(
            self._compoundframe, anchor=anchor, text=text_b, graphic=graphic_b
        )
        self._indicate_default()
        if debug_b:
            self._print("GATHERING is %r" % gathering)
        self._discipline_family(kids=gathering)
        return gathering

    def _release(self, event=None, **kw):
        debug_b = kw.get("debug", self.default_debug)
        num = kw.get("num", getattr(event, "num", -1))
        if self._widget_cget(state_s) == tk.DISABLED:
            return None
        # bx_motion_b = event.state & (MOUSE_B1 | MOUSE_B2 | MOUSE_B3)# UNUSED
        num = event.num
        current_widget = self._get_current_widget_from_event(event)
        resolved_current = self._resolve_widget(current_widget)
        # event_widget = self._resolve_widget(event.widget)  # UNUSED
        if debug_b:
            self._print(
                "_RELEASE: B{n} Self={s}, Event.Widget={ew}, Event={e}, "
                "CurrentWidget={cw}".format(
                    n=num, s=self, ew=event.widget, e=event, cw=current_widget
                )
            )
        self.config(relief=tk.RAISED, store=False)
        self._check_attributes("_fired_b")  # '_inside_f',
        if self == resolved_current and not self._fired_b:
            self.invoke()
            self._fired_b = True
        self.after_id = None
        if self._valid_widget(self._depressed_w):
            if self._is_mine(self._depressed_w):
                bind_widget = self._bx_bindings.pop("widget", None)
                if bind_widget and bind_widget == self._depressed_w:
                    for seq, funcid in self._bx_bindings.items():
                        if debug_b:
                            self._print(
                                "TRYING TO UNBIND Seq {seq!r} with FuncID "
                                "{funcid!r} from Widget {widget!r}".format(
                                    seq=seq,
                                    funcid=funcid,
                                    widget=self._depressed_w,
                                )
                            )
                        self._depressed_w.unbind(seq, funcid)
        self._depressed_w = None
        return self._enable() if platform.system() == "Windows" else None

    @staticmethod
    def _reorder_dict(d):
        od = collections.OrderedDict(
            {k: v for k, v in sorted(d.items(), reverse=False) if "debug" in k}
        )
        od.update(
            {
                k: v
                for k, v in sorted(d.items(), reverse=True)
                if k.startswith(text_s)
            }
        )
        od.update({k: v for k, v in sorted(d.items()) if k not in od})
        return od

    def _repeat_click(self):
        self._check_attributes("_depressed_w", "after_id")
        if self._depressed_w:
            if self.after_id:
                self.invoke()
                self._fired_b = True
                self.after_id = None
            repeatinterval = self._widget_cget(repeatinterval_s)
            if repeatinterval:
                self.after_id = self.after(
                    int(repeatinterval), self._repeat_click
                )
        else:
            self.after_id = None

    @classmethod
    def _resolve_widget(cls, widget):
        # debug_b = kw.get("debug", cls.default_debug)  # UNUSED
        while widget and not isinstance(widget, cls):
            if type(widget) in (tk.Frame, tk.Button, tk.Label):
                widget = widget.master
            else:
                break
        return widget

    def _set_default_debug(self, val):
        self.default_debug = val

    @classmethod
    def _top_widget(cls, widget):
        while hasattr(widget, "master"):
            if isinstance(widget, cls):
                return cls
            widget = widget.master
        for instance in cls._instances:
            if widget in instance._get_kids():
                return instance
        return None

    def _trace_callback(self, varname=None, varindex=None, varmode=None):
        if varmode == "w":
            # value = self.getvar(varname)  # UNUSED
            self._kids = self._procreate()

    def _underline(self, pos=-1, gathering=None, **kw):
        store_b = kw.get("store", True)
        if store_b:
            self._widget_config(underline_s, pos)
        if not self.emulation_b:
            return
        if gathering is None:
            gathering = self._kids
        if pos >= 0:
            count = 0
            for _, vals in gathering.items():
                prev_count = count
                count += len(vals["text1"])
                if prev_count <= pos < count:  # 'in this label'
                    index = pos - prev_count
                else:
                    index = -1
                label = vals["label"]
                if label and label.winfo_exists():
                    label.config(**{underline_s: index})
        return

    def _unmap(self, widget):
        return unmap(widget)

    def _update_text(self, text):
        textvariable = self._widget_cget(textvariable_s)
        if textvariable:
            textvariable.set(text)
        else:
            self.config(**{text_s: text})

    def _valid_widget(self, widget):
        if isinstance(widget, str):
            try:
                widget = self.nametowidget(widget)
            except KeyError:
                widget = None
        if widget and not widget.winfo_exists():
            widget = None
        return widget

    def _widget_bind(self, sequence=None, func=None, add=None, **kw):
        """Bind the requested SEQUENCE and store the info internally, making
        sure that no external call interferes with the internal state.

        For some external calls (like B1-3, make the call recursive down to the
        child widgets and track it so we can clean up if the user tries to
        unbind.

        This routine makes all bindings 'adds' but keeps track to simluate user
        non-adds.
        """
        debug_b = kw.get("debug", self.default_debug)
        if debug_b:
            self._print(
                "_WIDGET_BIND({self}, {sequence}, {func}, {add}, **{kw})"
                " Called!".format(
                    self=self, sequence=sequence, func=func, add=add, kw=kw
                )
            )
        if sequence == func is None:
            return super().bind() if self.emulation_b else self.widget.bind()
        if func is None:
            return (
                super().bind(sequence)
                if self.emulation_b
                else self.widget.bind(sequence)
            )
        internal_b = kw.get("internal", True)
        kids_d = kw.get("kids", self._kids)
        kidsonly = kw.get("kidsonly", None)
        recurse_b = kw.get("recurse", False)
        release_b = kw.get("release", internal_b or not add)
        if not hasattr(self, "_funcids_d"):
            setattr(self, "_funcids_d", {})
        if sequence not in self._funcids_d:
            self._funcids_d[sequence] = {}
        if release_b:
            self._widget_unbind(sequence, True, func=func, add=add, **kw)
        if kidsonly:
            func_id = kidsonly  # from dict
            func_ids = [
                func_id,
            ]
        else:
            if self.emulation_b:
                func_id = super().bind(sequence, func, "+")
            else:
                func_id = self.widget.bind(sequence, func, "+")
            self._funcids_d[sequence][func_id] = dict(
                sequence=sequence,
                func=func,
                add=add,
                internal=internal_b,
                self=func_id,
                kids={},
                frames={},
            )
            func_ids = [
                func_id,
            ]
        for frame in [
                getattr(self, "_compoundframe", None),
                getattr(self, "_textframe", None),
        ] + getattr(self, "_subframes", []):
            if frame and frame.winfo_exists():
                fid = frame.bind(sequence, func, "+")
                frame_str = str(frame)
                self._funcids_d[sequence][func_id]["frames"][frame_str] = fid
                func_ids.append(fid)
        matching_recursion_events = (
            e
            for e in self.event_types_requiring_recursion
            if e.startswith(sequence[1:])
        )
        recursion_b = (
            recurse_b or matching_recursion_events or not internal_b and False
        )
        if recursion_b or kidsonly:
            for child_str, vals in kids_d.items():
                child = vals["label"]
                if debug_b:
                    self._print(
                        "BINDING {sequence} to Child={child}: Child.bind("
                        "{sequence}, {func}, {add}, **{kw})".format(
                            child=child,
                            sequence=sequence,
                            func=func,
                            add=add,
                            kw=kw,
                        )
                    )
                # try:
                if kidsonly:
                    cfid = self._funcids_d[sequence][func_id]["kids"].get(
                        child_str
                    )
                    if cfid:
                        child.unbind(sequence, cfid)
                child_func_id = child.bind(sequence, func, "+")
                self._funcids_d[sequence][func_id]["kids"][
                    child_str
                ] = child_func_id
                func_ids.append(child_func_id)
                # except:  # else: #
                    # self._print(
                    #     "EXCEPTION while Binding Child({c}, {s}, {f}, {ad})"
                    #     "".format(
                    #         c=child, s=sequence, f=func, ad=add
                    #     )
                    # )
        result = func_ids if internal_b else func_ids[0]
        if debug_b:
            self._print(
                "FUNC_IDS are ", func_ids, " internal_b is ", internal_b
            )
        return result

    def _widget_cget(self, option, **kwargs):
        """Get config option info from the internal widget used to keep
        state.
        """
        cook_b = kwargs.get("cook", True)
        default_b = kwargs.get(default_s, False)
        if default_b:
            value = self.widget.config(option)[-2]
            return value
        try:  # if True: #
            value = self.widget.cget(option)
        except tk.TclError:  # else: #
            value = None
        if cook_b:
            # <border object: >
            if option in (
                    activebackground_s,
                    background_s,
                    font_s,
                    highlightbackground_s,
            ):
                value = str(value)
            # <color object: >
            elif option in (
                    activeforeground_s,
                    disabledforeground_s,
                    foreground_s,
                    highlightcolor_s,
            ):
                value = str(value)
            # <font object: >
            elif option in (font_s,):
                value = str(value)
            # <index object: >
            elif option in (
                    anchor_s,
                    compound_s,
                    default_s,
                    justify_s,
                    relief_s,
                    state_s,
            ):
                value = str(value)
            # <pixel object: >
            elif option in (
                    borderwidth_s,
                    highlightthickness_s,
                    padx_s,
                    pady_s,
                    wraplength_s,
            ):
                value = str(value)
            # int
            elif option in (
                    height_s,
                    repeatinterval_s,
                    repeatdelay_s,
                    underline_s,
                    width_s,
            ):
                value = int(value)
            # str
            elif option in (
                    bitmap_s,
                    command_s,
                    cursor_s,
                    image_s,
                    overrelief_s,
                    takefocus_s,
                    text_s,
                    textvariable_s,
            ):
                if option == command_s:
                    if self.command:
                        value = self.command
                    elif "<lambda>" not in value:
                        value = eval(value.lstrip(string.digits))
                    else:
                        value = "<lambda>"  # NotImplemented #
                elif option == textvariable_s:
                    if self.textvariable:
                        value = self.textvariable
                    elif value:
                        try:
                            value = eval(str(value))
                        except NameError:
                            pass
                else:
                    value = str(value)
            else:
                pass
        return value

    def _widget_config(self, option=None, value=sentinel, **kwargs):
        """Config option info for the internal widget used to keep state."""
        cget_b = kwargs.pop("cget", False)
        _ = kwargs.pop("pared", False)  # UNUSED pared_b
        success_i = 0
        if option and value != sentinel:
            kwargs[option] = value
        count_i = len(kwargs)
        for opt, val in kwargs.items():
            try:  # if True: #
                self.widget.config(**{opt: val})
                success_i += 1
            except NameError:  # else: #
                self._print(
                    "EXCEPTION While Configuring {o} with {v}".format(
                        o=opt, v=val
                    ),
                    Raise=True,
                )
            except tk.TclError:  # else: #
                self._print(
                    "EXCEPTION While Configuring {o} with {v}".format(
                        o=opt, v=val
                    ),
                    Raise=True,
                )
        if value == sentinel:
            config_d = self.widget.config()
            if not option:
                results = config_d
            elif option in config_d:
                results = config_d[option][-1] if cget_b else config_d[option]
            else:
                self._print(
                    "EXCEPTION: Option {o} Not Found in Widget".format(
                        o=option
                    ),
                    Raise=True,
                )
            return results
        return success_i == count_i

    def _widget_rebind_externals(self, **kw):
        """Rebind any bindings that existed before the child widgets were
        created.
        """
        if not hasattr(self, "_funcids_d"):
            setattr(self, "_funcids_d", {})
        values_l = self._funcids_d.values()  # bypasses seqs
        events_l = (list(v.values())[0] for v in values_l)
        external_events_l = (
            e for e in events_l if e.get("internal") is False
        )  # == 0)
        for e in external_events_l:
            self._widget_bind(
                e["sequence"],
                e["func"],
                e["add"],
                internal=e["internal"],
                kidsonly=e["self"],
                **kw
            )

    def _widget_unbind(self, sequence, funcid=None, **kw):
        """Unbind the requested sequence and update internal state."""
        # add = kw.get("add", sentinel)  # UNUSED
        debug_b = kw.get("debug", self.default_debug)
        # we can tell by this if called from  _w_bind
        # func = kw.get("func", sentinel)  # UNUSED
        internal_b = kw.get("internal", True)
        # kids_d = kw.get("kids", self._kids)  # UNUSED
        # kidsonly_b = kw.get("kidsonly", False)  # UNUSED
        recurse_b = kw.get("recurse", False)
        if debug_b:
            self._print(
                "_WIDGET_UNBIND({self}, {s}, {f}, **{kw})".format(
                    self=self, s=sequence, f=funcid, kw=kw
                )
            )
        if not hasattr(self, "_funcids_d"):
            setattr(self, "_funcids_d", {})
        x_funcids = ()
        seq_funcids_d = self._funcids_d.get(sequence)
        if seq_funcids_d:
            funcids = [
                fid
                for fid in seq_funcids_d.keys()
                if seq_funcids_d[fid].get("internal") == internal_b
            ]
            if funcid is True:
                if internal_b:
                    if len(funcids) > 1:
                        raise Exception(
                            "Failure Trying to Find Internal FuncID for"
                            " Sequence {sequence}. Got {funcids}".format(
                                sequence=sequence, funcids=funcids
                            )
                        )
                    funcid = funcids[0] if funcids else None
            if funcid is True:
                pass
            elif funcid:
                x_funcids = (funcid,)
            else:
                x_funcids = funcids
            for fid in x_funcids:
                if fid:
                    try:
                        if self.emulation_b:
                            super().unbind(sequence, fid)
                        else:
                            self.widget.unbind(sequence, fid)
                    except TypeError:
                        self._print(
                            "EXCEPTION for unbind(sequence={sequence},"
                            " funcid={fid})".format(
                                sequence=sequence, fid=fid
                            ),
                            Raise=True,
                        )
                d = seq_funcids_d.pop(fid)
                # self.widget.unbind(sequence, func)
                kids = d.get("kids", {})
                if recurse_b or kids:
                    for child_str in kids:
                        cfid = kids[child_str]
                        child = self._valid_widget(child_str)
                        if debug_b:
                            self._print(
                                "SELF is ", self,
                                ", CHILD_STR is ", child_str,
                                ", CHILD is ", child,
                                ", CFID is ", cfid,
                            )
                            self._print(
                                "_UNBINDING Child: child={child}, seq="
                                "{sequence}, funcid={cfid})".format(
                                    child=child_str,
                                    sequence=sequence,
                                    cfid=cfid,
                                )
                            )
                        if child and cfid and child.winfo_exists():
                            child.unbind(sequence, cfid)
        return x_funcids

    @staticmethod
    def alias(option=None):
        """See help on module method alias() for more info"""
        return alias(option)

    def bind(self, sequence=None, func=None, add=None):
        """Bind to this widget at event SEQUENCE a call to function FUNC.

        SEQUENCE is a string of concatenated event
        patterns. An event pattern is of the form
        <MODIFIER-MODIFIER-TYPE-DETAIL> where MODIFIER is one
        of Control, Mod2, M2, Shift, Mod3, M3, Lock, Mod4, M4,
        Button1, B1, Mod5, M5 Button2, B2, Meta, M, Button3,
        B3, Alt, Button4, B4, Double, Button5, B5 Triple,
        Mod1, M1. TYPE is one of Activate, Enter, Map,
        ButtonPress, Button, Expose, Motion, ButtonRelease
        FocusIn, MouseWheel, Circulate, FocusOut, Property,
        Colormap, Gravity Reparent, Configure, KeyPress, Key,
        Unmap, Deactivate, KeyRelease Visibility, Destroy,
        Leave and DETAIL is the button number for ButtonPress,
        ButtonRelease and DETAIL is the Keysym for KeyPress and
        KeyRelease. Examples are
        <Control-Button-1> for pressing Control and mouse button 1 or
        <Alt-A> for pressing A and the Alt key (KeyPress can be omitted).
        An event pattern can also be a virtual event of the form
        <<AString>> where AString can be arbitrary. This
        event can be generated by event_generate.
        If events are concatenated they must appear shortly
        after each other.

        FUNC will be called if the event sequence occurs with an
        instance of Event as argument. If the return value of FUNC is
        "break" no further bound function is invoked.

        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function.

        Bind will return an identifier to allow deletion of the bound function
        with unbind without memory leak.

        If FUNC or SEQUENCE is omitted the bound function or list
        of bound events are returned.
        """
        return self._widget_bind(sequence, func, add, internal=False)

    def bind_all(self, sequence=None, func=None, add=None):
        """Bind to all widgets at an event SEQUENCE a call to function FUNC.
        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function. See bind for the return value.
        """
        return super().bind_all(sequence, func, add)

    def bind_class(self, className, sequence=None, func=None, add=None):
        """Bind to widgets with bindtag CLASSNAME at event
        SEQUENCE a call of function FUNC. An additional
        boolean parameter ADD specifies whether FUNC will be
        called additionally to the other bound function or
        whether it will replace the previous function. See bind for
        the return value.
        """
        return super().bind_class(className, sequence, func, add)

    def cget(self, key):
        """Get Config option KEY."""
        return self._widget_cget(key, cook=False)

    def cget2(self, key, **kw):
        """Get Config option KEY, but with some preprocessing.

        This is like cget(), but better for 'textvariable' and 'command':
            'textvariable' - returns a usable StringVar.
            'command' - returns a callable function.
        """
        kw.update(cook=True)
        return self._widget_cget(key, **kw)

    def config(self, *args, cnf=None, **kwargs):  # cnf=None,
        """Configure resources of a widget.

        The values for resources are specified as keyword arguments. To get
        an overview about the allowed keyword arguments call the method keys().
        """
        # some for frame, some for children, some for both
        debug_b = kwargs.get("debug", self.default_debug)
        if cnf and isinstance(cnf, (dict, collections.OrderedDict)):
            kwargs.update(cnf)
        elif cnf is not None:
            args = (cnf,) + args
        if args:
            arg0 = args[0]  # .lower()
            arg0lower = arg0.lower() if type(arg0) is str else arg0
            arg1 = args[1] if len(args) > 1 else ()
            if arg0 in (
                    class_s,
                    TTWidget,
                    "TTWidget",
                    TTLabel,
                    "TTLabel",
                    TTButton,
                    "TTButton",
            ):
                if arg0 in (TTLabel, "TTLabel"):
                    cls = TTLabel
                elif arg0 in (TTButton, "TTButton"):
                    cls = TTButton
                else:
                    cls = TTWidget
                for opt, val in kwargs.items():
                    setattr(cls, opt, val)
                    if debug_b:
                        self._print(
                            "CONFIG Class %s SETTING %s to %r"
                            % (cls, opt, val),
                            getattr(cls, opt),
                        )
            elif arg0lower in (frame_s, "base"):
                return tk.Frame.config(self, **kwargs)
            elif arg0lower in ("compoundframe",):
                return self._compoundframe.config(self, **kwargs)
            elif arg0lower in ("textframe",):
                return self._textframe.config(self, **kwargs)
            elif arg0lower in ("subframes", "subbase"):  # button_s, label_s,
                results = []
                _subframes = (
                    (
                        self._subframes[i]
                        for i in arg1
                        if i < len(self._subframes)
                    )
                    if arg1
                    else self._subframes
                )
                for f in _subframes:
                    results.append(f.config(**kwargs))
                return results
            elif arg0lower in ("widget", ):  # button_s, label_s,
                return self._widget_config(**kwargs)
            elif arg0lower in ("child", "kid"):
                results = []
                _get_kids = self._get_kids()
                _kids = (
                    (_get_kids[i] for i in arg1 if i < len(_get_kids))
                    if arg1
                    else _get_kids
                )
                for child in _kids:
                    results.append(child.config(**kwargs))
                return results
            elif arg0lower in self._widget_config().keys():
                return self._widget_config(arg0lower)
            else:
                self._print(
                    "EXCEPTION: Config Arg {0} Not Supported".format(arg0),
                    Raise=True,
                )
            if (
                    len(args) > 2
                    or len(args) > 1
                    and arg0lower not in (
                        "subframes",
                        "subbase",
                        "child",
                        "kid",
                    )
            ):
                self._print(
                    "EXCEPTION: Config Args {0} Ignored".format(args[1:]),
                    Raise=True,
                )
        abstain_b = kwargs.pop("abstain", False)
        debug_b = kwargs.pop("debug", self.default_debug)
        _ = kwargs.pop("init", False)  # init_b UNUSED
        pared_b = kwargs.pop("pared", False)
        propagate_b = kwargs.pop("propagate", True)
        store_b = kwargs.pop("store", True)
        procreate_b = False
        if not args and kwargs:
            for (key, val) in kwargs.items():
                if key in self.widget_option_aliases_d:
                    key = self.widget_option_aliases_d[key]
                if key == "default_debug":
                    self._set_default_debug(val)
                    continue
                if key in ttfont_dict_keys:
                    fkey = (
                        key[1:]
                        if key in (funderline_s, foverstrike_s)
                        else key
                    )
                    self.font_d[fkey] = val
                    if store_b:
                        fontnm = self._widget_cget(font_s)
                        newfontnm = get_named_font(fontnm, **{fkey: val})
                        if fontnm != newfontnm:
                            self.config(font=newfontnm)
                    continue
                self.options[key] = val
                if store_b:
                    if key in (case_s,):
                        setattr(self.widget, key, val)
                    else:
                        self._widget_config(**{key: val})
                if key in self.OPTIONS_NOT_IMPLEMENTED:
                    self._print(
                        "EXCEPTION: Widget Option {0} Not Implemented".format(
                            key
                        ),
                        Raise=True,
                    )
                elif key in (case_s,):
                    case_func = self._get_case_func(val)
                    if not self.emulation_b:
                        text = self.widget.text
                        self._widget_config(text=case_func(text))
                    for _name, gathering in self._get_kids(items=True):
                        child = gathering["label"]
                        text = gathering.get("text1", "")
                        if text.endswith("\n"):
                            text = text[:-1]
                        text = case_func(text)
                        gathering.update(case=val, text2=text)
                        self._child_config(
                            child, caller="config", **{text_s: text}
                        )
                elif key in self.widget_opts_req_procreation:
                    if key == compound_s:
                        pass
                    elif key in (bitmap_s, image_s):
                        pass
                    elif key == text_s:
                        pass
                    if not abstain_b:
                        self._kids = self._procreate()
                elif key in self.widget_opts_for_custom_impl:
                    if key == state_s:
                        if val == tk.NORMAL:
                            self._enable()
                        elif val == tk.DISABLED:
                            self._disable()
                        elif val == tk.ACTIVE:
                            self._activate()
                        elif val == default_s:
                            pass
                        else:
                            pass
                        self.__state = val
                    elif key == textvariable_s:
                        self.textvariable = textvariable = val
                        if self.observer and textvariable:
                            textvariable.trace_delete("w", self.observer)
                        self.observer = val.trace("w", self._trace_callback)
                    elif key == underline_s:
                        self._underline(val)  # post-procreation...
                    else:
                        pass
                elif key in self.opts_in_button_not_in_label:
                    if self.widget_class is not tk.Button:
                        continue
                    if debug_b:
                        self._print(
                            "SELF ", self, ", KEY=", key, ", VAL=", val
                        )
                    if key == command_s:
                        self.command = val
                    elif key == default_s:
                        # capture keybd focus and bind <Return> and <Space>
                        # to invoke()?"
                        self._indicate_default()
                        if val in (tk.NORMAL, tk.DISABLED):
                            pass
                        elif val in (tk.ACTIVE,):
                            pass
                        else:
                            pass
                    elif key in (
                            overrelief_s,
                            repeatdelay_s,
                            repeatinterval_s,
                    ):
                        pass
                elif key in self.opts_in_label_not_in_button:  # none
                    pass
                elif key in self.opts_in_frame_not_in_widget:
                    self._base_config(**{key: val})
                elif key in self.widget_opts_to_base_cfg:
                    self._base_config(**{key: val})
                elif key in self.widget_opts_to_base_pack:
                    self._base_pack[key] = val
                elif key in self.widget_opts_to_kids_cfg:
                    if key == font_s:
                        self.font_d = tk_font.Font(font=val).actual()
                    for child in self._get_kids():
                        self._child_config(
                            child, caller="config", **{key: val}
                        )
                elif key in self.widget_opts_to_kids_pack:
                    pass
                elif key in self.widget_opts_to_base_and_kids:
                    if key == anchor_s:
                        self._base_pack[key] = val
                    elif key == background_s:
                        self._base_config(**{key: val})
                    else:
                        pass
                    if propagate_b:
                        for child in self._get_kids():
                            self._child_config(
                                child, caller="config", **{key: val}
                            )
                else:
                    self._print(
                        "EXCEPTION: Unexpected Option {0}!".format(key),
                        Raise=True,
                    )
                # store_b and self._widget_config(**{key:val})
            if abstain_b and procreate_b:
                self._kids = self._procreate()
            return None
        return _flesh_config(self, self._widget_config(), pared=pared_b)

    def configure(self, *a, cnf=None, **kw):
        return self.config(*a, cnf, **kw)

    def dump(self, stringy="", **kwargs):
        """Dump the internal state of the compound widget, including parent
        Frame and child Labels.
        """
        count = kwargs.get("count", tk.END)
        stringy = kwargs.get("stringy", stringy)
        self._print("+" * 40)
        if stringy:
            self._print(stringy)
        self._print(
            "DUMPING:: SELF {s}, class {cls}, widget_class {wc}, index {i}"
            "".format(
                s=str(self),
                cls=self.__class__,
                wc=self.widget_class,
                i=self._index_,
            )
        )
        self._print(pprint.pformat(self))
        self._print(pprint.pformat(self._config_pared(self)))
        self._print("Text is {t!r}".format(t=self.strip_tags()))
        kids = self._get_kids(items=True)
        if count in (tk.END, tk.ALL):
            count = len(kids)
        self._print("Kid Count is {n}".format(n=len(kids)))
        for num, (_name, vals) in enumerate(kids):
            kid = vals["label"]
            self._print(
                "DUMPING:: KID[{n}]: {id} type={t!r}".format(
                    n=num, id=str(kid), t=vals["type"]
                )
            )
            self._print(pprint.pformat(kid))
            if num < count:
                self._print(pprint.pformat(self._config_pared(kid)))
        self._print("-" * 40)

    def flash(self, **kwargs):
        """Flash the Button/Label.

        This is accomplished by redisplaying the widget several times,
        alternating between active and normal colors. At the end of the flash
        the widget is left in the same normal/active state as when the command
        was invoked. This command is ignored if the widget's state is disabled.
        """
        alt_b = kwargs.get("alt", False)
        debug_b = kwargs.get("debug", self.default_debug)  # True) #
        times = kwargs.get("times", 1)
        wait = kwargs.get("wait", 100)
        if alt_b:
            relief = tk.Frame.config(self, relief_s)
            init_state = relief[4] if relief else None
            if debug_b:
                self._print("INIT STATE is %r" % init_state)
            for i in range(3):
                self.after(2 * i * wait, lambda: self.config(relief=tk.SUNKEN))
                self.after(
                    (2 * i + 1) * wait, lambda: self.config(relief=tk.RAISED)
                )
            if init_state != tk.RAISED:
                self.after(3 * wait, lambda: self.config(relief=init_state))
        else:
            init_state = self._widget_cget(state_s)
            if init_state != tk.DISABLED:
                flash_funcs = (
                    lambda: self._activate(store=False),
                    lambda: self._enable(store=False),
                )
                for i in range(times):
                    self.after(
                        (2 * i) * wait,
                        flash_funcs[0 if init_state == tk.NORMAL else 1],
                    )
                    self.after(
                        (2 * i + 1) * wait,
                        flash_funcs[1 if init_state == tk.NORMAL else 0],
                    )

    @classmethod
    def fromwidget(cls, widget, unmap_b=False, **kw):
        """Create a new TTWidget based on an existing WIDGET.

        Returns a new TTWidget based on the resources of WIDGET and optionally
        unmaps WIDGET.

        By default TTWidget creates an internal widget to store the state.
        This routine allows an existing widget to be passed in and used as the
        basis of a TTWidget."""
        unmap_b = kw.pop("unmap", unmap_b)
        obj = cls(None, widget, **kw)
        if unmap_b:
            unmap(widget)
        return obj

    @classmethod
    def fromwidgetclass(cls, widget_class, **kw):
        """Create a new TTWidget based on WIDGET_CLASS."""
        obj = cls(None, None, widget_class, **kw)
        return obj

    def gen_tag_attrs(self, *a, **kw):
        """See help on module method gen_tag_attrs() for more info"""
        return gen_tag_attrs(self, *a, **kw)

    @staticmethod
    def get_font_dict(*a, **kw):
        """See help on module method get_font_dict() for more info"""
        return get_font_dict(*a, **kw)

    @staticmethod
    def get_named_font(*a, **kw):
        """See help on module method get_named_font() for more info"""
        return get_named_font(*a, **kw)

    def invoke(self, **kwargs):
        """
        Invoke the command associated with the button.

        The return value is the return value from the command,
        or an empty string if there is no command associated with
        the button. This command is ignored if the button's state
        is disabled.
        """
        debug_b = kwargs.get("debug", self.default_debug)
        if debug_b:
            self._print("INVOKE(self={self})".format(self=self))
        if hasattr(self.widget, "invoke"):
            if debug_b:
                self._print("INVOKING...")
            return self.widget.invoke()
        return ""

    @staticmethod
    def is_tagged_text(*a, **kw):
        """See help on module method is_tagged_text() for more info"""
        return is_tagged_text(*a, **kw)

    def keys(self):
        """List all available widget options.

        Returns a list of all configurable widget resources.

        Note that all original Tkinter Label options are supported and
        new, custom TTWidgets options are added, namely:

            For FONT Attributes:

                family
                size
                slant
                weight
                bold
                italic
                funderline
                foverstrike

            For CASE Processing:

                case=[one of the below]
                    capitalize
                    upper
                    lower
                    title
                    swapcase
        """
        if self.widget:
            w_keys = self.widget.keys()
        else:
            w_keys = []
        return sorted(w_keys + list(ttfont_dict_keys) + [case_s])

    @staticmethod
    def pare_dict(*a, **kw):
        """See help on module method pare_dict() for more info"""
        return pare_dict(*a, **kw)

    def parse_tag_attrs(self, *a, **kw):
        """See help on module method parse_tag_attrs() for more info"""
        return parse_tag_attrs(*a, **kw)

    @staticmethod
    def convert_font_dict_to_ttoptions_dict(*a, **kw):
        """See help on module method convert_font_dict_to_ttoptions_dict() for
        more info.
        """
        return convert_font_dict_to_ttoptions_dict(*a, **kw)

    @staticmethod
    def convert_ttoptions_dict_to_font_dict(*a, **kw):
        """See help on module method convert_ttoptions_dict_to_font_dict()
        for more info.
        """
        return convert_ttoptions_dict_to_font_dict(*a, **kw)

    @staticmethod
    def quote(*a, **kw):
        """Ensure that any string S with white space is enclosed in quotes."""
        return quote(*a, **kw)

    @staticmethod
    def split_attrs(s, *a, **kw):
        """Split (an attributes) string S into elements, preserving quoted fields.

        Returns a list of strings.

        For example:
            split_attrs('family="Courier New" size=16 bold')
                yields:
            ['family="Courier New"', 'size=16', 'bold']
        """
        return split_attrs(s, *a, **kw)

    @staticmethod
    def split_chunk(chunk, *a, **kw):
        """Split a CHUNK of tagged text into the tag, attributes, and text.

        Returns a tuple of tag string, attributes string, and text string.

        Note that:
        - the 'tag' and 'attributes' strings may be empty if the CHUNK
          consists of only plain text,
        - the 'attributes' string may be empty if no attributes passed, and
        - the 'text' string may be empty.
        """
        return split_chunk(chunk, *a, **kw)

    @staticmethod
    def split_dict_into_options_fontattrs_and_case(*a, **kw):
        """See help on module method
        split_dict_into_options_fontattrs_and_case() for more info"""
        return split_dict_into_options_fontattrs_and_case(*a, **kw)

    @staticmethod
    def split_tagged_text_into_chunks(text, *a, **kw):
        """Split the tagged TEXT into separate chunks, each of which may be used to
        create a child widget.

        Returns a list of chunks, where each chunk includes:
        - an optional tag
        - optional attributes
        - optional text
        """
        return split_tagged_text_into_chunks(text, *a, **kw)

    def strip_tags(self, *a, **kw):
        """Strip away all tags from widget's text and return printable text.

        Returns a string without any tagging information.
        """
        return strip_tags(self._widget_cget(text_s), *a, **kw)

    @staticmethod
    def unalias(*a, **kw):
        """See help on module method unalias() for more info"""
        return unalias(*a, **kw)

    def unbind(self, sequence, funcid=None):
        """Unbind for this widget for event SEQUENCE the function identified
        with FUNCID.
        """
        return self._widget_unbind(sequence, funcid, internal=False)

    def unbind_all(self, sequence):
        """Unbind for all widgets for event SEQUENCE all functions."""
        return super().unbind_all(sequence)

    def unbind_class(self, className, sequence):
        """Unbind for all widgets with bindtag CLASSNAME for event SEQUENCE
        all functions."""
        return super().unbind_class(className, sequence)

    def unmap(self):
        """Unmap/hide the TTWidget."""
        return unmap(self)

    @staticmethod
    def unquote(s, *a, **kw):
        """Remove any enclosing quotes for S."""
        return quote(s, *a, **kw)

    def update_named_font(self, *a, **kw):
        """See help on module method update_named_font() for more info"""
        return update_named_font(*a, **kw)


class TTButton(TTWidget):
    """TTButton Class - inherits from TTWidget except for __init__().

    TTButton uses a Tkinter Button for internal state."""

    def __init__(self, master=None, widget=None, **options):
        super().__init__(master, widget, tk.Button, **options)


class TTLabel(TTWidget):
    """TTLabel Class - inherits from TTWidget except for __init__().

    TTLabel uses a Tkinter Label for internal state."""

    def __init__(self, master=None, widget=None, **options):
        super().__init__(master, widget, tk.Label, **options)


class TTListbox(tk.Listbox):
    """TTListbox is an interim pass at implementing multiple fonts for the
    Listbox widget. Although it does not support multiple fonts/labels yet,
    it uses the same tagged-text parsing functionality of TTWidget to allow
    the user to define all the items via the new 'text' option or insert
    tagged-text items and skip the step of calling itemconfig().

    Additionally, the extended Font and Case widget options are supported.
    """

    def __init__(self, *a, **kw):
        self.text = kw.pop(text_s, "")
        (
            self.options,
            self.font_d,
            self.case,
        ) = split_dict_into_options_fontattrs_and_case(kw)
        super().__init__(*a, **self.options)
        font_d = tk_font.Font(font=super().cget(font_s)).actual()
        self.font_d = _merge_dicts(font_d, self.font_d)
        ttoptions_d = convert_font_dict_to_ttoptions_dict(self.font_d)
        if self.case:
            ttoptions_d.update({case_s: self.case})
        for k, v in ttoptions_d.items():
            self.config(**{k: v, "store": True})  # False})
        if self.text:
            self._insert_new_elements()

    def _insert_new_elements(self, append_b=False, **kw):
        append_b = kw.pop("append", append_b)
        if not append_b:
            super().delete(0, tk.END)
        for chunk in split_tagged_text_into_chunks(self.text):
            self.insert(tk.END, chunk)

    @staticmethod
    def alias(option=None):
        """See help on module method alias() for more info"""
        return alias(option)

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        if key in (text_s, text_as):
            return self.text
        if key in ttfont_dict_keys:
            return self.font_d.get(key)
        if key in (case_s, case_as) or key in case_dict_keys:
            return self.case
        return super().cget(key)

    def config(self, cnf=None, **kw):
        """Configure resources of a widget.

        The values for resources are specified as keyword arguments. To get
        an overview about the allowed keyword arguments call the keys() method.
        """
        if cnf and isinstance(cnf, (dict, collections.OrderedDict)):
            kw.update(cnf)
            cnf = None
        elif cnf:
            return super().config(cnf)
        store_b = kw.pop("store", True)
        for k, v in kw.items():
            if k in (text_s, text_as):
                self.text = v
                if store_b:
                    self._insert_new_elements()
            elif k in (font_s, font_as):
                self.font_d = tk_font.Font(font=v).actual()
                super().config(**{k: v})
            elif k in ttfont_dict_keys:
                fkey = k[1:] if k in (funderline_s, foverstrike_s) else k
                self.font_d[fkey] = v
                if store_b:
                    fontnm = super().cget(font_s)
                    newfontnm = get_named_font(fontnm, **{fkey: v})
                    if fontnm != newfontnm:
                        super().config(font=newfontnm)
            elif k in (case_s, case_as):
                self.case = v
                if store_b:
                    case_func = _get_case_func(self.case)
                    for index in range(self.index(tk.END)):
                        txt = self.get(index)
                        mod_txt = case_func(txt)
                        if txt != mod_txt:
                            self.update_line_text(index, mod_txt)
            else:
                super().config(**{k: v})
        if kw:
            return None
        return _flesh_config(self, super().config())

    def configure(self, cnf=None, **kw):
        return self.config(cnf, **kw)

    def gen_tag_attrs(self, *a, **kw):
        """See help on module method gen_tag_attrs() for more info"""
        widget = kw.get("widget", sentinel)
        if widget not in (sentinel, None):
            raise Exception(
                "TTListbox.gen_tag_attrs(): unsupported 'widget' keyword "
                "value {w}".format(
                    w=widget
                )
            )
        kw["widget"] = None
        return gen_tag_attrs(None, *a, **kw)

    def insert(self, index, *elements, **kw):
        """Insert new tagged-text ELEMENTS at location INDEX."""
        # add support for tagged_text on input!
        if PyVers_f >= 3.4:
            index_i = super().index(index)
            super().insert(index, *elements)
            lb_elements = super().get(index_i, index_i + len(elements) - 1)
            for x, elem in enumerate(lb_elements, index_i):
                _, attrs, text = split_chunk(elem)
                if attrs:
                    opts, _, case = parse_tag_attrs(attrs, {}, {}, **kw)
                    if case:
                        text = getattr(text, case)()
                    super().insert(x, text)
                    super().itemconfig(x, **opts)
                    super().delete(x + 1)
        else:
            # bug in earlier Py versions causes above to fail on 1st elem
            elems_to_process = elements[:: 1 if index == tk.END else -1]
            for elem in elems_to_process:  # elements[::-1]:
                if type(elem) in (list, tuple):
                    elem1 = [
                        e.replace("{", r"\{").replace("}", r"\}") for e in elem
                    ]
                    elem2 = ["{%s}" % e if " " in e else e for e in elem1]
                    elem = " ".join(elem2)
                _, attrs, text = split_chunk(elem)
                if attrs:
                    opts, _, case = parse_tag_attrs(attrs, {}, {}, **kw)
                    if case:
                        text = getattr(text, case)()
                    super().insert(index, text)
                    super().itemconfig(index, **opts)
                else:
                    super().insert(index, text)

    def keys(self):
        """List all available widget options.

        Returns a list of all configurable widget resources.

        Note that all original Tkinter Listbox options are supported and
        new, custom TTWidgets options are added, namely:

            For Tagged-Text Processing:

                text

            For FONT Attributes:

                family
                size
                slant
                weight
                bold
                italic
                funderline
                foverstrike

            For CASE Processing:

                case=[one of the below]
                    capitalize
                    upper
                    lower
                    title
                    swapcase
        """
        return sorted(
            super().keys() + list(ttfont_dict_keys) + [text_s, case_s]
        )

    def parse_tag_attrs(self, *a, **kw):
        """See help on module method parse_tag_attrs() for more info"""
        return parse_tag_attrs(*a, **kw)

    @staticmethod
    def unalias(*a, **kw):
        """See help on module method unalias() for more info"""
        return unalias(*a, **kw)

    def update_line_text(self, index, text):
        """Update TEXT at INDEX while preserving color scheme info."""
        if index is not None:
            index = self.index(index)
            if index < self.index(tk.END):
                cfg = _get_pared_cfg(self.itemconfig(index))
                self.insert(index, text)
                self.itemconfig(index, **cfg)
                self.delete(index + 1)
                return True
        return False


class TTToolTip:
    """TTToolTip supports a multi-font, tagged-text ToolTip."""

    def __init__(self, widget=None, text="...", **kw):
        self.defaults_d = {
            background_s: "wheat",
            borderwidth_s: 1,
            justify_s: tk.LEFT,
            relief_s: tk.SOLID,
        }
        self.custom_defs = {
            "base": "",
            "delay": 500,
            ipadx_s: 2,
            ipady_s: 1,
            "offsetx": 2,
            "offsety": 2,
        }
        self.base = kw.pop(
            "base", self.custom_defs["base"]
        )  # ''/'widget' or 'mouse'/'cursor'
        self.delay = kw.pop("delay", self.custom_defs["delay"])  # ms
        self.ipadx = kw.pop(ipadx_s, self.custom_defs[ipadx_s])
        self.ipady = kw.pop(ipady_s, self.custom_defs[ipady_s])
        self.offsetx = kw.pop("offsetx", self.custom_defs["offsetx"])
        self.offsety = kw.pop("offsety", self.custom_defs["offsety"])
        self.widget = kw.pop("widget", widget)
        kw[text_s] = kw.get(text_s, text)
        options = _merge_dicts(self.defaults_d, kw)
        if self.widget:
            self.widget.bind("<Enter>", self._enter)
            self.widget.bind("<Leave>", self._leave)
            self.widget.bind("<ButtonPress>", self._leave)
            self.widget.bind(
                "<ButtonPress-{RMB}>".format(RMB=RMB), self._leave
            )
        self._aid = None
        self._top = tk.Toplevel(self.widget)
        self._top.withdraw()
        self.ttlabel = TTLabel(self._top, **options)
        self.ttlabel.pack(ipadx=self.ipadx, ipady=self.ipady)

    def _cancel(self):
        if self._aid:
            if self.widget:
                self.widget.after_cancel(self._aid)
            self._aid = None

    def _enter(self, event=None):
        self._schedule()

    def _hidetip(self):
        if self._top:
            self._top.withdraw()

    def _leave(self, event=None):
        self._cancel()
        self._hidetip()

    def _schedule(self):
        self._cancel()
        if self.widget:
            self._aid = self.widget.after(self.delay, self._showtip)

    def _showtip(self, event=None):
        if not self.widget:
            return
        self.widget.winfo_toplevel().update_idletasks()
        if self.base and self.base[:1] in ("mouse"[:1], cursor_s[:1]):
            x0 = self.widget.winfo_pointerx() + self.offsetx
            y0 = self.widget.winfo_pointery() + self.offsety
        else:
            x0 = (
                self.widget.winfo_rootx()
                + self.widget.winfo_width()
                - self.offsetx
            )
            y0 = (
                self.widget.winfo_rooty()
                + self.widget.winfo_height()
                - self.offsety
            )
        if self._top:
            self._top.deiconify()
            self._top.wm_overrideredirect(True)
            self._top.wm_geometry("+%d+%d" % (x0, y0))
            if Platform_s == "Darwin":
                try:
                    self._top.tk.call(
                        "::tk::unsupported::MacWindowStyle",
                        "style",
                        self._top._w,
                        "help",
                        "noActivates",
                    )
                except tk.TclError:
                    pass

    @staticmethod
    def alias(option=None):
        """See help on method alias()"""
        return alias(option)

    def cget(self, key):
        """Return the resource value for a KEY given as string."""
        result = None
        if key:
            if key in self.ttlabel.keys():
                result = self.ttlabel.cget(key)
            elif key in self.custom_defs:
                result = getattr(self, key, None)
            else:
                raise Exception("Unexpected Key {key}".format(key=key))
        return result

    def config(self, cnf=None, **kw):
        """Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about the allowed keyword
        arguments call the keys() method.
        """
        if cnf:
            kw.update(cnf)
        for k, v in kw.items():
            if k in self.ttlabel.keys():
                self.ttlabel.config(**{k: v})
            elif k in self.custom_defs:
                setattr(self, k, v)
            else:
                raise Exception(
                    "Unexpected Key/Val Pair {k}:{v}".format(k=k, v=v)
                )
        if not cnf and not kw:
            return _flesh_config(
                self,
                self.ttlabel.config(),
                defaults=self.defaults_d,
                base=("", self.base),
                delay=(500, self.delay),
                ipadx=(2, self.ipadx),
                ipady=(1, self.ipady),
                offsetx=(2, self.offsetx),
                offsety=(2, self.offsety),
            )
        return None

    def configure(self, cnf=None, **kw):
        """Configure resources of a widget."""
        return self.config(cnf, **kw)

    def gen_tag_attrs(self, *a, **kw):
        """See help on method gen_tag_attrs()"""
        if kw.get("widget", sentinel) is not None:
            raise Exception(
                "TTToolTip.gen_tag_attrs(): 'widget' keyword must be set"
                " to None"
            )
        return gen_tag_attrs(None, *a, **kw)

    def keys(self):
        """List all available widget options.

        Returns a list of all configurable widget resources.

        Note that all original Tkinter Label options are supported and
        new, custom TTWidgets options are added, namely:

            For FONT Attributes:

                family
                size
                slant
                weight
                bold
                italic
                funderline
                foverstrike

            For CASE Processing:

                case=[one of the below]
                    capitalize
                    upper
                    lower
                    title
                    swapcase
        """
        return sorted(self.ttlabel.keys() + list(self.custom_defs.keys()))

    def parse_tag_attrs(
            self, tags_str, options_d=None, font_d=None, case="", **kwargs
    ):
        """See help on method parse_tag_attrs()"""
        return parse_tag_attrs(
            tags_str,
            options_d,
            font_d,
            case,
            widget=self,
            text=getattr(self, "debug_text", None),
            **kwargs
        )

    @staticmethod
    def unalias(*a, **kw):
        """See help on method unalias()"""
        return unalias(*a, **kw)


Button = TTButton
Label = TTLabel
Listbox = TTListbox
ToolTip = TTToolTip
__init_widget_option_unaliases_d()

if __name__ == "__main__":

    def build_the_gui():
        """create the GUI"""
        root.title(
            "Multi-Font Widgets from "
            + __file__
            + " on Python "
            + str(PyVers_s)
        )
        debugText = tk_scrolledtext.ScrolledText(root, width=150, height=20)
        but_nums = (36, 38) + tuple(range(1, 35))  # 5, )) +
        but_opts = dict(
            activebackground="aqua",
            activeforeground="red",
            anchor=tk.CENTER,
            bd="6",  # 2
            disabledforeground="blue",
            highlightbackground="yellow",
            highlightcolor="orange",
            highlightthickness="4",
            justify=tk.CENTER,
            wraplength=0,
        )
        # padx=10, pady=10, #
        but_cfg_opts = but_opts.copy()
        but_pack_opts = dict(side=tk.LEFT, padx=2, pady=2)
        # , fill=tk.BOTH, expand=True{} # ) #
        frame_cfg_opts = dict(
            bg="wheat",
            borderwidth=str(2),
            relief=tk.GROOVE,
         )
        frame_pack_opts = dict(side=tk.TOP, fill=tk.BOTH, expand=True)
        lab_nums = (
            1,
            2,
        )
        lb_nums = (
            1,
            2,
        )
        post_config_b = True
        root.frame0 = frame0 = tk.Frame(root, **frame_cfg_opts)
        frame0.pack(fill=tk.X, expand=True)
        reg_but = tk.Button(
            frame0,
            text="Regular Button\nCycle All States",
            command=lambda *a: (
                [cycle_but_state(i) for i in but_nums],
                print("Regular Button Release", *a),
            ),
            overrelief=tk.GROOVE,
            bg="cyan",
            **but_opts
        )
        reg_but.pack(side=tk.LEFT)
        root.top = tk.Toplevel()
        root.top.withdraw()
        tt1 = TTToolTip(
            reg_but,
            text="My <t bg=cyan px=2 py=2 bd=2 relief=groove size=6 "
                 "wraplength=70>Regular Button Cycle All States</t><t b> "
                 "ToolTip</t>... See how it matches? :)",
            bg="white",
            relief=tk.GROOVE,
            borderwidth=5,
            base="cursor",
        )
        print(tt1, dir(tt1))
        root.after(10000, lambda *a: tt1.config(bg="yellow"))
        TTButton.default_debug = False  # True #
        BITMAP = """
        #define im_width 32
        #define im_height 32
        static char im_bits[] = {
        0xaf,0x6d,0xeb,0xd6,0x55,0xdb,0xb6,0x2f,
        0xaf,0xaa,0x6a,0x6d,0x55,0x7b,0xd7,0x1b,
        0xad,0xd6,0xb5,0xae,0xad,0x55,0x6f,0x05,
        0xad,0xba,0xab,0xd6,0xaa,0xd5,0x5f,0x93,
        0xad,0x76,0x7d,0x67,0x5a,0xd5,0xd7,0xa3,
        0xad,0xbd,0xfe,0xea,0x5a,0xab,0x69,0xb3,
        0xad,0x55,0xde,0xd8,0x2e,0x2b,0xb5,0x6a,
        0x69,0x4b,0x3f,0xb4,0x9e,0x92,0xb5,0xed,
        0xd5,0xca,0x9c,0xb4,0x5a,0xa1,0x2a,0x6d,
        0xad,0x6c,0x5f,0xda,0x2c,0x91,0xbb,0xf6,
        0xad,0xaa,0x96,0xaa,0x5a,0xca,0x9d,0xfe,
        0x2c,0xa5,0x2a,0xd3,0x9a,0x8a,0x4f,0xfd,
        0x2c,0x25,0x4a,0x6b,0x4d,0x45,0x9f,0xba,
        0x1a,0xaa,0x7a,0xb5,0xaa,0x44,0x6b,0x5b,
        0x1a,0x55,0xfd,0x5e,0x4e,0xa2,0x6b,0x59,
        0x9a,0xa4,0xde,0x4a,0x4a,0xd2,0xf5,0xaa
        };
        """
        root.image = {}
        root.widgets = []
        root.buttons = collections.OrderedDict()
        # natives: 6, 14, 16, 22, 28
        num = iter(range(1, 100))
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 1, 2,
            if idx in but_nums:
                text = (
                    "%d: <t siz=10 B=1>Size 10 bold</t><t siz=6>Size 6\nNew"
                    " Line </t><t u wei=bold>Underlined and Bolded\n</t>"
                    "<t it>Italics</t><t>default</t> Nada <t fg=red u "
                    "bg=yellow>red on yellow </t><t>default\n</t><t fam=Arial"
                    " siz=18>Arial 18</t>\n<t fam='Courier New' siz=18>"
                    "Courier 18</t>\nI'm Right-clickable... Try me!!!\n"
                    " Anchor=West" % idx
                )
                root.buttons[idx] = but = cls(
                    root,
                    text=text,
                    command=lambda i=idx: example_method(i),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                but.bind(
                    "<Button-%d>" % RMB,
                    lambda e=None, i=idx, *a: print(
                        "RIGHT-CLICKED on %d!" % i, *a
                    ),
                )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 3, 4,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    text="%d: e<t fg=blue u low>xam</t>ple 2000\nR Justify,"
                         " C Anchor......." % idx,
                    command=lambda i=idx: example_method(i),
                    repeatdelay=2000,
                    **but_cfg_opts
                )  #
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 5, 6,
            tfont = tk_font.Font(font=("Courier", 36))
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    text="<t fg=green b font=%s tit>%d: example 2000/500\n"
                         "cursor=hand2</t>" % (tfont, idx),
                    command=lambda i=idx: example_method(i),
                    repeatdelay=2000,
                    repeatinterval=500,
                    cursor="hand2",
                    **but_cfg_opts
                )
                # font=('Courier', 36),
                root.widgets.append(but)
                but.idx = idx
                # but.font = tfont
                if isinstance(but, TTWidget):
                    root.after(2000, lambda b=but, *a: b.config(case="upper"))
                    root.after(4000, lambda b=but, *a: b.config(case=""))
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 7, 8,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    text="idx: one<t tit>two\nthree</t><t cap>four</t>"
                         "OR=Groove, flash on click\nAFG/ABG=blue/yellow\n"
                         " SW Anchor, L Justify",
                    command=lambda i=idx: example_method(i),
                    overrelief=tk.GROOVE,
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 9, 10,
            sv.set(value="X: SV:\npress to <t b>change</t>")
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    textvariable=sv,
                    command=lambda i=idx: example_method(i),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                but.bind(
                    "<Button-%d>" % RMB,
                    lambda e=None, i=idx, *a: print(
                        ">>>>>>>>>> RIGHT-CLICKED on %d!" % i, *a
                    ),
                )
                root.after(10000, lambda i=idx, b=but: b.config(bg="white"))
            if post_config_b:
                root.after(
                    5000,
                    lambda i=idx: sv.set(
                        "%d: Five Seconds\n<t bg=yellow fg=red b i u>Later!\n"
                        "red on yellow now,\nwhite bg in 5 secs...</t>" % i
                    ),
                )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 11, 12,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    command=lambda i=idx: cycle_but_state(i - 4),
                    underline=0,
                    text="%d: <t cas=tit>cycle but%d state</t> <t bg=cyan>"
                         "Cyan</t> (active=red/yellow)" % (idx, idx - 4),
                    bg="wheat",
                    **but_cfg_opts
                )  # -1)
                root.widgets.append(but)
                but.idx = idx
                if post_config_b:
                    root.after(
                        4000,
                        lambda i=idx, b=but: b.config(
                            underline=21,
                            text="%d: <t tit>cycle but%d state</t> <t bg="
                            "green>Green (updated)</t> (active=red/yellow)"
                            % (i, i - 4),
                        ),
                    )
                    root.after(
                        8000,
                        lambda i=idx, b=but: b.config(underline=3, bg="white"),
                    )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 13, 14,
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 15, 16,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    text="%d: TTButton\n" % idx + '"ButtonRelease-%d"' % RMB,
                    bg="wheat",
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 17, 18,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    text="%d: TTButton normal now, anchored East, <t relief="
                         "groove bd=2>active</t> in 5 secs...\n" % idx,
                    bg="wheat",
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                if post_config_b:
                    if cls == TTButton:
                        but.config(frame_s, bg="green")
                        but.config("child", (1,), bg="cyan")
                    root.after(
                        5000, lambda i=idx, b=but: b.config(default=tk.ACTIVE)
                    )
                    root.after(
                        10000,
                        lambda i=idx, b=but: b.config(
                            default=tk.NORMAL,
                            text="%d: <t case=title>NORMAL </t><t case=upper>"
                                 "again!</t>" % i,
                        ),
                    )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 19, 20,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    font=("Courier", 24),
                    text="%d: font is Courier 24\n<t fg=green bg=cyan "
                         "size=12>Green on Cyan size 12</t><t fam=Arial "
                         "fg=brown i=0>\nBrown Arial no Size</t>" % idx,
                    bg="wheat",
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                root.after(
                    2000,
                    lambda i=idx, b=but: b.config(bg="white", fg="magenta"),
                )
                if post_config_b:
                    root.after(
                        4000,
                        lambda i=idx, b=but: b.config(
                            font=("Times", 8, "italic bold")
                        ),
                    )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 21, 22,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    bitmap="question",
                    text="%d: Text on the Top" % idx,
                    compound=tk.NONE,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 23, 24,
            if idx in but_nums:
                text = (
                    "%d: Bitmap on the Top, bitmap <t bitmap=question>"
                    "Question</t> and <t bitmap=info>Info</t>" % idx
                )
                root.buttons[idx] = but = cls(
                    root,
                    text=text,
                    bitmap="error",
                    compound=tk.TOP,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )  #
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 25, 26,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print("IMAGE %d is " % idx, image)
                compound = tk.LEFT
                root.buttons[idx] = but = cls(
                    root,
                    image=image,
                    text="%d: <t fg=green>graphic location: %s</t>"
                    % (idx, compound),
                    fg="red",
                    bg="cyan",
                    compound=compound,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 27, 28,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print("IMAGE %d is " % idx, image)
                root.buttons[idx] = but = cls(
                    root,
                    text="<t image=%s>%d: Text on the Top</t>" % (image, idx),
                    fg="red",
                    bg="cyan",
                    compound=tk.CENTER,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 29, 30,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print("IMAGE %d is " % idx, image)
                root.buttons[idx] = but = cls(
                    root,
                    text="%d: Text <t image=%s>on the</t> Top" % (idx, image,),
                    fg="red",
                    bg="cyan",
                    compound=tk.CENTER,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 31, 32,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print("IMAGE %d is " % idx, image)
                root.buttons[idx] = but = cls(
                    root,
                    image=image,
                    compound=tk.LEFT,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        delay_time, loops = 2000, 1
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 33, 34,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print("IMAGE %d is " % idx, image)
                root.buttons[idx] = but = cls(
                    root,
                    image=image,
                    compound=tk.LEFT,
                    text="Simple Text",
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                for x in range(loops):
                    root.after(
                        (2 * x + 1) * delay_time,
                        lambda b=but, *a: b.config(
                            text="<t bg=red>Red </t><t bg=blue>Blue</t>"
                                 "<t bitmap=question>question</t>"
                        ),
                    )
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 35, 36,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    compound=tk.LEFT,
                    text="<t>Simple</t> Text",
                    fg="red",
                    funderline=1,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in (
                (next(num), tk.Button),
                (next(num), TTButton),
        ):  # 37, 38,
            if idx in but_nums:
                root.buttons[idx] = but = cls(
                    root,
                    compound=tk.LEFT,
                    text="<t>Simple</t> Text",
                    fg="red",
                    slant=tk_font.ITALIC,
                    foverstrike=1,
                    command=lambda i=idx, *a: print(
                        "BUTTON %d COMMAND!" % i, *a
                    ),
                    **but_cfg_opts
                )
                root.widgets.append(but)
                but.idx = idx
                if idx == 38:
                    root.after(
                        3000,
                        lambda e=None, b=but, i=idx: b.config(
                            text="<t bg=magenta>3 secs...</t>magenta bg"
                        ),
                    )
                    root.after(
                        6000,
                        lambda e=None, b=but, i=idx: b.config(
                            funderline=1, foverstrike=0, bg="cyan"
                        ),
                    )
                print("BUTTON %d: KEYS: " % idx, but.keys())
                print("BUTTON %d: CONFIG: " % idx, but.config())
        if 1 in lab_nums:
            root.lab1 = tk.Label(
                root,
                text="%s %d: Normal Label\nFor 13: in 6 secs, bg=white, "
                     "fg=magenta\nin 8 secs, Educate\nin 10 secs, "
                     "font=Arial,48\nin 12 secs, Educate" % (tk.Label, 1),
            )
            root.widgets.append(root.lab1)
            root.lab1.idx = "L1"
        if 2 in lab_nums:
            root.lab2 = TTLabel(
                root,
                text="%s %d: <t b>Titled</t> Text <t tit>hi there</t>\nCustom"
                     " Label" % (TTLabel, 2),
            )
            root.widgets.append(root.lab2)
            root.lab2.idx = "L2"
        if 1 in lb_nums:
            root.lb1 = lb1 = TTListbox(
                root, font=("Courier", 12), height=4, width=24
            )
            lb1.insert(tk.END, "<t fg=red case=up>red upper</t>")
            lb1.insert(tk.END, "plain/normal")
            lb1.insert(
                tk.END,
                "<t fg=green bg=yellow>green on yellow</t>",
                "<t fg=magenta sfg=cyan case=tit>magenta (cyan selected)"
                " titled</t>",
            )
            print("\nLB1: KEYS: ", lb1.keys())
            print("LB1: CONFIG:", lb1.config())
            root.widgets.append(root.lb1)
            root.lb1.idx = "LB1"
            tt = TTToolTip(
                widget=lb1,
                text="This was via inserting tagged text,\nwith base=cursor",
                base=cursor_s,
            )
            print("\nTT KEYS: ", tt.keys())
            print("TT CONFIG: ", tt.config())
        if 2 in lb_nums:
            root.lb2 = lb2 = TTListbox(
                root,
                font=("Courier", 12),
                height=4,
                width=24,
                text="<t fg=red case=up>red upper</t>plain/normal<t fg=green"
                     " bg=yellow>green on yellow</t><t fg=magenta sfg=cyan"
                     " case=tit>magenta (cyan selected) titled</t>",
                foverstrike=1,
            )
            root.widgets.append(root.lb2)
            root.lb2.idx = "LB2"
            TTToolTip(
                lb2,
                "This was via text attribute assigned tagged "
                + "text,\nwith default base=widget",
            )
            root.after(
                2000, lambda *a: lb2.config(case="upper", foverstrike=0)
            )
        root.update_idletasks()
        width = 6  # 8 #
        index = 0
        root.frames = []
        for child in root.winfo_children():
            if (
                    isinstance(child, TTWidget)
                    and not child.winfo_ismapped()
                    or hasattr(child, "idx")
            ):
                if index % width == 0:
                    root.frames.append(
                        tk.Frame(
                            root,
                           **frame_cfg_opts
                        )
                    )
                    root.frames[-1].pack(**frame_pack_opts)
                    root.frames[-1].lower()
                child.pack(in_=root.frames[-1], **but_pack_opts)
                if isinstance(child, TTListbox):
                    pass
                elif not isinstance(child, TTWidget):
                    try:
                        text = child.cget(text_s)
                        child.config(text=strip_tags(text))
                    except KeyError:
                        print(
                            "EXCEPTION Configuring %s %s"
                            % (type(child), child)
                        )
                index += 1
            else:
                print(
                    "SKIPPING {0!r} ({1}): {2}".format(
                        child,
                        child.__class__,
                        "NOT a TTWidget"
                        if not isinstance(child, TTWidget)
                        else "already mapped"
                        if child.winfo_ismapped()
                        else "because...",
                    )
                )
        fmt1 = gen_tag_attrs(
            options=dict(family="Courier", size=4, fun=True, ul=2, bg="yellow")
        )
        print("FMT1 is %r" % fmt1)
        debugText.pack(fill=tk.BOTH, expand=True)
        for bn in but_nums:
            but = root.buttons.get(bn)
            if but:
                but.bind(
                    "<ButtonRelease-3>",
                    lambda e=None, b=but, *a: print("\n", *a),
                    "+",
                )
                if isinstance(but, TTWidget):
                    fmt = but.gen_tag_attrs()
                else:
                    fmt = "(N/A)"
                print("FMT  for but is", pprint.pformat(fmt))
                print("TEXT for but is %r" % but.cget(text_s))

    def cycle_but_state(num):
        """Cycle a Button through all three states."""
        states = (tk.DISABLED, tk.NORMAL, tk.ACTIVE)
        but = root.buttons[num]
        state = but.cget(state_s)
        index = states.index(state)
        new_state = states[(index + 1) % len(states)]
        but.config(state=new_state)
        print("BUT %d STATE is " % num, new_state.upper(), ", was ", state)
        if isinstance(but, TTButton):
            print("BUT %d DUMP():" % num, but.dump())
        else:
            print("BUT %d CONFIG():" % num, but.config())

    def example_method(num=-1):
        """Print message when button is released."""
        print("BUTTON %d COMMAND!" % num)
        # button = root.buttons[num]  # UNUSED

    root = tk.Tk()
    sv = tk.StringVar(name="sv")
    build_the_gui()
    print(
        split_attrs(
            """family="Courier New" """
            + """family='Times  New   Roman' size=12 upper"""
        )
    )
    print(strip_tags("""one <t b>bold</t>"""))
    text_str = "one\n\ntwo<t cap>Capital Letters</t><t bitmap=question></t>"
    # <t fg="red" tit>Red\nBurn\n</t>\n
    chunks1 = split_tagged_text_into_chunks(text_str)
    print("TEXT is ", text_str, ", TEXT CHUNKS is ", chunks1)
    divisions = [split_chunk(ch) for ch in chunks1]
    print("DIVISIONS are ", divisions)
    wrapped = wrap_tagged_text(text_str, 5)
    print(
        "MATCH? ",
        wrapped == text_str,
        "\n",
        repr(text_str),
        "\n",
        repr(wrapped),
    )
    text1 = (
        "<tag fg=red>red</tag> and <tag bg=blue>blue</tag>"
        + "<tag bitmap=question /><tag bitmap=info></tag>"
    )
    print("CHUNKS: ", split_tagged_text_into_chunks(text1))
    print(
        "SPLIT CHUNKS:",
        [split_chunk(chunk) for chunk in split_tagged_text_into_chunks(text1)],
    )
    root.mainloop()
