MAX_SCORE_PER_NOTE = 100
MAX_PENALTY_PER_NOTE = -MAX_SCORE_PER_NOTE
MAX_SCORE_START_NOTE = MAX_SCORE_PER_NOTE / 2
MAX_PENALTY_START_NOTE = MAX_SCORE_START_NOTE
MAX_SCORE_STOP_NOTE = MAX_SCORE_PER_NOTE / 2
MAX_PENALTY_STOP_NOTE = MAX_SCORE_STOP_NOTE

def score_notes(correct_notes_dict:dict , played_notes: list[tuple[int,int, int]]):
    score = 0
    correct_notes_dict = correct_notes_dict.copy()
    # total_notes = sum([len(notes) for notes in correct_notes_dict.values() if notes is not None])
    for note in played_notes:
        score += score_note(correct_notes_dict, note)
    print(score)

def score_note(correct_notes_dict:dict , played_notes:tuple[int,int, int]):
    score = 0
    note, start, duration, velocity = played_notes 
    print(note)
    closest_time = get_closest_time(start, correct_notes_dict.get(note))
    if closest_time is not None:
        correct_start, correct_duration = closest_time
        end = start + duration
        correct_end = correct_start + correct_duration

        start_off_by = start - correct_start
        end_off_by = end - correct_end

        
        if abs(start_off_by) < .1:
            score += MAX_SCORE_START_NOTE
        elif abs(start_off_by) < .5:
            score += ((abs(start_off_by) - .1)/.4) * MAX_SCORE_START_NOTE
        else:
            score -= MAX_PENALTY_START_NOTE

        if abs(end_off_by) < .1:
            score += MAX_SCORE_STOP_NOTE
        elif abs(end_off_by) < .4:
            score += ((abs(end_off_by) - .1)/.3) * MAX_SCORE_STOP_NOTE
        else:
            score += MAX_PENALTY_STOP_NOTE

        print(score, start_off_by, end_off_by, sep=", ")
    else:
        score += -MAX_SCORE_PER_NOTE
    
    return score

def getMaxScore(correct_notes_dict:dict):
    score = 0
    for note_timings in correct_notes_dict.values():
        try:
            score += len(note_timings) * MAX_SCORE_PER_NOTE
        except TypeError:
            pass

    return score


def get_closest_time(target, times: list[tuple[int, int]]):
    if times is None: return None
    closest = 0
    for i,time in enumerate(times):
        if abs(time[0] - target) < abs(times[closest][0] - target):
            closest = i

    return times[closest]


