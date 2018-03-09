

def find_partitions_for_returning_books(books, partitions):
    sorted_partitions = sorted(partitions, key=lambda p: p.distance, reverse=False)
    chosen_partitions = []
    for book in books:
        for partition in sorted_partitions:
            if partition.space>=book.width:
                chosen_partitions.append(partition)
                partition.space -= book.width
                break
    return chosen_partitions
