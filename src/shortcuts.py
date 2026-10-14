# shortcuts.py
#
# Copyright 2026 Diego Povliuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from gettext import gettext as _

import gi

gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gdk, Gtk

from .utils import KEY_REMAP

INTERNAL_BINDINGS = f"""\
UP               no-osd add volume 5; show-text "{_("Volume")}: ${{volume}}%" #{_("Volume Increase")}
DOWN             no-osd add volume -5; show-text "{_("Volume")}: ${{volume}}%" #{_("Volume Decrease")}
d                no-osd add volume 5; show-text "{_("Volume")}: ${{volume}}%" #{_("Volume Increase")}
c                no-osd add volume -5; show-text "{_("Volume")}: ${{volume}}%" #{_("Volume Decrease")}
WHEEL_UP         no-osd add volume 5; show-text "{_("Volume")}: ${{volume}}%"
WHEEL_DOWN       no-osd add volume -5; show-text "{_("Volume")}: ${{volume}}%"
k                nonrepeatable cycle pause; #{_("Play/Pause")}
p                nonrepeatable cycle pause; #{_("Play/Pause")}
SPACE            nonrepeatable cycle pause; #{_("Play/Pause")}
BS               nonrepeatable cycle pause; #{_("Play/Pause")}
Z                nonrepeatable cycle sub down; show-text "{_("Subtitles")}: ${{sub}}" #{_("Previous Subtitle Track")}
alt+z            nonrepeatable cycle secondary-sid; show-text "{_("Secondary Subtitles")}: ${{secondary-sid}}"; #{_("Next Secondary Subtitle Track")}
ctrl+z           nonrepeatable cycle secondary-sid down; show-text "{_("Secondary Subtitles")}: ${{secondary-sid}}"; #{_("Previous Secondary Subtitle Track")}
A                nonrepeatable cycle audio down; show-text "{_("Audio")}: ${{audio}}" #{_("Previous Audio Track")}
j                set video-zoom 0; set video-align-x 0; set video-align-y 0; set video-pan-x 0; set video-pan-y 0; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Reset Zoom and Pan")}
l                seek 10; show-text "⯈⯈" #{_("Seek 10s Forward")}
LEFT             seek -5; show-text "⯇⯇" #{_("Seek 5s Backward")}
RIGHT            seek 5; show-text "⯈⯈" #{_("Seek 5s Forward")}
s                seek -5; show-text "⯇⯇" #{_("Seek 5s Backward")}
h                seek 5; show-text "⯈⯈" #{_("Seek 5s Forward")}
F11              nonrepeatable cycle fullscreen; #{_("Fullscreen")}
f                nonrepeatable cycle fullscreen; #{_("Fullscreen")}
ESC              set fullscreen no; #{_("Exit Fullscreen")}
MBTN_LEFT_DBL    nonrepeatable cycle fullscreen
MBTN_MID         nonrepeatable cycle fullscreen
MBTN_BACK        playlist-prev; 
MBTN_FORWARD     playlist-next;
w                nonrepeatable playlist-prev; #{_("Previous File")}
b                nonrepeatable playlist-next; #{_("Next File")}
WHEEL_LEFT       seek -5 keyframes; show-text "⯇⯇"
WHEEL_RIGHT      seek 5 keyframes; show-text "⯈⯈"
shift+WHEEL_DOWN seek -5 keyframes; show-text "⯇⯇"
shift+WHEEL_UP   seek 5 keyframes; show-text "⯈⯈"
=                add video-zoom 0.05; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Zoom In")}
+                add video-zoom 0.05; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Zoom In")}
-                add video-zoom -0.05; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Zoom Out")}
z                add video-zoom 0.05; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Zoom In")}
a                add video-zoom -0.05; show-text "{_("Zoom")}: ${{video-zoom}}" #{_("Zoom Out")}
n                add video-align-x -0.1; show-text "{_("Pan")}: ${{video-align-x}}" #{_("Pan Left")}
i                add video-align-x 0.1; show-text "{_("Pan")}: ${{video-align-x}}" #{_("Pan Right")}
o                add video-align-y -0.1; show-text "{_("Pan")}: ${{video-align-y}}" #{_("Pan Up")}
,                add video-align-y 0.1; show-text "{_("Pan")}: ${{video-align-y}}" #{_("Pan Down")}
x                add video-align-y -0.1; show-text "{_("Pan")}: ${{video-align-y}}" #{_("Pan Up")}
e                add video-align-y 0.1; show-text "{_("Pan")}: ${{video-align-y}}" #{_("Pan Down")}
Ctrl+WHEEL_UP    script-binding positioning/cursor-centric-zoom 0.05
Ctrl+WHEEL_DOWN  script-binding positioning/cursor-centric-zoom -0.05
.                add sub-delay +0.1; show-text "{_("Subtitle Delay")}: ${{sub-delay}}" #{_("Increase Subtitle Delay")}
PGUP             add sub-pos -1; show-text "{_("Subtitle Position")}: ${{sub-pos}}" #{_("Move Subtitles Up")}
PGDWN            add sub-pos +1; show-text "{_("Subtitle Position")}: ${{sub-pos}}" #{_("Move Subtitles Down")}
G                add sub-scale +0.05; show-text "{_("Subtitle Scale")}: ${{sub-scale}}" #{_("Increase Subtitle Scale")}
F                add sub-scale -0.05; show-text "{_("Subtitle Scale")}: ${{sub-scale}}" #{_("Decrease Subtitle Scale")}
m                nonrepeatable no-osd cycle mute; no-osd set user-data/show-icon "yes" #{_("Mute/Unmute")}
ctrl+-           add audio-delay -0.1; show-text "{_("Audio Delay")}: ${{audio-delay}}" #{_("Decrease Audio Delay")}
ctrl+=           add audio-delay 0.1; show-text "{_("Audio Delay")}: ${{audio-delay}}" #{_("Increase Audio Delay")}
ctrl++           add audio-delay 0.1; show-text "{_("Audio Delay")}: ${{audio-delay}}" #{_("Increase Audio Delay")}
ctrl+[           frame-step -1 seek; show-text "⯇⯇" #{_("Go Back One Frame")}
ctrl+]           frame-step 1 seek; show-text "⯈⯈" #{_("Advance One Frame")}
r                frame-step -1 seek; show-text "⯇⯇" #{_("Go Back One Frame")}
g                frame-step 1 seek; show-text "⯈⯈" #{_("Advance One Frame")}
Ctrl+LEFT        nonrepeatable add chapter -1 #{_("Seek to the Previous Chapter")}
Ctrl+RIGHT       nonrepeatable add chapter 1 #{_("Seek to the Next Chapter")}
F7               nonrepeatable script-message cine-screenshot video #{_("Take Screenshot Without Subtitles")}
I                nonrepeatable script-binding stats/display-stats-toggle #{_("Statistics Overlay")}
ctrl+l           nonrepeatable ab-loop #{_("Set/Clear A-B Loop Points")}
L                nonrepeatable cycle-values loop-file "inf" "no"; show-text "{_("Loop")}: ${{loop-file}}" #{_("Loop File")}
1                add contrast -1; show-text "{_("Contrast")}: ${{contrast}}" #{_("Decrease Contrast")}
2                add contrast 1; show-text "{_("Contrast")}: ${{contrast}}" #{_("Increase Contrast")}
3                add brightness -1; show-text "{_("Brightness")}: ${{brightness}}" #{_("Decrease Brightness")}
4                add brightness 1; show-text "{_("Brightness")}: ${{brightness}}" #{_("Increase Brightness")}
5                add gamma -1; show-text "{_("Gamma")}: ${{gamma}}" #{_("Decrease Gamma")}
6                add gamma 1; show-text "{_("Gamma")}: ${{gamma}}" #{_("Increase Gamma")}
7                add saturation -1; show-text "{_("Saturation")}: ${{saturation}}" #{_("Decrease Saturation")}
8                add saturation 1; show-text "{_("Saturation")}: ${{saturation}}" #{_("Increase Saturation")}
[                nonrepeatable multiply speed 1/1.1; show-text "{_("Speed")}: ${{speed}}×" #{_("Decrease Playback Speed")}
]                nonrepeatable multiply speed 1.1; show-text "{_("Speed")}: ${{speed}}×" #{_("Increase Playback Speed")}
*                set speed 1.0; show-text "{_("Speed")}: ${{speed}}×" #{_("Reset Playback Speed")}
"""

