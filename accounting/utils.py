

def leftpad_table(title, rows, offset=3):
    acc = ''
    longest_by_col = [0] * len(rows[0])
    for row in rows:
        for i, col in enumerate(row):
            len_col = len(col)
            if len_col > longest_by_col[i]:
                longest_by_col[i] = len_col

    acc = title
    for row in rows:
        acc += '\n'
        for i, col in enumerate(row):
            target_len = longest_by_col[i] + offset
            acc += (" " * (target_len - len(col))) + col

    return acc
