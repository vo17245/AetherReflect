import ut
import ut.cpp_code
import ut.cpp_code.file_test
import ut.cpp_code.group_test
import ut.do_file_test

def run_ut():
    ut.cpp_code.file_test.run()
    ut.do_file_test.run()
    ut.cpp_code.group_test.run()