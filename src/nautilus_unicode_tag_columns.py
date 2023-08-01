# Started from playing with and modifying of
#    * Nautilus-Emblems-Menu-Extension
#      https://github.com/allefant/Nautilus-Emblems-Menu-Extension
#      by ubuntu@allefant.com
#    * Nautilus extension: nautilus extra columns
#      https://github.com/3ed/nautilus-nec
#      by krzysztof1987@gmail.com


import gi
gi.require_version('Nautilus', '4.0')

from gi.repository import Nautilus, GObject
import os, glob, subprocess
from collections import OrderedDict, namedtuple
from urllib.parse import unquote


EmojiEntry = namedtuple('EmojiEntry', ['ordering', 'label', 'string'])

EMOJIS = OrderedDict([string, EmojiEntry(i, f'{string} {label}', string)]
        for [i, (string, label)] in enumerate([
    ('✔', 'check mark')
  , ('❤️', 'Red Heart')
  , ('🔴', 'Red Circle')
  , ('🟠', 'Orange Circle')
  , ('🟡', 'Yellow Circle')
  , ('🟢', 'Green Circle')
  , ('🔵', 'Blue Circle')
  , ('🟣', 'Purple Circle')
  , ('🟤', 'Brown Circle')
  , ('⚫', 'Black Circle')
  , ('⚪', 'White Circle')
]))

def read_metadata_emoji(file_info):
    path = unquote(file_info.get_uri()[7:])
    p = subprocess.Popen(['gio', 'info', '-a', 'metadata::custom_unicode_tags', path],
        stdout = subprocess.PIPE)
    out, err = p.communicate()
    emojis = []
    for row in out.splitlines()[1:]:
        row = row.strip()
        if row.startswith(b'metadata::custom_unicode_tags:'):
            row = row[len(b'metadata::custom_unicode_tags:'):].strip(b"[ ]")
            emojis.extend([x.strip() for x in
                row.split(b',')])
    return {e.decode() for e in emojis};


class UnicodeTagColumn(GObject.GObject,
             Nautilus.MenuProvider,
             Nautilus.ColumnProvider,
             Nautilus.InfoProvider):

    # The MenuProvider
    def get_file_items(self, files):
        menu_item = Nautilus.MenuItem(name = 'CodeSelectionMenu::UnicodeTags',
            label = 'Emoji Tags', tip = '', icon = '')

        submenu = Nautilus.Menu()
        menu_item.set_submenu(submenu)

        sub_item = Nautilus.MenuItem(name = 'CodeSelectionMenu::Clear',
        label = 'Clear', tip = '', icon = '')
        sub_item.connect('activate', self.clear_metadata_emoji, files)
        submenu.append_item(sub_item)

        for emoji in EMOJIS.values():
            emoji_item = Nautilus.MenuItem(
                name = 'CodeSelectionMenu::' + emoji.string,
                label = emoji.label, tip = emoji.label)
            emoji_item.connect('activate', self.write_metadata_emoji, (files, emoji))
            submenu.append_item(emoji_item)

        return menu_item,

    def write_metadata_emoji(self, menu, files_emoji):
        (files, emoji) = files_emoji
        for file_info in files:
            path = unquote(file_info.get_uri()[7:])
            file_emojis = read_metadata_emoji(file_info);
            # write all emojis
            file_emojis.add(emoji.string)
            p = subprocess.Popen(['gio', 'set', '-t', 'stringv',
                path, 'metadata::custom_unicode_tags'] + list(file_emojis))
            p.communicate()
            file_info.invalidate_extension_info()

    def clear_metadata_emoji(self, menu, files):
        for file_info in files:
            p = subprocess.Popen(['gio', 'set', '-t', 'unset',
                unquote(file_info.get_uri()[7:]), 'metadata::custom_unicode_tags'])
            p.communicate()
            file_info.invalidate_extension_info()

    # the ColumnProvider
    def get_columns(self):
        return [
            Nautilus.Column(
                name='NautilusPython::unicode_tag_column',
                attribute='unicode_tags',
                label='Emoji Tags',
                description='Emoji Tags'
            )
        ]

    def update_file_info_full(self, provider, handle, closure, file_info):
        GObject.idle_add(
            self.set_file_info,
            provider,
            handle,
            closure,
            file_info,
        )
        return Nautilus.OperationResult.IN_PROGRESS

    def set_file_info(self, provider, handle, closure, file_info):
        filename = unquote(file_info.get_uri()[7:])
        # read the value
        file_emojis = read_metadata_emoji(file_info)
        file_emojis = sorted(file_emojis, key=lambda string:EMOJIS[string].ordering)
        value = ''.join(file_emojis);
        # add it
        file_info.add_string_attribute('unicode_tags', value);
        # complete it
        Nautilus.info_provider_update_complete_invoke(
            closure, provider, handle, Nautilus.OperationResult.COMPLETE)

