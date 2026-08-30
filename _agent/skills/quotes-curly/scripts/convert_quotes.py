import sys
from itertools import accumulate
from typing import Iterator, Sequence

LEFT_QUOTE = '“'
RIGHT_QUOTE = '”'
STRAIGHT_QUOTE = '"'
FENCE_MARKER = '```'


def is_fence_marker(line: str) -> bool:
    return line.lstrip().startswith(FENCE_MARKER)


def toggle_fence_state(in_fenced_code_block: bool) -> bool:
    return not in_fenced_code_block


def next_open_quote(open_quote: bool) -> bool:
    return not open_quote


def curly_quote(open_quote: bool) -> str:
    if open_quote:
        return LEFT_QUOTE
    return RIGHT_QUOTE


def convert_char(ch: str, open_quote: bool) -> tuple[str, bool]:
    if ch != STRAIGHT_QUOTE:
        return ch, open_quote
    return curly_quote(open_quote), next_open_quote(open_quote)


def quote_states(line: str, open_quote: bool) -> Iterator[bool]:
    """
    >>> list(quote_states('ab"cd"', True))
    [True, True, True, False, False, False, True]

    >>> list(quote_states('', True))
    [True]

    >>> all(quote_states('no quotes here', True))
    True

    >>> list(quote_states('"a" "b" "c" "d"', True))[-1]
    True
    """
    return accumulate(
        line, lambda quote, ch: next_open_quote(quote) if ch == STRAIGHT_QUOTE else quote,
        initial=open_quote,
    )


def convert_line(line: str, in_fenced_code_block: bool, open_quote: bool) -> str:
    """
    >>> convert_line('a"b"c', False, True)
    'a“b”c'

    >>> convert_line('"skip"', True, True)
    '"skip"'

    >>> convert_line('', False, True)
    ''

    >>> convert_line('plain text, no quotes', False, True)
    'plain text, no quotes'

    >>> convert_line('unterminated "quote', False, True)
    'unterminated “quote'

    >>> convert_line('"a" "b" "c" "d"', False, True)
    '“a” “b” “c” “d”'
    """
    if in_fenced_code_block:
        return line

    return ''.join(
        convert_char(ch, quote)[0]
        for ch, quote in zip(line, quote_states(line, open_quote))
    )


LineState = tuple[bool, bool]


def next_line_state(state: LineState, line: str) -> LineState:
    """
    >>> next_line_state((False, True), 'a"b"')
    (False, True)

    >>> next_line_state((False, True), '```')
    (True, True)
    """
    in_fenced_code_block, open_quote = state
    if is_fence_marker(line):
        return toggle_fence_state(in_fenced_code_block), open_quote

    if in_fenced_code_block:
        return in_fenced_code_block, open_quote

    final_quote_state = list(quote_states(line, open_quote))[-1]
    return in_fenced_code_block, final_quote_state


def line_states(lines: Sequence[str], in_fenced_code_block: bool, open_quote: bool) -> Iterator[LineState]:
    """
    >>> list(line_states(['a"b"\\n', '"c"\\n'], False, True))
    [(False, True), (False, True), (False, True)]
    """
    return accumulate(
        lines, next_line_state, initial=(in_fenced_code_block, open_quote)
    )


def convert_content(content: str) -> str:
    """
    각 줄을 변환해 다시 이어붙인다.
    줄바꿈 보존과 펜스 블록에 걸친 상태 전파를 확인한다.

    >>> convert_content('"hello" world\\n"open across\\n```\\ncode "stays"\\n```\\nlines" end\\n')
    '“hello” world\\n“open across\\n```\\ncode "stays"\\n```\\nlines” end\\n'

    >>> convert_content('')
    ''
    """
    lines = content.splitlines(keepends=True)
    states_before_each_line = list(line_states(lines, False, True))[:-1]

    converted_lines = [
        convert_line(line, in_fenced_code_block, open_quote)
        for line, (in_fenced_code_block, open_quote) in zip(lines, states_before_each_line)
    ]

    return ''.join(converted_lines)


def read_file(filepath: str) -> str:
    try:
        with open(filepath, encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise SystemExit(f'Error: file not found: {filepath}')
    except IsADirectoryError:
        raise SystemExit(f'Error: not a file: {filepath}')
    except PermissionError:
        raise SystemExit(f'Error: permission denied reading: {filepath}')
    except UnicodeDecodeError as e:
        raise SystemExit(f'Error: {filepath} is not valid UTF-8 text: {e}')


def write_file(filepath: str, content: str) -> None:
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except PermissionError:
        raise SystemExit(f'Error: permission denied writing: {filepath}')
    except OSError as e:
        raise SystemExit(f'Error: failed to write {filepath}: {e}')


def print_quote_counts(content: str) -> None:
    count_straight = content.count(STRAIGHT_QUOTE)
    count_left = content.count(LEFT_QUOTE)
    count_right = content.count(RIGHT_QUOTE)
    print(f'Straight quotes remaining: {count_straight}')
    print(f'Left curly quotes ({LEFT_QUOTE}): {count_left}')
    print(f'Right curly quotes ({RIGHT_QUOTE}): {count_right}')
    if count_left != count_right:
        print(
            f'Warning: unbalanced curly quotes '
            f'({count_left} left vs {count_right} right). '
            f'Check for an odd number of straight quotes in the source.',
            file=sys.stderr,
        )


def require_filepath_arg(argv: Sequence[str]) -> str:
    if len(argv) < 2:
        raise SystemExit(f'Usage: {argv[0]} <filepath>')
    return argv[1]


def convert_file(filepath: str) -> None:
    content = read_file(filepath)
    new_content = convert_content(content)
    write_file(filepath, new_content)
    print_quote_counts(new_content)


def is_test_run(argv: Sequence[str]) -> bool:
    return len(argv) > 1 and argv[1] == '--test'


def run_tests() -> None:
    import doctest
    results = doctest.testmod(verbose=True)
    if results.failed:
        raise SystemExit(1)


def main() -> None:
    if is_test_run(sys.argv):
        run_tests()
        return

    filepath = require_filepath_arg(sys.argv)
    convert_file(filepath)


if __name__ == '__main__':
    main()
