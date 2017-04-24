def flatten(items, param):
    output = {}
    for item in items:
        value = getattr(item, param)
        if value in output:
            output[value].append(item)
        else:
            output[value] = [item]
    return output
