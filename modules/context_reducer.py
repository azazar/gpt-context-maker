from modules import token_counter

def reduce_context(summaries, limit=2048):
    # Get token count for each summary
    token_counts = [(token_counter.count_tokens(s.get("file_content", "") + ''.join(s.values())), s) for s in summaries]

    # Sort summaries by token count
    sorted_summaries = sorted(token_counts, key=lambda x: x[0])

    # Drop the largest summaries until we fit into the limit
    total_tokens = sum(count for count, _ in sorted_summaries)
    while total_tokens > limit and sorted_summaries:
        total_tokens -= sorted_summaries.pop()[0]

    # Return the reduced list of summaries
    return [summary for _, summary in sorted_summaries]
