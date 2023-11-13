
def format_query(query: list, duartion: float, losses: int, total: int) -> list:
    '''
    Format the query messages to fix the data with negative differences. This function is needed
    because the query messages are sent with no delay (in contrast to the final result message),
    which means that the messages may not arrive in the correct order.
    The query is copied and the original is not modified. The differences are recalculated.

            Parameters:
                    query (list): List of dictionaries containing the query messages
                    duartion (float): Duration of the test scenario
                    losses (int): Number of lost packets
                    total (int): Total number of packets

            Returns:
                    new_query (list): List of dictionaries containing the query messages
    '''

    # Why is this function needed?
    #   - The query messages are sent with no delay (in contrast to the final result message).
    #   - This means that the messages may not arrive in the correct order (the query message is very small).
    #   - This function fixes the data by looking for negative differences.

    # Check if the query is empty
    if query == []:
        return query

    new_query = query.copy()
    new_query.append({'losses': losses, 'total': total, 'timestamp': duartion, 'difference': (losses - new_query[-1]['losses'])})
    if  not any(report['difference'] < 0 for report in new_query):
        # No negative differences found, return the query as is
        return new_query

    # Negative differences found, we need to fix the data.

    # Iterate through the list and until we find a negative difference
    while any(report['difference'] < 0 for report in new_query):
        current_index = 0
        for idx, current_report in enumerate(new_query):
            if current_report['difference'] < 0:
                # Found a negative difference, fix the data
                for previous_report in new_query[:idx]:
                    # If the previous report has more losses than the current report, we can fix the data
                    if previous_report['losses'] > current_report['losses']:
                        previous_report['losses'] = current_report['losses']
                current_index = idx
                break

        # Recalculate the differences
        for idx, current_report in enumerate(new_query[:current_index+1]):
            if idx == 0:
                current_report['difference'] = current_report['losses']
            else:
                current_report['difference'] = current_report['losses'] - new_query[idx-1]['losses']

    # Reduce the length of the query
    while len(new_query) > 5000:
        # Remove every second element
        new_query = new_query[::2]

    return new_query