GENERAL_SHORTCUTS = [
    (_("New Window"), "app.new-window"),
    (_("Open Files"), "win.clear-and-add"),
    (_("Open Folder"), "win.open-folder"),
    (_("Open URL"), "win.open-url"),
    (_("Add Files to Playlist"), "win.add-playlist-files"),
    (_("Add Folder to Playlist"), "win.add-playlist-folder"),
    (_("Add URL to Playlist"), "win.add-url"),
    (_("Open Subtitles Menu"), "win.open-sub-menu"),
    (_("Open Audio Menu"), "win.open-audio-menu"),
    (_("Open Chapters Menu"), "win.open-chapters-menu"),
    (_("Watch History"), "win.open-history"),
    (_("Show Shortcuts"), "win.custom-shortcuts"),
    (_("Close Window"), "win.quit"),
    (_("Save Session"), "win.save-session"),
    (_("Save Session and Close"), "win.save-session-close"),
    (_("Quit"), "app.quit"),
]

MPV_TO_GTK = {v: k for k, v in KEY_REMAP.items()}


def translate_mpv_to_gtk(key):
    """Converts mpv key strings to GTK accelerator format with symbol support."""
    # Handle single uppercase chars
    if len(key) == 1 and key.isupper():
        key = f"<Shift>{key.lower()}"

    # Replace mpv modifiers with GTK format
    key = re.sub(r"ctrl\+", "<Control>", key, flags=re.IGNORECASE)
    key = re.sub(r"alt\+", "<Alt>", key, flags=re.IGNORECASE)
    key = re.sub(r"shift\+", "<Shift>", key, flags=re.IGNORECASE)
    key = re.sub(r"meta\+", "<Meta>", key, flags=re.IGNORECASE)

    parts = key.split(">")
    base_key = parts[-1]

    # Map the base key if it exists in the reversed KEY_REMAP
    if base_key.upper() in MPV_TO_GTK:
        base_key = MPV_TO_GTK[base_key.upper()]
    elif base_key in MPV_TO_GTK:
        base_key = MPV_TO_GTK[base_key]

    # Dynamically resolve single characters/symbols using Gdk
    elif len(base_key) == 1:
        unicode_val = ord(base_key)
        keyval = Gdk.unicode_to_keyval(unicode_val)
        name = Gdk.keyval_name(keyval)

        if name:
            # If Gdk returns a single char (like "A"), GTK accelerators need it lowercase ("a")
            # If it returns a symbol name (like "period"), use it directly
            if len(name) == 1:
                base_key = name.lower()
            else:
                base_key = name
        else:
            # Fallback if Gdk fails to find a name
            base_key = base_key.lower()

    return ">".join(parts[:-1]) + (">" if len(parts) > 1 else "") + base_key


