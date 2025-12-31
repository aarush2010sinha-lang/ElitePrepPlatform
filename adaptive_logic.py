def next_difficulty(current, correct):
    if correct:
        return min(3, current + 1)
    return max(1, current - 1)
