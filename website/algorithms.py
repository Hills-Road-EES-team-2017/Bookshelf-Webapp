

def find_partitions_for_returning_books(books, partitions):
    sorted_partitions = sorted(partitions, key=lambda p: p.user_distance, reverse=False)
    chosen_partitions = []
    for book in books:
        for partition in sorted_partitions:
            if partition.partition_space >= book.book_width:
                chosen_partitions.append(partition)
                partition.partition_space -= book.book_width
                break
    return chosen_partitions
