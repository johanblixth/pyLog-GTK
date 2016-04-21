#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py  'pyLog GTK3' version
#
#  Copyright 2016 Johan Blixth <johan@blixth.se>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pickle
import time


class pyLog(Gtk.Window):
    # Initialization
    def __init__(self):

        # Load Old Items from File, if no file, create new dictionary
        try:
            self.log = pickle.load(open('pylog.dat', 'rb'))
        except:
            self.log = {}
        self.selectedKey=""

        # Setup main Window
        Gtk.Window.__init__(self, title="pyLog")
        self.set_border_width(10)
        self.set_default_size(600, 500)

        # Set header
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "pyLog"
        self.set_titlebar(headerbar)
        # Layout main GUI
        notebook = Gtk.Notebook()
        self.add(notebook)

        # viewEntry page
        pageViewEntry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # Liststore for treeview
        scrollable = Gtk.ScrolledWindow()
        self.listStore = Gtk.ListStore(str, str)
        self.updateListStore(None)
        # get selectedRowselection
        self.selectedRow = self.treeview.get_selection()
        self.selectedRow.connect("changed", self.item_selected)
        scrollable.add(self.treeview)
        pageViewEntry.add(scrollable)
        self.viewEntryButton = Gtk.Button("View Entry")
        self.viewEntryButton.connect("clicked", self.viewEntry)
        pageViewEntry.add(self.viewEntryButton)
        notebook.append_page(pageViewEntry, Gtk.Label('View Entries'))

        # newEntry page
        pageNewEntry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #Title Entry
        hbox1 = Gtk.Box(border_width=10)
        self.titleEntry = Gtk.Entry()
        self.titleEntry.set_hexpand(True)
        hbox1.pack_start(Gtk.Label("Title:", xalign=0), True, True, 0)
        hbox1.pack_start(self.titleEntry, True, True, 0)
        #Content Entry
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, border_width=10)
        vbox.add(Gtk.Label("Content:",xalign=0))
        self.contentEntry = Gtk.TextView()
        self.contentEntry.set_vexpand(True)
        vbox.pack_start(self.contentEntry, True, True, 0)
        buttonPost = Gtk.Button("Post Entry",xalign=0)
        buttonClear = Gtk.Button("Clear Entry",xalign=1)
        hboxButton = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, border_width=10, spacing=10)
        hboxButton.add(buttonPost)
        hboxButton.add(buttonClear)
        #connect Buttons newEntry
        buttonPost.connect("clicked",self.postEntry)
        buttonClear.connect("clicked",self.clearEntry)

        pageNewEntry.add(hbox1)
        pageNewEntry.add(vbox)
        pageNewEntry.add(hboxButton)
        notebook.append_page(pageNewEntry, Gtk.Label('New Entry'))

    # selected row
    def item_selected(self, selection):
        try:
            model, row = selection.get_selected()
            if row is not "":
                self.selectedKey = (model[row][0])
        except:
            return 0

    # view entry function
    def viewEntry(self, widget):
        try:
            a,b = self.log[self.selectedKey]
        except:
            a,b = "",""
        viewWindow = Gtk.Window(title="View Entry", border_width=10)
        viewWindow.set_default_size(600,400)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, border_width=10,spacing=10)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, border_width=10,spacing=10)
        viewWindow.add(vbox)
        #title View
        label = Gtk.Label("Title:", xalign=0)
        hbox.add(label)
        titleView = Gtk.Entry()
        titleView.set_text(a)
        titleView.set_hexpand(True)
        titleView.set_editable(False)
        hbox.add(titleView)
        #content View
        label = Gtk.Label("Content:",xalign=0)
        contentView = Gtk.TextView()
        contentViewBuffer = contentView.get_buffer()
        contentViewBuffer.set_text(b)
        contentView.set_buffer(contentViewBuffer)
        contentView.set_vexpand(True)
        contentView.set_editable(False)
        vbox2.add(label)
        vbox2.add(contentView)
        vbox.add(hbox)
        vbox.add(vbox2)
        viewWindow.show_all()

    #Button Post
    def postEntry(self, widget):
        key = time.strftime("%Y%m%d%H%M%S")
        a = self.titleEntry.get_text()
        postBuffer = self.contentEntry.get_buffer()
        start = postBuffer.get_start_iter()
        end = postBuffer.get_end_iter()
        b = postBuffer.get_text(start, end, True)
        self.clearEntry(None)
        self.log[key] = (a,b)
        self.updateListStore(None)
        pickle.dump(self.log, open('pylog.dat','wb'))

    #Button Clear
    def clearEntry(self, widget):
        self.titleEntry.set_text("")
        textBuffer = self.contentEntry.get_buffer()
        textBuffer.set_text("")
        self.contentEntry.set_buffer(textBuffer)

    def updateListStore(self, widget):
        self.listStore.clear()
        for item in sorted(self.log, reverse=True):
            tmp = (item, self.log[item][0])
            self.listStore.append(list(tmp))
        # treeview
        self.treeview = Gtk.TreeView(self.listStore)
        self.treeview.set_vexpand(True)
        self.treeview.set_vscroll_policy(True)
        for i, col_title in enumerate(["Key", "Title"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.treeview.append_column(column)

if (__name__ == '__main__'):
    app = pyLog()
    app.connect('delete-event', Gtk.main_quit)
    app.show_all()
    Gtk.main()
