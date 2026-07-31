class Bin:

    def __init__(self, capacity):
        self.capacity = capacity
        self.remaining_space = capacity
        self.items = []

    def can_fit(self, item_size):
        return self.remaining_space >= item_size

    def add_item(self, item_size):
        if self.can_fit(item_size):
            self.items.append(item_size)
            self.remaining_space -= item_size
            return True
        return False

    def __repr__(self):
        return f"Bin(items={self.items}, remaining={self.remaining_space})"


def first_fit(items, capacity):
    """First Fit (FF) Bin Packing Algorithm"""
    bins = []

    for item in items:
        placed = False
        # Try to place item in the first bin that can fit it
        for bin_obj in bins:
            if bin_obj.can_fit(item):
                bin_obj.add_item(item)
                placed = True
                break

        # If item doesn't fit in any existing bin, open a new bin
        if not placed:
            new_bin = Bin(capacity)
            new_bin.add_item(item)
            bins.append(new_bin)

    return bins


def first_fit_decreasing(items, capacity):
    """First Fit Decreasing (FFD) Bin Packing Algorithm"""
    # Sort items in decreasing order
    sorted_items = sorted(items, reverse=True)
    return first_fit(sorted_items, capacity)


def best_fit_decreasing(items, capacity):
    """Best Fit Decreasing (BFD) Bin Packing Algorithm"""
    # Sort items in decreasing order
    sorted_items = sorted(items, reverse=True)
    bins = []

    for item in sorted_items:
        best_bin = None
        min_space_left = capacity + 1

        # Find the bin with the minimum remaining space that can still fit the item
        for bin_obj in bins:
            if bin_obj.can_fit(item):
                space_left_after = bin_obj.remaining_space - item
                if space_left_after < min_space_left:
                    min_space_left = space_left_after
                    best_bin = bin_obj

        # If a suitable bin exists, place the item there
        if best_bin is not None:
            best_bin.add_item(item)
        else:
            # Otherwise, open a new bin
            new_bin = Bin(capacity)
            new_bin.add_item(item)
            bins.append(new_bin)

    return bins


# --- Execution ---
if __name__ == "__main__":
    # Test Data
    items = [4, 8, 1, 4, 2, 1, 7, 6]
    capacity = 10

    print(f"Items   : {items}")
    print(f"Capacity: {capacity}")
    print("-" * 50)

    # 1. First Fit
    ff_bins = first_fit(items, capacity)
    print(f"First Fit (FF)            : {len(ff_bins)} Bins")
    for idx, b in enumerate(ff_bins, 1):
        print(f"   Bin {idx}: {b.items} (Remaining: {b.remaining_space})")

    print("-" * 50)

    # 2. First Fit Decreasing
    ffd_bins = first_fit_decreasing(items, capacity)
    print(f"First Fit Decreasing (FFD): {len(ffd_bins)} Bins")
    for idx, b in enumerate(ffd_bins, 1):
        print(f"   Bin {idx}: {b.items} (Remaining: {b.remaining_space})")

    print("-" * 50)

    # 3. Best Fit Decreasing
    bfd_bins = best_fit_decreasing(items, capacity)
    print(f"Best Fit Decreasing (BFD) : {len(bfd_bins)} Bins")
    for idx, b in enumerate(bfd_bins, 1):
        print(f"   Bin {idx}: {b.items} (Remaining: {b.remaining_space})")