# This file contains an implementation for Part A of the project that was
# used explore inheritence in Python and was ultimately abandonded once the
# super() rabbit hole was determined to be too deep.
# It passes theBigDiffer just the same as partA.py does.

import numpy as np
import math
import sys

class System:
    def __init__(self) -> None:
        # Open Input File for a Page Table.
        inFile = open(sys.argv[1])
        data = np.array(inFile.read().split(), dtype=int)
        inFile.close()

        # Description of System.
        sys_desc_indices = [0, 1, 2]
        self.__virtualAddressSize = data[0] # Number of bits in Virtual Address.
        self.__physicalAddressSize = data[1] # Number of bits in Physical Address.
        self.__pageSize = data[2] # Number of bytes in a single page.
        self.__numOffsetBits = int(math.log(self.__pageSize, 2))
        self.__numPageBits = self.__virtualAddressSize - self.__numOffsetBits

        # Drop N, M, SIZE, and reshape to have rows of 4 columns each.
        data = np.reshape(np.delete(data, sys_desc_indices), (-1, 4))

        # PT Dictionary -- { "00" : [1, 3, 2, 1], "01" : [0, 2, 4, 0], ... }.
        pageTable = {}
        for i in range(0, len(data)):
            pg_num = bin(i)[2:].zfill(self.__numPageBits)
            pageTable[pg_num] = data[i]
        
        self.__pageTable = pageTable
    
    def getVirtualAddressSize(self) -> int:
        return self.__virtualAddressSize

    def getPhysicalAddressSize(self) -> int:
        return self.__physicalAddressSize

    def getPageSize(self) -> int:
        return self.__pageSize

    def getNumPageBits(self) -> int:
        return self.__numPageBits
    
    def getNumOffsetBits(self) -> int:
        return self.__numOffsetBits
    
    def getPageTable(self) -> dict:
        return self.__pageTable
    
    def setPageTable(self, pageTable) -> None:
        self.__pageTable = pageTable
    
    def printTable(self) -> None:
        for page in self.__pageTable:
            print(f"{page} : {self.__pageTable[page]}")



class VirtualAddress(System):
    def __init__(self, ADDRESS:str) -> None:
        super().__init__() # Super is really weird...
        
        self.__pageNumber = ADDRESS[0:self.getNumPageBits()]
        self.__offset = ADDRESS[self.getNumPageBits():self.getVirtualAddressSize()]
        self.__fullAddress = ADDRESS
    
    def getPageNumber(self) -> str:
        return self.__pageNumber
    
    def getOffset(self) -> str:
        return self.__offset

    def getFullAddress(self) -> str:
        return self.__fullAddress

    def getPhysicalAddress(self) -> str:
        M = self.getPhysicalAddressSize()

        # Define the column indices of page attribute.
        V_IDX = 0
        P_IDX = 1
        F_IDX = 2
        U_IDX = 3

        page = self.getPageTable()[self.__pageNumber]

        # DISK -- Not in Physical Mem, Permission bit not 0.
        if page[V_IDX] == 0 and page[P_IDX] != 0:
            return "DISK"

        # SEGFAULT -- Not in Physical Mem, Lack Permission.
        elif page[V_IDX] == 0 and page[P_IDX] == 0:
            return "SEGFAULT"

        # Page Hit
        elif page[V_IDX] == 1 and page[P_IDX] != 0:
            frame = bin(page[F_IDX])[2:]
            physicalAddress = (frame + self.__offset).zfill(M)
            return hex(int(physicalAddress, 2))


def main():
    system = System()

    N = system.getVirtualAddressSize()
    
    # Loop on User Input (Crtl+D).
    try:
        while(True):

            # Get Virtual Address.
            VA = 0
            userInput = input()
            if len(userInput) > 1 and userInput[1] == "x":
                hex_str_to_dec_int = int(userInput, 16)
                bin_int = bin(hex_str_to_dec_int)[2:].zfill(N)
                VA = VirtualAddress(bin_int)
            else:
                dec_str_to_dec_int = int(userInput)
                bin_int = bin(dec_str_to_dec_int)[2:].zfill(N)
                VA = VirtualAddress(bin_int)

            # Translate Virtual Address, VA, to Physical Address.
            print(VA.getPhysicalAddress())

    except EOFError as e:
        1 + 1
        # print(e)


if __name__ == "__main__":
    main()