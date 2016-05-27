# -*- coding: utf-8 -*-
"""Formatting Chinese into HTML with dragonmapper's functions"""


from __future__ import unicode_literals
from dragonmapper import hanzi
from dragonmapper import transcriptions as trans

"""See recomended CSS style: DRAGONMAPPER_DIR/style.css"""


_indentation = 0
_line_html = ''
_puctuation = ['，', '。', '“', '”', '：', '；']
_tones_marks = ['¯', 'ˊ', 'ˇ', 'ˋ', '˙', '1', '2', '3', '4', '5']


def _identify(s):

    """
    Returns string of text type for HTML/CSS.

    *s* is the string to identify.
    """
    if hanzi.has_chinese(s):
        return "hanzi"
    elif s in _puctuation:
        return "punct"
    elif s in _tones_marks:
        return "tone-mark"
    else:
        c = trans.identify(s)
        if c == trans.ZHUYIN:
            return "zhuyin"
        elif c == trans.PINYIN:
            return "pinyin"
        elif c == trans.UNKNOWN:
            return "unknown"


def _stackify(s):

    """
    Stack string for HTML formatting on the left and right of characters.

    *s* is the string to "stackify".
    """

    temp_s = ""
    for c in s:
        temp_s += c + "<br />"
    return temp_s


def _html_add(s, tabs=0):

    """
    Wrapper for _line_html+="..."

    *s* is what to add to the html string.
    *tabs* specifies the identation intensity (in tabs).
    """

    global _line_html
    _line_html += (("\n")+("\t"*(tabs+_indentation)))+s


def _split_punct(zi_s):

    """
    Internal function for spliting punctuation (with spaces
    ... only for HTML formatting.

    *zi_s* specifies the string to preform this action on.
    """

    return zi_s.replace(
        '，', "  ").replace(
        '。', "  ").replace(
        '：', "  ").replace(
        '；', "  ").replace(
        '“', "  ").replace(
        '”', "  ").replace(
        "      ", "     ").replace(
        "    ", "   ").split(' ')


def to_html(characters,
            bottom=None,
            right=None,
            left=None,
            top=None,
            indentation=0,
            keep_puct=True):

    """
    Returns valid HTML for the Chinese characters, and (assumed) phonetic ...
     ... notations provided, on any given side.

    *characters* will be displayed in the middle of each output table.
    *bottom/right/left/bottom* will be displayed on their respective sides ...
     ... of the character
    *indentation* specifies how many extra tab spaces there should be.
    *keep_puct* will make sure that punct is preserved.
    """

    global _indentation
    global _line_html
    _indentation = indentation
    _line_html = ""

    _html_add("<table class=\"chinese-line\">")
    _html_add("<tobdy>", 1)

    if bottom is None:
        bottom = ["" for a, e in enumerate(characters)]
    elif keep_puct:
        bottom = _split_punct(bottom)

    if right is None:
        right = ["" for a, e in enumerate(characters)]
    elif keep_puct:
        right = _split_punct(right)

    if left is None:
        left = ["" for a, e in enumerate(characters)]
    elif keep_puct:
        left = _split_punct(left)

    if top is None:
        top = ["" for a, e in enumerate(characters)]
    elif keep_puct:
        top = _split_punct(top)

    for y in range(0, 3):
        _html_add("<tr>", 2)
        char_num = 0
        for i in range(0, len(characters)*3):
            x = i % 3
            text = ""
            text_type = "unknown"
            # top
            if x == 1 and y == 0:
                text_type = _identify(top[char_num])
                text = top[char_num]
                char_num += 1
            # left
            elif x == 0 and y == 1:
                text_type = _identify(left[char_num])
                text = _stackify(left[char_num])

            # center
            elif x == 1 and y == 1:
                text_type = _identify(characters[char_num])
                text = characters[char_num]

            # right
            elif x == 2 and y == 1:
                text_type = _identify(right[char_num])
                text = _stackify(right[char_num])
                char_num += 1
            # bottom
            elif x == 1 and y == 2:
                text_type = _identify(bottom[char_num])
                text = bottom[char_num]
                char_num += 1

            _html_add("<td class=\"{0}\">".format(text_type), 3)
            _html_add("<span>{0}</span>".format(text), 4)
            _html_add("</td>", 3)

        _html_add("</tr>", 2)
    _html_add("</tbody>", 1)
    _html_add("</table>")
    return _line_html

if __name__ == '__main__':
    zi = '你好，我叫顏毅。'
    zh = hanzi.to_zhuyin(zi)
    pi = trans.zhuyin_to_pinyin(hanzi.to_zhuyin(zi))
    print(to_html(zi, bottom=pi, right=zh))
