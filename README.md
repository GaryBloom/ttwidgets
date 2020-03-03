# ttwidgets

Package **TTWidgets** improves the `Button`, `Label`, and `Listbox` widgets of
the Tkinter library and provides a new `ToolTip` widget, all with support for
multiple fonts and visual schemes.

Although the standard Tkinter `Button` and `Label` widgets are limited to a
single set of widget options (e.g. background/bg, foreground/fg, bitmap,
cursor, relief) and a **single font**, a **TTWidgets** enhanced widget can be
passed *tagged text* instead of plain text to create a visually compound widget 
(with multiple fonts and visual option sets) that behaves like a simple widget.

- The `Button` and `Label` implementations are complete.
- The `Listbox` implementation is partial: there is no multi-font support, but 
    the user can use the new 'text' option to pass in *tagged text* to define all
    the elements with visual schemes.  The user can also pass *tagged text* to the
    insert() method, and thereby skip the secondary call to itemconfig() for the
    inserted element(s).  A full multi-font implementation of a *tagged text*
    `Listbox` may come later.
- As a bonus, a `ToolTip` widget is included, which also accepts *tagged text*
    as input, allowing the creation of colorful and multi-font ToolTips.

All **TTWidgets** support the 'text' keyword to accept and process *tagged text*
as input on creation. 
All **TTWidgets** support modification of 'text' via the `config()` method and
retrieval via `cget()`.

As a **ttwidgets** Button example:

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

As a **ttwidgets** ToolTip example:

    tooltip = ttwidgets.TTToolTip(reg_but, text='My <t bg=cyan px=2 py=2 bd=2 relief=groove size=6 wraplength=70>Regular Button Cycle All States</t><t b> ToolTip</t>... See how it matches? :)', bg='white', relief=tk.GROOVE, borderwidth=5)
    
gives a ToolTip for button "reg_but" which includes a smaller version of the
button it is tipping, to make the ToolTip more visually appealing. The ToolTip
also shows bold text and a white background.

![exampleToolTip](https://user-images.githubusercontent.com/19311746/75097456-fa2e5b80-5578-11ea-8768-bce0c4306874.jpg "Example TTToolTip")

In general, all the visual options and font attributes are supported in the
*tagged text*.  For a *tagged text* overview, please see **ttwidgets** class `TTWidget` help.
