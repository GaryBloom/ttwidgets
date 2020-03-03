"""
   Copyright 2020 Gary Michael Bloom
                  mailto:bloominator@hotmail.com

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

'''
demo.py
===================

This gives a quick demo of the ttwidgets package, which improves a subset of Tkinter widgets (Button, Label, 
Listbox), and provides a bonus ToolTip widget, with support for multiple
fonts and visual schemes.

The standard Tkinter Button and Label widgets are limited to a single set
of widget options (such as background/bg, foreground/fg, bitmap, cursor,
relief, etc), including a single font. With the TTWidgets enhancements,
Tagged Text can be passed in as text to create a compound widget (with
multiple fonts and visual option sets) that behaves like a simple widget.

The Button and Label implementations are complete.
The Listbox implementation is partial: the user can skip the secondary 
itemconfig() step by passing in the supported config options via Tagged 
Text.  A full multi-font implementation of a Tagged-Text Listbox may come 
later.
As a bonus, a ToolTip widget is included, which also accepts Tagged Text
as input, allowing the creation of colorful and multi-font ToolTips.

For an overview of Tagged Text, please see the TTWidget help.
'''

from ttwidgets import *
import tkinter as tk
from tkinter import font as tk_font
from tkinter import scrolledtext as tk_scrolledtext
import collections

if __name__ == '__main__':

    def build_the_gui(root):
        root.title('Multi-Font Widgets from ' + __file__ + ' on Python ' + str(PyVers_s))
        debugText = tk_scrolledtext.ScrolledText(root, width=150, height=20)
        but_nums = (36, 38) + tuple(range(1, 35)) # 5, )) +
        but_opts = dict(activebackground='yellow', activeforeground='red', anchor=tk.CENTER, bd=2, disabledforeground='blue', justify=tk.CENTER, wraplength=0, ) 
        # padx=10, pady=10, #
        but_cfg_opts = but_opts.copy()
        but_pack_opts = dict(side=tk.LEFT, padx=2, pady=2)
        # , fill=tk.BOTH, expand=True{} # ) #
        frame_pack_opts = dict(side=tk.TOP, fill=tk.BOTH, expand=True)
        lab_nums = (1, 2, )
        lb_nums = (1, 2, )
        post_config_b = True
        root.frame0 = frame0 = tk.Frame(root)
        frame0.pack(fill=tk.X, expand=True)
        reg_but = tk.Button(frame0, text='Regular Button\nCycle All States', command=lambda *a: ([cycle_but_state(i) for i in but_nums], print("Regular Button Release", *a), ), overrelief=tk.GROOVE, bg='cyan', **but_opts)
        reg_but.pack(side=tk.LEFT)
        root.top = tk.Toplevel()
        root.top.withdraw()
        tt1 = TTToolTip(reg_but, text='My <t bg=cyan px=2 py=2 bd=2 relief=groove size=6 wraplength=70>Regular Button Cycle All States</t><t b> ToolTip</t>... See how it matches? :)', bg='white', relief=tk.GROOVE, borderwidth=5, base='cursor')
        print(tt1, dir(tt1))
        root.after(10000, lambda *a: tt1.config(bg='yellow'))
        TTButton.default_debug = False # True #
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
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 1, 2,
            if idx in but_nums:
                text = "%d: <t siz=10 B=1>Size 10 bold</t><t siz=6>Size 6\nNew Line </t><t u wei=bold>Underlined and Bolded\n</t><t it>Italics</t><t>default</t> Nada <t fg=red u bg=yellow>red on yellow </t><t>default\n</t><t fam=Arial siz=18>Arial 18</t>\n<t fam='Courier New' siz=18>Courier 18</t>\nI'm Right-clickable... Try me!!!\n Anchor=West" % idx
                root.buttons[idx] = but = cls(root, text=text, command=lambda i=idx: example_method(i), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                but.bind('<Button-%d>' % RMB, lambda e=None, i=idx, *a: print('RIGHT-CLICKED on %d!'%i, *a))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 3, 4,
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, text='%d: e<t fg=blue u low>xam</t>ple 2000\nR Justify, C Anchor.......'%idx, command=lambda i=idx: example_method(i), repeatdelay=2000, **but_cfg_opts) #
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 5, 6,
            tfont = tk_font.Font(font=('Courier', 36))
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, text='''<t fg=green b font=%s tit>%d: example 2000/500\ncursor=hand2</t>'''%(tfont, idx), command=lambda i=idx: example_method(i), repeatdelay=2000, repeatinterval=500, cursor='hand2', **but_cfg_opts) 
                # font=('Courier', 36),
                root.widgets.append(but)
                but.idx = idx
                but.font = tfont
                if isinstance(but, TTWidget):
                    root.after(2000, lambda b=but, *a: b.config(case='upper'))
                    root.after(4000, lambda b=but, *a: b.config(case=''))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)):
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, text='idx: one<t tit>two\nthree</t><t cap>four</t>OR=Groove, flash on click\nAFG/ABG=blue/yellow\n SW Anchor, L Justify', command=lambda i=idx: example_method(i), overrelief=tk.GROOVE,  **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 9, 10,
            sv.set(value='X: SV:\npress to <t b>change</t>')
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, textvariable=sv, command=lambda i=idx: example_method(i), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                but.bind('<Button-%d>' % RMB, lambda e=None, i=idx, *a: print('>>>>>>>>>> RIGHT-CLICKED on %d!'%i, *a))
                root.after(10000, lambda i=idx, b=but: b.config(bg='white'))
            if post_config_b:
                root.after(5000, lambda i=idx: sv.set('%d: Five Seconds\n<t bg=yellow fg=red b i u>Later!\nred on yellow now,\nwhite bg in 5 secs...</t>'%i))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 11, 12,
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, command=lambda i=idx: cycle_but_state(i-4), underline=0, text="%d: <t cas=tit>cycle but%d state</t> <t bg=cyan>Cyan</t> (active=red/yellow)"%(idx, idx-4), bg='wheat', **but_cfg_opts) # -1)
                root.widgets.append(but)
                but.idx = idx
                if post_config_b:
                    root.after(4000, lambda i=idx, b=but: b.config(underline=21, text="%d: <t tit>cycle but%d state</t> <t bg=green>Green (updated)</t> (active=red/yellow)"%(i, i-4)))
                    root.after(8000, lambda i=idx, b=but: b.config(underline=3, bg='white'))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)):
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # (15, 16, )
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, text='%d: TTButton\n'%idx + '"ButtonRelease-%d"' % RMB, bg='wheat', command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)):
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, text='%d: TTButton normal now, anchored East, <t relief=groove bd=2>active</t> in 5 secs...\n'%idx, bg='wheat', command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                if post_config_b:
                    if cls == TTButton:
                        but.config(frame_s, bg='green')
                        but.config('child', (1, ), bg='cyan')
                    root.after(5000, lambda i=idx, b=but: b.config(default=tk.ACTIVE))
                    root.after(10000, lambda i=idx, b=but: b.config(default=tk.NORMAL, text='%d: <t case=title>NORMAL </t><t case=upper>again!</t>'%i))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 19, 20
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, font=('Courier', 24), text='%d: font is Courier 24\n<t fg=green bg=cyan size=12>Green on Cyan size 12</t><t fam=Arial fg=brown i=0>\nBrown Arial no Size</t>'%idx, bg='wheat', command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                root.after(2000, lambda i=idx, b=but: b.config(bg='white', fg='magenta'))
                if post_config_b:
                    root.after(4000, lambda i=idx, b=but: b.config(font=('Times', 8, 'italic bold')))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): #21, 22
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, bitmap='question', text='%d: Text on the Top'%idx, compound=tk.NONE, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): #23, 24
            if idx in but_nums:
                text = '%d: Bitmap on the Top, bitmap <t bitmap=question>Question</t> and <t bitmap=info>Info</t>'%idx
                root.buttons[idx] = but = cls(root, text=text, bitmap='error', compound=tk.TOP, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts) #
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 25, 26,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print('IMAGE %d is '%idx, image)
                compound = tk.LEFT
                root.buttons[idx] = but = cls(root, image=image, text='%d: <t fg=green>graphic location: %s</t>'%(idx, compound), fg='red', bg='cyan', compound=compound, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 27, 28,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print('IMAGE %d is '%idx, image)
                root.buttons[idx] = but = cls(root, text='<t image=%s>%d: Text on the Top</t>'%(image, idx), fg='red', bg='cyan', compound=tk.CENTER, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 29, 30,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print('IMAGE %d is '%idx, image)
                root.buttons[idx] = but = cls(root, text='%d: Text <t image=%s>on the</t> Top'%(idx, image, ), fg='red', bg='cyan', compound=tk.CENTER, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 31, 32,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print('IMAGE %d is '%idx, image)
                root.buttons[idx] = but = cls(root, image=image, compound=tk.LEFT, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        delay_time, loops = 2000, 1
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 33, 34,
            if idx in but_nums:
                root.image[idx] = image = tk.BitmapImage(data=BITMAP)
                print('IMAGE %d is '%idx, image)
                root.buttons[idx] = but = cls(root, image=image, compound=tk.LEFT, text='Simple Text', command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                for x in range(loops):
                    root.after((2 * x + 1) * delay_time, lambda b=but, *a: b.config(text='<t bg=red>Red </t><t bg=blue>Blue</t><t bitmap=question>question</t>'))
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 35, 36,
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, compound=tk.LEFT, text='<t>Simple</t> Text', fg='red', funderline=1, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
        for idx, cls in ((next(num), tk.Button), (next(num), TTButton)): # 37, 38,
            if idx in but_nums:
                root.buttons[idx] = but = cls(root, compound=tk.LEFT, text='<t>Simple</t> Text', fg='red', slant=tk_font.ITALIC, foverstrike=1, command=lambda i=idx, *a: print('BUTTON %d COMMAND!'%i, *a), **but_cfg_opts)
                root.widgets.append(but)
                but.idx = idx
                if idx == 38:
                    root.after(3000, lambda e=None, b=but, i=idx: b.config(text='<t bg=magenta>3 secs...</t>magenta bg'))
                    root.after(6000, lambda e=None, b=but, i=idx: b.config(funderline=1, foverstrike=0, bg='cyan'))
                print('BUTTON %d: KEYS: ' % idx, but.keys())
                print('BUTTON %d: CONFIG: ' % idx, but.config())
        if 1 in lab_nums:
            root.lab1 = tk.Label(root, text='%s %d: Normal Label\nFor 13: in 6 secs, bg=white, fg=magenta\nin 8 secs, Educate\nin 10 secs, font=Arial,48\nin 12 secs, Educate'%(tk.Label, 1))
            root.widgets.append(root.lab1)
            root.lab1.idx = 'L1'
        if 2 in lab_nums:
            root.lab2 = TTLabel(root, text='%s %d: <t b>Titled</t> Text <t tit>hi there</t>\nCustom Label'%(TTLabel, 2))
            root.widgets.append(root.lab2)
            root.lab2.idx = 'L2'
        if 1 in lb_nums:
            root.lb1 = lb1 = TTListbox(root, font=('Courier', 12), height=4, width=24)
            lb1.insert(tk.END, '<t fg=red case=up>red upper</t>')
            lb1.insert(tk.END, 'plain/normal')
            lb1.insert(tk.END, '<t fg=green bg=yellow>green on yellow</t>', '<t fg=magenta sfg=cyan case=tit>magenta (cyan selected) titled</t>')
            print('\nLB1: KEYS: ', lb1.keys())
            print('LB1: CONFIG:', lb1.config())
            root.widgets.append(root.lb1)
            root.lb1.idx = 'LB1'
            tt = TTToolTip(widget=lb1, text="This was via inserting tagged text,\nwith base=cursor", base=cursor_s)
            print('\nTT KEYS: ', tt.keys())
            print('TT CONFIG: ', tt.config())
        if 2 in lb_nums:
            root.lb2 = lb2 = TTListbox(root, font=('Courier', 12), height=4, width=24, text='<t fg=red case=up>red upper</t>plain/normal<t fg=green bg=yellow>green on yellow</t><t fg=magenta sfg=cyan case=tit>magenta (cyan selected) titled</t>', foverstrike=1)
            root.widgets.append(root.lb2)
            root.lb2.idx = 'LB2'
            TTToolTip(lb2, "This was via text attribute assigned tagged text,\nwith default base=widget")
            root.after(2000, lambda *a: lb2.config(case='upper', foverstrike=0))
        root.update_idletasks()
        width = 8 # 6 #
        index = 0
        root.frames = []
        for child in root.winfo_children():
            if isinstance(child, TTWidget) and not child.winfo_ismapped() or hasattr(child, 'idx'):
                if index % width == 0:
                    root.frames.append(tk.Frame(root, borderwidth=str(2), relief=tk.GROOVE, background='white'))
                    root.frames[-1].pack(**frame_pack_opts)
                    root.frames[-1].lower()
                child.pack(in_=root.frames[-1], **but_pack_opts)
                if isinstance(child, TTListbox):
                    pass
                elif not isinstance(child, TTWidget):
                    try:
                        text = child.cget(text_s)
                        child.config(text=strip_tags(text))
                    except:  # KeyError:
                        print('EXCEPTION Configuring %s %s' % (type(child), child))
                index += 1
            else:
                print('SKIPPING {0!r} ({1}): {2}'.format(child, child.__class__, 'NOT a TTWidget' if not isinstance(child, TTWidget) else 'already mapped' if child.winfo_ismapped() else 'because...'))
        fmt1 = gen_tag_attrs(options=dict(family='Courier', size=4, fun=True, ul=2, bg='yellow'))
        print('FMT1 is %r' % fmt1)
        debugText.pack(fill=tk.BOTH, expand=True)
        for bn in but_nums:
            but = root.buttons.get(bn)
            if but:
                but.bind('<ButtonRelease-3>', lambda e=None, b=but, *a: print('\n', *a), '+')
                if isinstance(but, TTWidget):
                    fmt = but.gen_tag_attrs()
                else:
                    fmt = '(N/A)'
                print('FMT  for but is', pprint.pformat(fmt))
                print('TEXT for but is %r' % but.cget(text_s))

    def cycle_but_state(num):
        states = (tk.DISABLED, tk.NORMAL, tk.ACTIVE)
        but = root.buttons[num]
        state = but.cget(state_s)
        index = states.index(state)
        new_state = states[(index + 1) % len(states)]
        but.config(state=new_state)
        print('BUT %d STATE is ' % num, new_state.upper(), ', was ', state)
        if isinstance(but, TTButton):
            print('BUT %d DUMP():' % num, but.dump())
        else:
            print('BUT %d CONFIG():' % num, but.config())

    def example_method(num=-1, *args, **kwargs):
        print('BUTTON %d COMMAND!' % num)
        button = root.buttons[num]  # UNUSED

    root = tk.Tk()
    sv = tk.StringVar(name='sv')
    build_the_gui(root)
    print(split_attrs('''family="Courier New" family='Times  New   Roman' size=12 upper'''))
    print(strip_tags('''one <t b>bold</t>'''))
    text_str = '''one\n\ntwo<t cap>Capital Letters</t><t bitmap=question></t>''' # <t fg="red" tit>Red\nBurn\n</t>\n
    text_chunks = split_tagged_text_into_chunks(text_str)
    print('TEXT is ', text_str, ', TEXT CHUNKS is ', text_chunks)
    divs = [split_chunk(ch) for ch in text_chunks]
    print('DIVS are ', divs)
    wrapped = wrap_tagged_text(text_str, 5)
    print('MATCH? ', wrapped == text_str, '\n', repr(text_str), '\n', repr(wrapped))
    text = '<tag fg=red>red</tag> and <tag bg=blue>blue</tag><tag bitmap=question /><tag bitmap=info></tag>'
    print('CHUNKS: ', split_tagged_text_into_chunks(text))
    print('SPLIT CHUNKS:', [split_chunk(chunk) for chunk in split_tagged_text_into_chunks(text)])
    root.mainloop()