def get_section_name(cmd):
    """Categorizes an mpv command into a section title."""
    cmd = cmd.lower()

    def is_match(keyword, cmd):
        # matches the boundary between a word char and a non-word char
        return re.search(rf"\b{re.escape(keyword)}\b", cmd)

    mapping = [
        (
            _("Display & Video"),
            [
                "video",
                "fullscreen",
                "contrast",
                "brightness",
                "gamma",
                "saturation",
                "hue",
                "panscan",
                "zoom",
                "rotate",
                "aspect",
                "vf",
            ],
        ),
        (_("Subtitles"), ["sub", "sid"]),
        (_("Audio & Volume"), ["volume", "mute", "audio", "aid", "af", "ao"]),
        (_("Navigation"), ["seek", "chapter", "playlist", "frame", "revert-seek"]),
        (_("Playback"), ["pause", "stop", "quit", "speed", "loop"]),
    ]

    if "screenshot" in cmd:
        return _("Miscellaneous")

    for section, keywords in mapping:
        if any(is_match(k, cmd) for k in keywords):
            return section

    return _("Miscellaneous")


def present_shortcuts_dialog(win, mpv_bindings):
    """
    Presents the shortcuts dialog for the app actions and mpv bindings,
    joining multiple keys if they trigger the same command.
    """
    # Key: (label, section_title), Value: List of gtk_accelerators
    grouped_bindings = {}

    # First Pass: Resolve which keys are active (handling priority)
    resolved_keys = {}
    for b in mpv_bindings:
        key = b.get("key")
        if not key or "MBTN" in key or "WHEEL" in key or b.get("cmd") == "ignore":
            continue
        if b.get("is_weak", False):
            continue

        priority = b.get("priority", 0)
        if key not in resolved_keys or priority >= resolved_keys[key].get(
            "priority", 0
        ):
            resolved_keys[key] = b

    # Second Pass: Group keys by their command/label
    for key, b in resolved_keys.items():
        cmd = b.get("cmd", "")
        gtk_accel = translate_mpv_to_gtk(key)

        success, _key, _mods = Gtk.accelerator_parse(gtk_accel)
        if not success:
            continue

        # Determine the label (translatable)
        label = b.get("comment")
        if not label:
            clean_cmd = cmd.split(";")[0].strip()
            label = clean_cmd.replace("-", " ")
            label = label.capitalize()

        section_title = get_section_name(cmd)

        # Group by the unique combination of the label and its section
        group_key = (label, section_title)
        if group_key not in grouped_bindings:
            grouped_bindings[group_key] = []
        grouped_bindings[group_key].append(gtk_accel)

    app = win.get_application()
    sections = {
        _("General"): [
            (title, " ".join(app.get_accels_for_action(action)))
            for title, action in GENERAL_SHORTCUTS
            if app.get_accels_for_action(action)
        ],
        _("Subtitles"): [],
        _("Audio & Volume"): [],
        _("Navigation"): [],
        _("Display & Video"): [],
        _("Playback"): [],
        _("Miscellaneous"): [],
    }

    for (label, title), accels in grouped_bindings.items():
        target = title if title in sections else _("Miscellaneous")
        # Allows space-separated accelerators
        # e.g. "<Control>q q" shows both shortcuts for the same item
        sections[target].append((label, " ".join(accels)))

    sections = {title: items for title, items in sections.items() if items}

    if hasattr(Adw, "ShortcutsDialog"):
        dialog = Adw.ShortcutsDialog(  # pyright: ignore[reportAttributeAccessIssue]
            content_width=514
        )
        for title, items in sections.items():
            section_widget = Adw.ShortcutsSection(  # pyright: ignore[reportAttributeAccessIssue]
                title=title
            )
            dialog.add(section_widget)
            for label, accels in items:
                section_widget.add(
                    Adw.ShortcutsItem(  # pyright: ignore[reportAttributeAccessIssue]
                        title=label, accelerator=accels
                    )
                )
        dialog.present(win)
        return

    # libadwaita < 1.8 has no ShortcutsDialog, fall back to GTK's own window
    page = Gtk.ShortcutsSection()
    for title, items in sections.items():
        group = Gtk.ShortcutsGroup(title=title)
        page.add_group(group)
        for label, accels in items:
            group.add_shortcut(Gtk.ShortcutsShortcut(title=label, accelerator=accels))
    window = Gtk.ShortcutsWindow(transient_for=win, modal=True)
    window.add_section(page)
    window.present()
