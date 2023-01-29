from constants import FILE_PATH_VIETNAMESE_STOPWORDS


def get_stop_words():
    """
    Get stop words from file.
    """
    stop_words = []
    with open(FILE_PATH_VIETNAMESE_STOPWORDS, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            stop_words.append(line.strip())
    return stop_words


stopwords = get_stop_words()
