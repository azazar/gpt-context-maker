from modules import token_counter


def reduce_context(summaries, max_tokens=2048):
    # Get token count for each summary
    token_counts = [(token_counter.count_tokens(s.get("file_content", "") + ''.join([item for sublist in [
                     v if isinstance(v, list) else [v] for v in s.values()] for item in sublist])), s) for s in summaries]

    # Sort summaries by token count
    sorted_summaries = sorted(token_counts, key=lambda x: x[0])

    # Drop the largest summaries until we fit into the limit
    total_tokens = sum(count for count, _ in sorted_summaries)
    while total_tokens > max_tokens and sorted_summaries:
        removed_file_summary = sorted_summaries.pop()
        total_tokens -= removed_file_summary[0]
        print(f"WARNING: File '{removed_file_summary[1]['filename']}' was removed from context due to token limit.")

    # Return the reduced list of summaries
    return [summary for _, summary in sorted_summaries]
