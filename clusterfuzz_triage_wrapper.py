# 2 steps before running the script (to bypass configuration folder setup):
#    1. replace clusterfuzz/src/python/crash_analysis/stack_parsing/stack_analyzer.py line650-652
#       by "custom_stack_frame_ignore_regexes = []"
#    2. replace clusterfuzz/src/python/crash_analysis/crash_analyzer.py line136-137
#       by "stack_blacklist_regexes = []"

import sys
sys.path.append('<path_to_clusterfuzz>/src/')
sys.path.append('<path_to_clusterfuzz>/src/python')
sys.path.append('<path_to_clusterfuzz>/src/python/crash_analysis')

from base import utils
from crash_analysis.stack_parsing import stack_analyzer
from crash_analysis.crash_result import CrashResult
from crash_analysis import crash_analyzer

# log sample: https://www.bugsnag.com/blog/how-to-make-sense-of-android-crash-logs
unsymbolized_crash_stacktrace = """
2019-08-27 16:10:28.303 10773-10773/com.bugsnag.android.example E/AndroidRuntime: FATAL EXCEPTION: main
    Process: com.bugsnag.android.example, PID: 10773
    java.lang.RuntimeException: Fatal Crash
        at com.example.foo.CrashyClass.sendMessage(CrashyClass.java:10)
        at com.example.foo.CrashyClass.crash(CrashyClass.java:6)
        at com.bugsnag.android.example.ExampleActivity.crashUnhandled(ExampleActivity.kt:55)
        at com.bugsnag.android.example.ExampleActivity$onCreate$1.invoke(ExampleActivity.kt:33)
        at com.bugsnag.android.example.ExampleActivity$onCreate$1.invoke(ExampleActivity.kt:14)
        at com.bugsnag.android.example.ExampleActivity$sam$android_view_View_OnClickListener$0.onClick(ExampleActivity.kt)
        at android.view.View.performClick(View.java:5637)
        at android.view.View$PerformClick.run(View.java:22429)
        at android.os.Handler.handleCallback(Handler.java:751)
        at android.os.Handler.dispatchMessage(Handler.java:95)
        at android.os.Looper.loop(Looper.java:154)
        at android.app.ActivityThread.main(ActivityThread.java:6119)
        at java.lang.reflect.Method.invoke(Native Method)
        at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:886)
        at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:776)"""
application_command_line = ""
state = stack_analyzer.get_crash_data(
    unsymbolized_crash_stacktrace, symbolize_flag=False, already_symbolized=True)
security_flag = crash_analyzer.is_security_issue(
    unsymbolized_crash_stacktrace, state.crash_type, state.crash_address)
key = '%s,%s,%s' % (state.crash_type, state.crash_state, security_flag)
should_be_ignored = crash_analyzer.ignore_stacktrace(state.crash_stacktrace)
print("key:", key)

# sample output:
#   key: Fatal Exception,com.example.foo.CrashyClass.sendMessage
#   com.example.foo.CrashyClass.crash
#   com.bugsnag.android.example.ExampleActivity.crashUnhandled
#   ,False
