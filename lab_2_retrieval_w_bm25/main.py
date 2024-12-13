"""
Lab 2.
Text retrieval with BM25
"""
# pylint:disable=too-many-arguments, unused-argument
import math
def tokenize(text: str) -> list[str] | None:
    """
    Tokenize the input text into lowercase words without punctuation, digits and other symbols.
    Args:
        text (str): The input text to tokenize.
    Returns:
        list[str] | None: A list of words from the text.
    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(text, str):
        return None
    for item in text:
        if not (item.isalpha() or
                item == " " or
                item == "\n"):
            text = text.replace(item, " ")
            
    return text.lower().split()


def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str] | None:
    """
    Remove stopwords from the list of tokens.
    Args:
        tokens (list[str]): List of tokens.
        stopwords (list[str]): List of stopwords.
    Returns:
        list[str] | None: Tokens after removing stopwords.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(tokens, list) and
            len(tokens) > 0 and
            all(isinstance(token, str) for token in tokens) and
            isinstance(stopwords, list) and
            len(stopwords) > 0 and
            all(isinstance(word, str) for word in stopwords)):
        return None
    new_tokens = [token for token in tokens if not token in stopwords]
    return new_tokens


def build_vocabulary(documents: list[list[str]]) -> list[str] | None:
    """
    Build a vocabulary from the documents.
    Args:
        documents (list[list[str]]): List of tokenized documents.
    Returns:
        list[str] | None: List with unique words from the documents.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(documents, list) and
            len(documents) > 0 and
            all(isinstance(doc, list) for doc in documents)):
        return None
    set_of_words = set()
    for doc in documents:
        if all(isinstance(token, str) for token in doc):
            set_of_words = set_of_words | set(doc)
            
        else:
            return None
    return list(set_of_words)
def calculate_tf(vocab: list[str], document_tokens: list[str]) -> dict[str, float] | None:
    """
    Calculate term frequency for the given tokens based on the vocabulary.
    Args:
        vocab (list[str]): Vocabulary list.
        document_tokens (list[str]): Tokenized document.
    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to their term frequency.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(vocab, list) and
            len(vocab) > 0 and
            all(isinstance(word, str) for word in vocab) and
            isinstance(document_tokens, list) and
            len(document_tokens) > 0 and
            all(isinstance(token, str) for token in document_tokens)):
        return None
    frequency_dict = dict.fromkeys(document_tokens + vocab, 0.0)
    for word in document_tokens:
        frequency_dict[word] = document_tokens.count(word) / len(document_tokens)
    return frequency_dict
def calculate_idf(vocab: list[str], documents: list[list[str]]) -> dict[str, float] | None:
    """
    Calculate inverse document frequency for each term in the vocabulary.
    Args:
        vocab (list[str]): Vocabulary list.
        documents (list[list[str]]): List of tokenized documents.
    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to its IDF scores.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(vocab, list) and
            len(vocab) > 0 and
            all(isinstance(word, str) for word in vocab) and
            isinstance(documents, list) and
            len(documents) > 0 and
            all(isinstance(doc, list) for doc in documents)):

        return None
    for doc in documents:
        if not all(isinstance(word, str) for word in doc):
            return None
    idf = {}
    for word in vocab:
        docs_w_word = len([True for doc in documents if word in doc])
        idf[word] = math.log((len(documents) - docs_w_word + 0.5) / (docs_w_word + 0.5))
    return idf
def calculate_tf_idf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float] | None:
    """
    Calculate TF-IDF scores for a document.
    Args:
        tf (dict[str, float]): Term frequencies for the document.
        idf (dict[str, float]): Inverse document frequencies.
    Returns:
        dict[str, float] | None: Mapping from terms to their TF-IDF scores.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(tf, dict) and
            len(tf) > 0 and
            all(isinstance(key, str) and isinstance(tf[key], float) for key in tf) and
            isinstance(idf, dict) and
            len(idf) > 0 and
            all(isinstance(key, str) and isinstance(idf[key], float) for key in idf)):
        return None
    tf_idf = {}
    for key in tf:
        if key in idf:
            tf_idf[key] = tf[key] * idf[key]
        else:
            return None
    return tf_idf
def calculate_bm25(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document.
    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.
    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(vocab, list) and
            len(vocab) > 0 and
            isinstance(document, list) and
            len(document) > 0 and
            isinstance(idf_document, dict) and
            len(idf_document) > 0):
        return None
    if not (isinstance(k1, float) and
            isinstance(b, float) and
            isinstance(avg_doc_len, float) and
            avg_doc_len > 0 and
            isinstance(doc_len, int) and
            doc_len is not True):
        return None
    if not (all(isinstance(word, str) for word in vocab) and
            all(isinstance(word, str) for word in document) and
            all(isinstance(key, str) and
                isinstance(idf_document[key], float) for key in idf_document)):
        return None
    result_dict = {}
    for word in set(idf_document) | set(document):
        amount = document.count(word)
        value = 0.0
        if word in idf_document:
            value = (idf_document[word] *
                    (amount * (k1 + 1)) /
                    (amount + k1 * (1 - b + b * doc_len / avg_doc_len)))
        result_dict[word] = value
    return result_dict
def rank_documents(
    indexes: list[dict[str, float]], query: str, stopwords: list[str]
) -> list[tuple[int, float]] | None:
    """
    Rank documents for the given query.
    Args:
        indexes (list[dict[str, float]]): List of BM25 or TF-IDF indexes for the documents.
        query (str): The query string.
        stopwords (list[str]): List of stopwords.
    Returns:
        list[tuple[int, float]] | None: Tuples of document index and its score in the ranking.
    In case of corrupt input arguments, None is returned.
    """
    if not (isinstance(indexes, list) and
            all(isinstance(index, dict) for index in indexes) and
            isinstance(query, str) and
            isinstance(stopwords, list) and
            all(isinstance(word, str) for word in stopwords)):
        return None
    if not (len(indexes) > 0 and len(stopwords) > 0 and len(query) > 0):
        return None

    tokenized_query = tokenize(query)
    if not isinstance(tokenized_query, list):
        return None
    query_to_compare = remove_stopwords(tokenized_query, stopwords)
    if not isinstance(query_to_compare, list):
        return None

    doc_sums = []
    for doc_num, doc in enumerate(indexes):
        values_sum = 0.0
        for token in query_to_compare:
            if token in doc:
                values_sum += doc[token]
        doc_sums.append((doc_num, values_sum))
    doc_sums.sort(reverse=True, key=lambda a: a[1])
    return doc_sums

def calculate_bm25_with_cutoff(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    alpha: float,
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document with IDF cutoff.
    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        alpha (float): IDF cutoff threshold.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.
    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores with cutoff applied.
    In case of corrupt input arguments, None is returned.
    """
def save_index(index: list[dict[str, float]], file_path: str) -> None:
    """
    Save the index to a file.
    Args:
        index (list[dict[str, float]]): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """
def load_index(file_path: str) -> list[dict[str, float]] | None:
    """
    Load the index from a file.
    Args:
        file_path (str): The path to the file from which to load the index.
    Returns:
        list[dict[str, float]] | None: The loaded index.
    In case of corrupt input arguments, None is returned.
    """
def calculate_spearman(rank: list[int], golden_rank: list[int]) -> float | None:
    """
    Calculate Spearman's rank correlation coefficient between two rankings.
    Args:
        rank (list[int]): Ranked list of document indices.
        golden_rank (list[int]): Golden ranked list of document indices.
    Returns:
        float | None: Spearman's rank correlation coefficient.
    In case of corrupt input arguments, None is returned.
    """
