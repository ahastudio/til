import sys

filepath = sys.argv[1]
with open(filepath) as f:
    content = f.read()

result = []
open_quote = True
in_fenced_code_block = False

for line in content.splitlines(keepends=True):
    if line.lstrip().startswith('```'):
        in_fenced_code_block = not in_fenced_code_block
        result.append(line)
        continue

    for ch in line:
        if ch == '"' and not in_fenced_code_block:
            if open_quote:
                result.append('\u201c')
            else:
                result.append('\u201d')
            open_quote = not open_quote
        else:
            result.append(ch)

new_content = ''.join(result)

with open(filepath, 'w') as f:
    f.write(new_content)

count_straight = new_content.count('"')
count_left = new_content.count('\u201c')
count_right = new_content.count('\u201d')
print(f'Straight quotes remaining: {count_straight}')
print(f'Left curly quotes (\u201c): {count_left}')
print(f'Right curly quotes (\u201d): {count_right}')
