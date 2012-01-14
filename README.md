#Goto-CSS-Declaration

**v0.2.1**

---
## Goto CSS declaration in an open \*.css (.less, .sass, .other) file from other file (\*.html, \*.js, \*.other_extantion)

**Forum Thread**
http://www.sublimetext.com/forum/viewtopic.php?f=5&t=4397

![Goto-CSS-Declaration](https://github.com/rmaksim/Sublime-Text-2-Goto-CSS-Declaration/raw/master/goto_css_declaration.gif)


### Example
**html:**

    <div id="box" class="box"></div>
                          ^
                          |-cursor

**js:**

    $(".box").click(...);
         ^
         |-cursor


Pressing the key `super+right` or `super+left` go to the **first** CSS declaration of `box` (.class or #id => .box or #box), in this example the id `#box`

    #box .box-shadow {
        background: url(../img/box.jpg);
        }
    #box-shadow .box-shadow-1 {
        box-shadow: 0 0 5px #ff0;
        }
        .box__inner {
            box-shadow: 0 0 5px #f00;
            }

and if then press (in CSS file) `super+right` goes to the **next** CSS declaration of `box`, in this example the class `.box-shadow`, and next => `#box-shadow`, and next => `.box-shadow-1`, and next => `.box__inner`

also you can press (in CSS file) `super+left` and goes to the **previous** CSS declaration of `box`.


### [goto_css_declaration.sublime-settings](https://github.com/rmaksim/Sublime-Text-2-Goto-CSS-Declaration/blob/master/goto_css_declaration.sublime-settings)
    {
        "css_files": [".css", ".sass", ".less"]
    }


### Default (Linux).sublime-keymap
    super + right
    super + left


### Default (Windows).sublime-keymap
    super + .
    super + ,


### Copyright
**Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>**

MIT License, see http://opensource.org/licenses/MIT
