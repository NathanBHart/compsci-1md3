def convert(num: str, new_base: int, original_base: int=10) -> str:
    '''
    convert(num:str, new_base:int, original_base:int=10)
    
    Takes a string number and converts it to a new base from an
    original base, supplied as integers. Returns number as a string in
    the new base. Cannot convert to or from a base larger than 36.
    '''

    largest_base = max(new_base, original_base) 

    if largest_base > 36: # Standard is not defined for larger bases
        raise TypeError(
            'Cannot convert to or from a base larger than 36'
        ) from TypeError

    values = "0123456789abcdefghijklmnopqrstuvwxyz"
    value_dict = {values[i]: i
        for i in range(largest_base)
    }

    x = num.lower()

    # Converts string from original base to numeric value
    accu = 0
    rev = x[::-1]
    for i in range(len(rev)):
        accu += value_dict[rev[i]] * (original_base**i)

    key_dict = {i: values[i] for i in range(len((values)))}

    # Converts numeric value to string of new base
    i = 0
    rem = accu
    str_val = "" if rem > 0 else "0"
    while rem > 0:
        str_val = key_dict[rem % new_base] + str_val
        rem = rem // new_base
        i += 1

    return str_val
