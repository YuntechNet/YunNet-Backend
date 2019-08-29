def big5_encode(s: str):
    return s.encode("big5").decode("ascii", "surrogateescape")
