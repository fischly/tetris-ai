SCORING = {
    'NORMAL': {
        0: 0,
        1: 50, # 0,
        2: 150, # 50,
        3: 300, # 100,
        4: 800 #1000
    },
    
    'TSPIN': {
        0: 50,
        1: 600, #800,
        2: 1200, #1400,
        3: 1600, # 4000,
        4: 2600
    },
    
    'BACKTOBACK_MULTIPLIER': 1.5,
    'COMBO': 50, # 0, 
    'ALL_CLEAR': 3500, # 0,
    
    'GAME_OVER': -5000
}

def calculate_score(cleared_lines, t_spin, all_clear, combo, btb):
    """Calculates the score by considering the number of cleared lines, whether a t-spin was performed and the current combo and back-to-back streaks."""
    # get base score
    score = SCORING['TSPIN' if t_spin else 'NORMAL'][cleared_lines]

    if cleared_lines > 0 and btb > 1:
        score *= SCORING['BACKTOBACK_MULTIPLIER'] * (btb / 2)

    if combo > 1:
        score += SCORING['COMBO'] * (combo - 1)

    if all_clear:
        score += SCORING['ALL_CLEAR']

    return score