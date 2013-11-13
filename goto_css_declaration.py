# -*- coding: utf-8 -*-
"""
Goto-CSS-Declaration v0.3

Goto CSS declaration in an open *.css file from:
    - *.html
    - *.js
    - *.other_extantion

https://github.com/rmaksim/Sublime-Text-2-Goto-CSS-Declaration

Copyright (c) 2011 Razumenko Maksim <razumenko.maksim@gmail.com>

MIT License, see http://opensource.org/licenses/MIT
"""

import sublime, sublime_plugin, re

class GotoCssDeclarationCommand(sublime_plugin.TextCommand):

    def run(self, edit, goto):
        """@param {String} goto = "next" | "prev"""

        settings  = sublime.load_settings('goto_css_declaration.sublime-settings')
        css_files = settings.get("css_files", "[]")

        win = sublime.active_window()
        view = self.view

        self.cur_pos   = view.sel()[0].a
        self.scope_reg = view.extract_scope(self.cur_pos)

        if goto == "next":
            cmp = lambda x, y: x if x.a < y.a else y
        else:
            cmp = lambda x, y: x if x.a > y.a else y


        def is_css(view):
            """Returns True if file_name is .css (.less, .sass or .other from settings)"""

            file_type = re.match('.*(\..*)$', view.file_name() or "")
            file_type = file_type.group(1) if file_type else ""

            return file_type in css_files


        def set_settings_for_all_tabs():
            """  """
            views = win.views()

            for view in views:
                if is_css(view):
                    view.settings().set('class_or_id', self.class_or_id)


        def nearest(region1, region2):
            """  """
            # ST2 view.find returns None if not found
            if None in (region1, region2):
                return region1 or region2

            # ST3 view.find returns (-1,-1) if not found
            if region1.a == -1 and region1.b == -1:
                return region2

            if region2.a == -1 and region2.b == -1:
                return region1

            return cmp(region1, region2)


        def goto_region(view, region):
            """ """
            if region:
                sel = view.sel()
                sel.clear()
                sel.add(region)
                view.show(region)
                return True
            else:
                return False


        def goto_decl(view, find_in_other=None):
            """  """
            if not is_css(view):
                return False

            pos = self.cur_pos

            if goto == "next":  # goto nearest next declaration
                if find_in_other:
                    pos = -1

                return goto_region(view,
                    nearest(
                        view.find("\." + self.class_or_id, pos + 1),
                        view.find("\#" + self.class_or_id, pos + 1)
                    ))

            elif goto == "prev":  # goto nearest previous declaration
                def previous(regions):
                    all_prev = [r for r in regions if r.a < pos]
                    if all_prev:
                        return all_prev[-1]  # return nearest

                if find_in_other:
                    pos = view.size()

                return goto_region(view,
                    nearest(
                        previous(view.find_all("\." + self.class_or_id)),
                        previous(view.find_all("\#" + self.class_or_id))
                    ))


        def goto_decl_in_other_file(view):
            """  """
            views = win.views()

            # index of current file from all views
            vi = [v.id() for v in views].index(view.id())

            prev = views[:vi]
            next = views[vi+1:]

            if goto == "next":
                views = next
                views.extend(prev)

            elif goto == "prev":
                views = prev
                views.reverse()
                next.reverse()
                views.extend(next)

            for view in views:
                if goto_decl(view, "find_in_other"):
                    win.focus_view(view)
                    return
                else:
                    sublime.status_message(
                        'Goto-CSS-Declaration: ' +
                        'not found CLASS or ID "' + self.class_or_id + '"'
                        )


        # **********************************************************************

        if is_css(view):
            self.class_or_id = view.settings().get('class_or_id')
        else:
            self.class_or_id = self.get_class_or_id();

        if not self.class_or_id:
            return

        set_settings_for_all_tabs()

        if not goto_decl(view):
            goto_decl_in_other_file(view)

        # **********************************************************************


    def get_class_or_id(self):
        """Gets the class name from the current position in the editor

        <div class="class_1 class_2"></div>
                              |->cursor
        returns "class_2"
        """

        def get_sym(pos):
            """Returns the symbol from the current position in editor"""
            sym = self.view.substr(sublime.Region(pos, pos+1))
            return sym

        rule_type  = set(". #".split(" "))
        delims     = set([" "]+"{ } < > ( ) [ ] / : , + = ` ' \n \"".split(" "))
        all_delims = rule_type | delims
        left = self.cur_pos

        # $(".b-qwe,.b-asd")        $(".b-qwe,.b-asd")
        #    ^                          ^
        if get_sym(left) in rule_type:
            left += 1

        # $(".b-qwe,.b-asd")        $(".b-qwe,.b-asd")
        #          ^                        ^
        if get_sym(left) in delims:
            left -= 1

        # $(".b-qwe,.b-asd")        $(".b-qwe,.b-asd")
        #         ^                     ^
        while left >= self.scope_reg.a and get_sym(left) not in all_delims:
            left -= 1
        left += 1

        # if get_sym(left) in all_delims: left += 1
        right = self.cur_pos if self.cur_pos >= left else left

        while right < self.scope_reg.b and get_sym(right) not in all_delims:
            right += 1

        word = self.view.substr(sublime.Region(left, right))

        # @see http://www.w3.org/TR/CSS21/grammar.html#scanner
        # class="re-valid_class_or_id"
        match = re.match('(-?[_a-zA-Z]+)([_a-zA-Z0-9-])*$', word)

        return word if match else None
