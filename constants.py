from io import TextIOWrapper
import json
from typing import Union

class Logs:
    class Good:
        pass

    class Static:
        pass

    class Warning:
        pass

    class Error:
        pass


class Interface:
    process: bool = False
    timer: int = 0
    
    symbols_done: int = 0
    symbols_left: int = 0
    symbols_per_second: int = 0

    last_print_speeds: list = []
    print_speed: int = 0


class Text:
    text: list = []
    current_text_id: int
    current_symbol: int = 0

    _last_symbol_was_ok: bool = True

    with open('examples.json', 'r') as __text_file:
        __text_file_json: dict = json.load(__text_file)
        for __key in __text_file_json.keys():
            text.append(__text_file_json[__key])
        del __text_file_json
        del __text_file
        del __key

    def check_symbol(_symbol_to_check: str, ) -> list:
        _text = list(Text.text[Text.current_text_id])
        if Text.text[Text.current_text_id][Text.current_symbol] == _symbol_to_check:
            _text_str = ''.join(_text[0:Text.current_symbol]) + f'<span style="background-color: #45c44d;">{_text[Text.current_symbol]}</span>' + ''.join(_text[Text.current_symbol + 1:-1])
            Text.current_symbol += 1

            return [True, _text_str]
        else:
            _text_str = ''.join(_text[0:Text.current_symbol]) + f'<span style="background-color: #801818;">{_text[Text.current_symbol]}</span>' + ''.join(_text[Text.current_symbol + 1:-1])
            
            # Добавить уменьшение текущего символа на Backspace
            return [False, _text_str]

    def _move_to_the_next_symbol():
        pass


