import numpy as np
import math
import sys


class VirtualAddress:
    """
    Maintains a virtual address with its bits for the offset and the bits for
    the page number used to access a page table for logical to physical address
    translation when needed.
    
    Members:

    getPageNumber() -> int

    getOffset() -> str

    getFullAddress() -> str
    """
    def __init__(self, ADDRESS:str, VIRTUAL_ADDRESS_SIZE:int, PAGE_SIZE:int) -> None:
        """
        This method will construct a virtual address which contains an offset in
        the rightmost bits and a page number in the remaining bits to the left.
        
        Parameters:
        ADDRESS: A binary string, representing the virtual address.
        VIRTUAL_ADDRESS_SIZE: An integer representing the maximum size of the
        virtual address space on this given system.
        OFFSET_BITS: An integer representing the number of virtual address
        bits used for the offset.

        Returns:
        None.
        """
        
        OFFSET_BITS = int(math.log(PAGE_SIZE, 2))
        PAGE_BITS = VIRTUAL_ADDRESS_SIZE - OFFSET_BITS
        
        self.__page_number = ADDRESS[0:PAGE_BITS]
        self.__offset = ADDRESS[PAGE_BITS:VIRTUAL_ADDRESS_SIZE]
        self.__full_address = ADDRESS
    
    def getPageNumber(self) -> int:
        """
        This method will cast the binary string representation of the page
        number to its corresponding decimal integer for indexing into an array
        based page table.
        
        Parameters:
        None.
        
        Returns:
        An integer representing the index into the page table at a given page
        number.
        """
        return int(self.__page_number, 2)
    
    def getOffset(self) -> str:
        """
        Parameters:
        None.
        
        Returns:
        The binary string representation of the address's offset.
        """
        return self.__offset

    def getFullAddress(self) -> str:
        """
        Parameters:
        None.

        Returns:
        The binary string representation of the full virtual address referenced
        by self.
        """
        return self.__full_address



def show(pageTable: np.ndarray, sysDesc: tuple[int, int, int]) -> None:
    print(f"N:\t {sysDesc[0]}")
    print(f"M:\t {sysDesc[1]}")
    print(f"SIZE:\t {sysDesc[2]}")

    print("page_table:")
    print(" V P F U")
    for row in pageTable:
        print(row)


def translate(VA:object, PAGE_TABLE:np.ndarray, PHYSICAL_ADDRESS_SIZE:int) -> str:
    """
    This method uses the page table we have constructed to translate a given
    logical / virtual address into the physical address that it refers to.
    
    Parameters:
    - VA: A VirtualAddress object representing the virtual address to be
    translated.
    - PAGE_TABLE: The page table used to translate the given virtual address.
    - PHYSICAL_ADDRESS_SIZE: The size of the physical address space on this
    given system.

    Returns:
    - A string representing the physical address that the given virtual address
    refers to.
    """

    # Define the column indices of page attribute.
    V_IDX = 0
    P_IDX = 1
    F_IDX = 2
    U_IDX = 3

    # Get the page in the page table that the virtual address refers to.
    page = PAGE_TABLE[VA.getPageNumber()]

    # DISK -- Not in Physical Mem, Permission bit not 0.
    if page[V_IDX] == 0 and page[P_IDX] != 0:
        return "DISK"

    # SEGFAULT -- Not in Physical Mem, Lack Permissions.
    elif page[V_IDX] == 0 and page[P_IDX] == 0:
        return "SEGFAULT"

    # Page Hit -- In Physical Mem, Permission bit not 0.
    elif page[V_IDX] == 1 and page[P_IDX] != 0:
        frame = bin(page[F_IDX])[2:]
        physicalAddress = (frame + VA.getOffset()).zfill(PHYSICAL_ADDRESS_SIZE)
        return hex(int(physicalAddress, 2))


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
    page_table = np.delete(data, sys_desc_indices).reshape(-1, 4)

    # Prints Description of System, followed by entries of the page_table.
    # show(pageTable=page_table, sysDesc=(N, M, SIZE))


    # Loop on user input Virtual Addresses (until CTRL-D).
    # while is considerably slower than for.
    for inputLine in sys.stdin:
        VA = 0
        if len(inputLine) > 1 and inputLine[1] == "x":
            hex_str_to_dec_int = int(inputLine, 16)
            bin_int = bin(hex_str_to_dec_int)[2:].zfill(N)
            VA = VirtualAddress(bin_int, N, SIZE)
        else:
            dec_str_to_dec_int = int(inputLine)
            bin_int = bin(dec_str_to_dec_int)[2:].zfill(N)
            VA = VirtualAddress(bin_int, N, SIZE)

        # Translate Virtual Address, VA, to Physical Address.
        print(translate(VA, page_table, M))


if __name__ == "__main__":
    main()