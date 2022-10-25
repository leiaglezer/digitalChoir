# chordList: [[C,E,D], [D,F,A], [E,G,B], [F,A,C], [G,B,D], [A,C,E], [B,D,F]]
# chord encoding: A=0, B=1, C=2, D=3, E=4, F=5, G=6
# chord progression we'll use:
# C major: C – E – G
# D minor: D – F – A
# E minor: E – G – B
# F major: F – A – C
# G major: G – B – D
# A minor: A – C – E
# B diminished: B – D – F
pitchList = [0, 1, 2, 3, 4, 5, 6]

#eventually, this can be a slider that switches the scale as demonstrated below

def set_chord_list(scale):
    return {
        'c_major': [[2, 4, 3], [3, 5, 0], [4, 6, 1], [5, 0, 2], [6, 1, 3], [0, 2, 4], [1, 3, 5]],
        'b_major': [[2, 4, 3], [3, 5, 0], [4, 6, 1], [5, 0, 2], [6, 1, 3], [0, 2, 4], [1, 3, 5]], #this is the same
    }[scale]


