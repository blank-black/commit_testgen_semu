import sys, os

sys.path.insert(0, "__ORIGINAL_CONF_DIR__")
from __ORIGINAL_CONF_MODULE__ import *
sys.path.pop(0)

# override
OUTPUT_ROOT_DIR="__MUTERIA_OUTPUT__"

# remove all criteria
ENABLED_CRITERIA = []

# remove all test tools and create a shadow tool to collect tests
from muteria.drivers.testgeneration.tools_by_languages.c.shadow_se.\
                                        driver_config import DriverConfigShadow
shadow_for_seeds = TestcaseToolsConfig(tooltype=TestToolType.USE_CODE_AND_TESTS, toolname='shadow_se', \
                        tool_user_custom=ToolUserCustom(\
                            PATH_TO_TOOL_BINARY_DIR='/home/shadowvm/shadow/klee-change/Release+Asserts/bin/',
                            DRIVER_CONFIG=DriverConfigShadow(keep_first_test=True),
                            PRE_TARGET_CMD_ORDERED_FLAGS_LIST=[
                                ('-shadow-replay-standalone',),
                                ('-only-output-states-covering-new',),
                                ('-dont-simplify',),

                                ('--search', 'bfs'),
                            ]
                        ))
                        
TESTCASE_TOOLS_CONFIGS = [
        dev_test,
        shadow_for_seeds,
]

old_build_func = CODE_BUILDER_FUNCTION
def override_build(*args, **kwargs):
    # Make sure that shadow don't generate tests, but just replay
    # Remove the klee changes
    if flags_list is None:
        flags_list = [ "-DRESOLVE_KLEE_CHANGE=11" ]
		else:	
        flags_list.append("-DRESOLVE_KLEE_CHANGE=11")
    return old_build_func(*args, **kwargs)
  
CODE_BUILDER_FUNCTION=override_build
