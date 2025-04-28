from collections import Counter

def majority_vote(predictions):
    """
    Determines the most common prediction from a list.

    Args:
        predictions (List[str]): List of predicted class labels.

    Returns:
        str: Final prediction after majority voting.
    """
    vote_counts = Counter(predictions)
    final_prediction = vote_counts.most_common(1)[0]
    return final_prediction[0]

