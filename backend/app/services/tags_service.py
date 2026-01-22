from ..state.memory import DOC_TAGS


def get_tags(doc_id: str):
    return DOC_TAGS.get(doc_id, [])


def add_tag(doc_id: str, tag: str):
    if doc_id not in DOC_TAGS:
        DOC_TAGS[doc_id] = []
    if tag not in DOC_TAGS[doc_id]:
        DOC_TAGS[doc_id].append(tag)
    return DOC_TAGS[doc_id]


def remove_tag(doc_id: str, tag: str):
    if doc_id in DOC_TAGS and tag in DOC_TAGS[doc_id]:
        DOC_TAGS[doc_id].remove(tag)
    return DOC_TAGS.get(doc_id, [])