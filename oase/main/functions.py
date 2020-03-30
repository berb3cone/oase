def age_interval_calc(age):
    if age < 20:
        return 0
    elif (age // 10) < 7:
        return (age // 10 - 1)
    else:
        return 6

def diet_calc(d):
    if "fat" in d:
        return 0
    elif "carbs" in d:
        return 1
    else:
        return 2

def work_calc(w):
    if "once" in w:
        return 0
    elif "twice" in w:
        return 1
    else:
        return 2

def stress_calc(s):
    if "low" in s:
        return 0
    elif "medium" in s:
        return 1
    else:
        return 2