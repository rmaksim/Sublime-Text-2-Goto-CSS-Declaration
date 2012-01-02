'''
Goto-CSS-Declaration v0.1.0

Goto CSS declaration in an open *.css file from:
    - *.html
    - *.js
    - *.other_extantion

https://github.com/rmaksim/Sublime-Text-2-Goto-CSS-Declaration

Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>

MIT License, see http://opensource.org/licenses/MIT
'''

import sublime, sublime_plugin

class GotoCssDeclarationCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        self.cur_pos = self.view.sel()[0].a
        self.scope_reg  = self.view.extract_scope(self.cur_pos)
        class_name = self.get_class();

        win = sublime.active_window()
        for view in win.views():
            f_name = view.file_name()
            # Find Results has no file_name
            if f_name and f_name[-3:] == "css":
                find_reg = view.find(class_name, 0)
                if find_reg:
                    win.focus_view(view)
                    sel = view.sel()
                    sel.clear()
                    sel.add(find_reg)
                    view.show(find_reg)
                    win.run_command("find_under_expand")
                    sel.clear()
                    sel.add(find_reg)
                else:
                    sublime.status_message("not found [ " + class_name + " ]")


    def get_class(self):
        """Gets the class name from the current position in the editor

                              |->cursor
        <div class="class_1 class_2"></div>
        returns "class_2"
        """

        def get_sym(pos):
            """Returns the symbol from the current position in editor"""
            sym = self.view.substr(sublime.Region(pos, pos + 1))
            return sym

        rule_type = set([".", "#"])
        delim = set([" ", "\"", "'", "<", ">", "/", "\n"])
        all_delim = rule_type | delim

        left = self.cur_pos
        while get_sym(left) in delim:
            left -= 1
        while left > self.scope_reg.a and get_sym(left) not in all_delim:
            left -= 1
        if get_sym(left) in all_delim: left += 1

        right = self.cur_pos
        while right < self.scope_reg.b and get_sym(right) not in delim:
            right += 1

        return self.view.substr(sublime.Region(left, right))
