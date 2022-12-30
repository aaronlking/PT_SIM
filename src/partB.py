import numpy as np
import math
import sys


class VirtualAddress:
    def __init__(self, ADDRESS:str, VIRTUAL_ADDRESS_SIZE:int, PAGE_SIZE:int) -> None:
        OFFSET_BITS = int(math.log(PAGE_SIZE, 2))
        PAGE_BITS = VIRTUAL_ADDRESS_SIZE - OFFSET_BITS
        
        self.__page_number = ADDRESS[0:PAGE_BITS]
        self.__offset = ADDRESS[PAGE_BITS:VIRTUAL_ADDRESS_SIZE]
        self.__full_address = ADDRESS
    
    def getPageNumber(self) -> int:
        return int(self.__page_number, 2)
    
    def getOffset(self) -> str:
        return self.__offset

    def getFullAddress(self) -> str:
        return self.__full_address

def show(pageTable: np.ndarray, sysDesc: tuple[int, int, int]) -> None:
    print("N:\t", sysDesc[0])
    print("M:\t", sysDesc[1])
    print("SIZE:\t", sysDesc[2])

    print("page_table:")
    print(" V P F U")
    for row in pageTable:
        print(row)


def translate(VA, page_table, clockQ, PHYSICAL_ADDRESS_SIZE) -> str:

    # Used to index into a page (V P F U).
    V_IDX = 0
    P_IDX = 1
    F_IDX = 2
    U_IDX = 3

    page = page_table[VA.getPageNumber()]

    # DISK -- Not in Physical Mem, Permission bit not 0.
    if page[V_IDX] == 0 and page[P_IDX] != 0:

        if not clockQ:
            print("No valid frames to evict.")
            sys.exit(1)

        (clockQ, page_table) = evict(VA.getPageNumber(), clockQ, page_table)

        frame = bin(page[F_IDX])[2:]
        physicalAddress = (frame + VA.getOffset()).zfill(PHYSICAL_ADDRESS_SIZE)
        
        print(f"PAGEFAULT {hex(int(physicalAddress, 2))}")


    # SEGFAULT -- Not in Physical Mem, Lack Permission.
    elif page[V_IDX] == 0 and page[P_IDX] == 0:
        print("SEGFAULT")

    # Page Hit
    elif page[V_IDX] == 1 and page[P_IDX] != 0:
        page_table[VA.getPageNumber()][U_IDX] = 1
        frame = bin(page[F_IDX])[2:]
        physicalAddress = (frame + VA.getOffset()).zfill(PHYSICAL_ADDRESS_SIZE)
        print(hex(int(physicalAddress, 2)))


def evict(reqPage: str, clockQ: list, page_table: np.ndarray):
    """
    This method will modify the page table state and clockQ state to reflect an
    eviction. An eviction takes place when there is no room in the page table to
    store a physical address and we must replace one of the physical addresses
    already in memory.

    Parameters:
    reqPage: The page in the page table that the virtual address is using to
    reference the physical frame.
    clockQ: State of the clockQ before the eviction has taken place.
    page_table: The page_table being used for address translation.
    
    Returns:
    clockQ: State after eviction.  
    page_table: State after eviction.
    """

    # Used to index into a page (V P F U).
    V_IDX = 0
    P_IDX = 1
    F_IDX = 2
    U_IDX = 3
    
    # Get the first page in the clockQ.
    page2evict = clockQ.pop(0)
    
    # Find the next page in the clockQ that is not in use.
    while page2evict[U_IDX] == 1:
        page2evict[U_IDX] = 0
        clockQ.append(page2evict)
        page2evict = clockQ.pop(0)
    
    # Update the page table to reflect the eviction.
    page_table[reqPage][V_IDX] = 1 # Step One: Set valid bit of incoming page.
    page_table[reqPage][F_IDX] = page2evict[F_IDX] # Step Two: Set frame.
    page_table[reqPage][U_IDX] = 1 # Step Three: Set dirty bit of incoming page.
    clockQ.append(page_table[reqPage])

    page2evict[V_IDX] = 0

    return (clockQ, page_table)
        



def main():
    # Open the input file containing the system description and initial page
    # table state.
    with open(sys.argv[1], "r") as f:
        data = np.array(f.read().split(), dtype=int)


    # Get Description of System.
    N = int(data[0]) # Number of bits in Virtual Address.
    M = int(data[1]) # Number of bits in Physical Address.
    SIZE = int(data[2]) # Number of bytes in a single page.

    # Remove the first 3 elements (N, M, SIZE) from data,
    # reshaping the remaining rows to be 4 columns.
    sys_desc_indices = [0, 1, 2]
    pageTable = np.reshape(np.delete(data, sys_desc_indices), (-1, 4))


    # Initialize ClockQueue of valid frames from the pageTable.
    clockQ = []
    for page in pageTable:
        if page[0] == 1:
            clockQ.append(page)

    # Prints Description of System, followed by entries of the pageTable.
    # show(pageTable=pageTable, sysDesc=(N, M, SIZE))


    # Loop on user input Virtual Addresses (until CTRL-D).
    for inputLine in sys.stdin:

        # Get Virtual Address.
        VA = 0
        if len(inputLine) > 1 and inputLine[1] == "x":
            hex_str_to_dec_int = int(inputLine, 16)
            bin_int = bin(hex_str_to_dec_int)[2:].zfill(N)
            VA = VirtualAddress(bin_int, N, SIZE)
        else:
            dec_str_to_dec_int = int(inputLine)
            bin_int = bin(dec_str_to_dec_int)[2:].zfill(N)
            VA = VirtualAddress(bin_int, N, SIZE)

        # Translate Virtual Address to Physical Address.
        translate(VA, pageTable, clockQ, M)


if __name__ == "__main__":
    main()