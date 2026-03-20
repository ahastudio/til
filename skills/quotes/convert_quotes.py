import sys

filepath = sys.argv[1]
with open(filepath) as f:
    content = f.read()

result = []
open_quote = True
for ch in content:
    if ch == '"':
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
