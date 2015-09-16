EXECUTE_PROCESS(
    COMMAND ${PYTHON_INSTALL_DIR}/bin/python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)"
    OUTPUT_VARIABLE PYTHON_VERSION
    )
FIND_PATH(PYTHON_INCLUDE_DIR Python.h
    PATHS ${PYTHON_INSTALL_DIR}/include/python${PYTHON_VERSION}
    NO_DEFAULT_PATH
    )
FIND_LIBRARY(PYTHON_LIBRARY
    NAMES python${PYTHON_VERSION}
    PATHS ${PYTHON_INSTALL_DIR}/lib
    NO_DEFAULT_PATH
    )
MESSAGE("PYTHON_VERSION=${PYTHON_VERSION}")
MESSAGE("PYTHON_INCLUDE_DIR=${PYTHON_INCLUDE_DIR}")
MESSAGE("PYTHON_LIBRARY=${PYTHON_LIBRARY}")

INCLUDE(FindPythonInterp)
MESSAGE("PYTHON_EXECUTABLE=${PYTHON_EXECUTABLE}")
MESSAGE("PYTHON_VERSION_STRING=${PYTHON_VERSION_STRING}")

INCLUDE(FindPythonLibs)
MESSAGE("PYTHON_LIBRARIES=${PYTHON_LIBRARIES}")
MESSAGE("PYTHON_INCLUDE_PATH=${PYTHON_INCLUDE_PATH}")
MESSAGE("PYTHON_INCLUDE_DIRS=${PYTHON_INCLUDE_DIRS}")
MESSAGE("PYTHONLIBS_VERSION_STRING=${PYTHONLIBS_VERSION_STRING}")

INCLUDE_DIRECTORIES(SYSTEM ${PYTHON_INCLUDE_DIRS})
