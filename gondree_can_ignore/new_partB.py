# This file contains an implementation for Part B of the project that was
# used explore inheritence in Python and was ultimately abandonded once the
# super() rabbit hole was determined to be too deep.

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
        
        clockQ = []
        for page in pageTable:
            if pageTable[page][0] == 1:
                clockQ.append(pageTable[page])
        
        self.__pageTable = pageTable
        self.__clockQ = clockQ
    
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

    def getClockQ(self):
        return self.__clockQ
    
    def setClockQ(self, clockQ) -> None:
        self.__clockQ = clockQ
    
    def printTable(self) -> None:
        for page in self.__pageTable:
            print(f"{page} : {self.__pageTable[page]}")



class VirtualAddress(System):
    def __init__(self, ADDRESS:str) -> None:
        super().__init__()  
        
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
        page_table = self.getPageTable()
        clockQ = self.getClockQ()

        # Define the column indices of page attribute.
        V_IDX = 0
        P_IDX = 1
        F_IDX = 2
        U_IDX = 3

        page = page_table[self.__pageNumber]
        print()
        print()
        self.printTable()
        print()
        print()

        # DISK -- Not in Physical Mem, Permission bit not 0.
        if page[V_IDX] == 0 and page[P_IDX] != 0:
            (clockQ, page_table) = self.evict(self.__pageNumber)
            self.setClockQ(clockQ)
            self.setPageTable(page_table)
            frame = bin(page[F_IDX])[2:]
            physicalAddress = (frame + self.__offset).zfill(M)
            print("PAGEFAULT {0}".format(hex(int(physicalAddress, 2))))

        # SEGFAULT -- Not in Physical Mem, Lack Permission.
        elif page[V_IDX] == 0 and page[P_IDX] == 0:
            print("SEGFAULT")

        # Page Hit
        elif page[V_IDX] == 1 and page[P_IDX] != 0:
            page_table[self.__pageNumber][U_IDX] = 1
            self.setClockQ(clockQ)
            self.setPageTable(page_table)
            frame = bin(page[F_IDX])[2:]
            physicalAddress = (frame + self.__offset).zfill(M)
            print(hex(int(physicalAddress, 2)))

    def evict(self, reqPage: str):
        page_table = self.getPageTable()
        clockQ = self.getClockQ()
        # Used to index into a page (V P F U).
        V_IDX = 0
        P_IDX = 1
        F_IDX = 2
        U_IDX = 3

        page2evict = clockQ.pop(0)

        while page2evict[U_IDX] == 1:
            page2evict[U_IDX] = 0
            clockQ.append(page2evict)
            page2evict = clockQ.pop(0)

        if page2evict[U_IDX] == 0:
            # Replace the current_page with the requested page.
            page_table[reqPage][V_IDX] = 1 # Step One: Swap valid bit of both pages.
            page_table[reqPage][F_IDX] = page2evict[F_IDX] # Step Two: Get Frame.
            page_table[reqPage][U_IDX] = 1 # Step Three: Set Recently Used.
            clockQ.append(page_table[reqPage])

            page2evict[V_IDX] = 0

        self.setClockQ(clockQ)
        self.setPageTable(page_table)
        return (clockQ, page_table)


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
            VA.getPhysicalAddress()

    except EOFError as e:
        1 + 1
        # print(e)


if __name__ == "__main__":
    main()