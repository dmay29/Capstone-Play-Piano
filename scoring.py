def score_notes(correct_notes_dict:dict , played_notes: list[tuple[int,int, int]]):
    correct_notes_dict = correct_notes_dict.copy()
    for note, start, duration, velocity in played_notes:
        
        closest_time = get_closest_time(start, correct_notes_dict.get(note))
        if closest_time is not None:
            correct_start, correct_duration = closest_time
            end = start + duration
            correct_end = correct_start + correct_duration

            overlap_start = max(start, correct_start)
            overlap_end = min(end, correct_end)

            if (overlap_start - correct_start) < .25: overlap_start = correct_start

            overlap_time = max(0, overlap_end - overlap_start)

            score = (overlap_time / correct_duration) * 100

            print(start, correct_start, score)



def get_closest_time(target, times: list[tuple[int, int]]):
    if times is None: return None
    closest = 0
    for i,time in enumerate(times):
        if abs(time[0] - target) < abs(times[closest][0] - target):
            closest = i

    return times[closest]


