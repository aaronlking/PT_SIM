echo "Welcome to The Big Differ, the ultra-enhanced-5000 page table simulator checkinator."
echo "https://open.spotify.com/track/4nlvKIIetOWGIMyhjQXgOZ?si=e99c6245d71c47ab"

# Hard - Coded Quick Testing.

# Test Actual vs Expected Part A output (with input1 & PT_A).
sh ptsim tests/PT_A.txt < tests/test_input1.txt > tests/actual_output/ptsim_PT_A_output1.out
diff tests/expected_output/ptsim_PT_A_output1.txt tests/actual_output/ptsim_PT_A_output1.out

# Test Actual vs Expected Part A output (with input2 & PT_B).
sh ptsim tests/PT_B.txt < tests/test_input2.txt > tests/actual_output/ptsim_PT_B_output2.out
diff tests/expected_output/ptsim_PT_B_output2.txt tests/actual_output/ptsim_PT_B_output2.out

# Test Actual vs Expected Part A output (with input2 & PT_C).
sh ptsim tests/PT_C.txt < tests/test_input2.txt > tests/actual_output/ptsim_PT_C_output2.out
diff tests/expected_output/ptsim_PT_C_output2.txt tests/actual_output/ptsim_PT_C_output2.out

# Test Actual vs Expected Part B output (with input1 & PT_A).
sh ptsim-clock tests/PT_A.txt < tests/test_input1.txt > tests/actual_output/ptsim_clock_PT_A_output1.out
diff tests/expected_output/ptsim_clock_PT_A_output1.txt tests/actual_output/ptsim_clock_PT_A_output1.out

# Test Actual vs Expected Part B output (with input2 & PT_C).
sh ptsim-clock tests/PT_C.txt < tests/test_input2.txt > tests/actual_output/ptsim_clock_PT_C_output2.out
diff tests/expected_output/ptsim_clock_PT_C_output2.txt tests/actual_output/ptsim_clock_PT_C_output2.out