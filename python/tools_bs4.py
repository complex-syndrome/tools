# Flatten all texts inside a tag
def get_all_texts(tag):
    return [t.strip() for t in tag.stripped_strings] if tag.stripped_strings else []

def get_all_hrefs(tag):
    if a_tags := tag.find_all('a', href=True):
        return [a['href'].strip() for a in a_tags]
    else:
        return []