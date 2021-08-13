def incrementor():
    info = {"count": 100}
    def number():
        info["count"] += 1
        return info["count"]
    return number
