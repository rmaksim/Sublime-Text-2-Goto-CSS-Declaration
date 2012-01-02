#Goto-CSS-Declaration

## Goto CSS declaration in an open *.css file from other file (*.html, *.js, *.other_extantion)


Example
-------
    <div id="menu_1" class="class_1 class_2"></div>
                                       ^
                                       |-cursor

Pressing the key `super+right` go to the first CSS declaration of class_2

    ...
    .class_2           { ... }
    ...
    .b-header .class_2 { ... }
    ...
    .b-footer .class_2 { ... }
    ...
    #menu_1   .class_2 { ... }
    ...

and if then press `F3` goes to the next CSS declaration of class_2.


Default (Linux).sublime-keymap
------------------------------
    [
        { "keys": ["super+right"], "command": "goto_css_declaration" }
    ]


Copyright
---------
### Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>

MIT License, see http://opensource.org/licenses/MIT