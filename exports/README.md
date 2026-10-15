# exports -- copy-and-paste checks of Michael Warren Song's work
`everything_check.py` is one plain Python 3 file (standard library only) that recomputes 49 results from the repository -- 1/137 and the 137-map, twin primes, seed 246, Phi_12 at 137, Langton's ant, 0.25, the drip cycle, counting the commas, the doubling and 181, the earlier pages -- each opened with the lines it checks, word for word: the owner's messages with their number, earlier work from the owner's files, pasted text marked as pasted.
On a phone: open the file on GitHub, tap Raw, select all and copy; open any online Python site (search "online python"), paste over the sample code, press Run.
It finishes in about a second and prints PASS or FAIL for every result, then "49 of 49 checks passed"; a FAIL line says what came out different.
On a computer with the repository: `python3 exports/everything_check.py` (`check_265_270.py` is the earlier, shorter check of #265-#270).
