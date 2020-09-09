# triage_tools_analysis

This repo lists the most frequently used triage tools on Linux.

1. [AFL/AFL++](#afl-id)
2. [exploitable](#exploitable-id)
3. [crashwalk](#crashwalk-id)
4. [afl-utils](#afl-utils-id)
5. [clusterfuzz](#clusterfuzz-id)

## 1. <a name="afl-id"></a>[AFL](https://github.com/google/AFL/tree/master)/[AFL++](https://github.com/AFLplusplus/AFLplusplus)

> no further triage

Path to the triage scripts for AFL and AFL++ are [experimental/crash_triage/triage_crashes.sh](https://github.com/google/AFL/blob/master/experimental/crash_triage/triage_crashes.sh) and [examples/crash_triage/triage_crashes.sh](https://github.com/AFLplusplus/AFLplusplus/blob/stable/examples/crash_triage/triage_crashes.sh), respectively.

AFL/AFL++ consider a crash unique based on **the trace bitmap**. `triage_crashes.sh` doesn't further group the unique crashes identified by AFL/AFL++, it only reproduces the crash, and then prints relavent information, including instruction that causes the crash and instructions near it, backtrace, and register information.

## 2. <a name="exploitable-id"></a>[explitable](https://github.com/jfoote/exploitable)

> triage crashes empirically by exploitablity level based on the behavior of crash

The 'exploitable' GDB plugin is only capable of analzing single crash at a time.

[exploitable.py](https://github.com/jfoote/exploitable/blob/master/exploitable/exploitable.py) is the entry point
--> [classifier.py](https://github.com/jfoote/exploitable/blob/master/exploitable/lib/classifier.py) implement the entry to the iteration of all rules, general form of rules and their ranks are implemented in ([rules.py](https://github.com/jfoote/exploitable/blob/master/exploitable/lib/rules.py))
--> for every rule, determine match or not ([analyzer](https://github.com/jfoote/exploitable/tree/master/exploitable/lib/analyzers)/\<specific platform\>.py, e.g [x86.py](https://github.com/jfoote/exploitable/blob/master/exploitable/lib/analyzers/x86.py)) --> the match with highest rank is chosen.

Crashes are triaged based on:

1. SIGNAL (e.g. access violation signal, abort signal...)
2. Location of crash (heap, stack)
3. Instruction (jump, banch...)
4. Operand (destination operand, source operand)
5. Near null or not
6. ...

## 3. <a name="crashwalk-id"></a>[crashwalk](https://github.com/bnagy/crashwalk)

> wrapper around `exploitable` to support triage for multiple crashes at at a time

It takes a directory of input files that would cause crash, apply `exploitable` to each input file, group crashes with the same backtrace hash, save output to `crashwalk.db`

AFL friendly.

## 4. <a name="afl-utils-id"></a>[afl-utils](https://github.com/rc0r/afl-utils)

> make use of `exploitable`, same as `crashwalk`

[`afl-vcrash`](https://github.com/rc0r/afl-utils/blob/master/README.md#afl-vcrash) may be useful, it verifies that afl-fuzz crash samples really lead to crashes in the target binary and optionally removes these samples automatically.

## 5. <a name="clusterfuzz-id"></a>[clusterfuzz](https://github.com/google/clusterfuzz)

> a more comprehensive and flexible triage tool

It covers a wide range of possible crashe senario including crashes happen in different languages, platforms, using different sanitizer and others.

Path to the analysis logic is [src/python/crash_analysis/](https://github.com/google/clusterfuzz/tree/master/src/python/crash_analysis). Main logic is in [stack_parsing/stack_analyzer.py](https://github.com/google/clusterfuzz/blob/master/src/python/crash_analysis/stack_parsing/stack_analyzer.py). Crash analysis and triage module can be used stand-alone, which takes error message as input, and output the analysis of crashes.

The main idea is to compare the error message line by line with empirically delineated regular expression, if match then record the corresponding crash type. The identified crashes are further grouped together based on three criteria which are implemented in [crash_comparer.py](https://github.com/google/clusterfuzz/blob/master/src/python/crash_analysis/crash_comparer.py) to see if unique.

The example usage of crash analysis can be found in `clusterfuzz_triage_wrapper.py`
