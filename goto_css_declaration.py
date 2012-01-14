'''
Goto-CSS-Declaration v0.2.1

Goto CSS declaration in an open *.css file from:
    - *.html
    - *.js
    - *.other_extantion

https://github.com/rmaksim/Sublime-Text-2-Goto-CSS-Declaration

Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>

MIT License, see http://opensource.org/licenses/MIT
'''

import sublime, sublime_plugin, re

class GotoCssDeclarationCommand(sublime_plugin.TextCommand):

    def run(self, edit, goto):
        '''@param {String} goto = "next" | "prev"'''

        settings  = sublime.load_settings(__name__ + '.sublime-settings')
        css_files = settings.get("css_files", "[]")


        def goto_decl(f_class, f_id):
            '''Returns "next" or "prev" nearest class or id '''

            if f_class or f_id:
                min_max = lambda x ,y: y and (not x or (x.a > y.a if goto == "next" else x.a < y.a))
                region  = lambda x, y: y if min_max(x, y) else x if min_max(y, x) else False

                found_reg = region(f_class, f_id)

                sel = view.sel()
                sel.clear()
                sel.add(found_reg)
                view.show(found_reg)
                return True


        def is_css(file_name):
            '''Returns True if file_name is .css (.less, .sass or .other from settings)'''

            file_type = re.match('.*(\..*)$', file_name or "")
            file_type = file_type.group(1) if file_type else ""

            return file_type in css_files


        view = self.view
        self.cur_pos   = view.sel()[0].a
        self.scope_reg = view.extract_scope(self.cur_pos)

        # if current window == css styles file
        if is_css(view.file_name()):
            class_or_id = view.settings().get('class_or_id')

            if class_or_id :

                if  goto == "next":
                    goto_decl(
                        view.find("\." + class_or_id, self.cur_pos + 1),
                        view.find("\#" + class_or_id, self.cur_pos + 1)
                    )

                else: # goto == "prev"
                    prev     = lambda x: filter(lambda y: y.a < self.cur_pos, x)
                    previous = lambda x: x and prev(x)[-1] if prev(x) else False

                    goto_decl(
                        previous(view.find_all("\." + class_or_id)),
                        previous(view.find_all("\#" + class_or_id))
                    )

        # go to opened CSS file and find in them
        else:
            class_or_id = self.get_class_or_id();
            win = sublime.active_window()
            for view in win.views():
                if is_css(view.file_name()):
                    view.settings().set('class_or_id', class_or_id)

                    if  goto_decl(
                            view.find("\." + class_or_id, 0),
                            view.find("\#" + class_or_id, 0)
                        ):
                        win.focus_view(view)

                    else:
                        sublime.status_message("not found [ " + class_or_id + " ]")


    def get_class_or_id(self):
        """Gets the class name from the current position in the editor

        <div class="class_1 class_2"></div>
                              |->cursor
        returns "class_2"
        """

        def get_sym(pos):
            """Returns the symbol from the current position in editor"""
            sym = self.view.substr(sublime.Region(pos, pos + 1))
            return sym

        rule_type  = set([".", "#"])
        delims     = set([" ", "\"", "'", "<", ">", "/", "\n", ":"])
        all_delims = rule_type | delims

        left = self.cur_pos
        while get_sym(left) in delims:
            left -= 1
        while left > self.scope_reg.a and get_sym(left) not in all_delims:
            left -= 1
        if get_sym(left) in all_delims: left += 1

        right = self.cur_pos
        while right < self.scope_reg.b and get_sym(right) not in all_delims:
            right += 1

        return self.view.substr(sublime.Region(left, right))
