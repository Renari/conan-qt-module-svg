project(test_package)
cmake_minimum_required(VERSION 3.1.0)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

list( INSERT CMAKE_PREFIX_PATH 0 C:/.conan/dgdwbv7w/1/)
message(" CMAKE_PREFIX_PATH is ${CMAKE_PREFIX_PATH}")

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed
set(CMAKE_AUTOMOC ON)
# Create code from a list of Qt designer ui files
set(CMAKE_AUTOUIC ON)

# Need to find all dependendancies of qtsvg
find_package(Qt5Core CONFIG REQUIRED)
find_package(Qt5Gui CONFIG REQUIRED)
find_package(Qt5Widgets CONFIG REQUIRED)

find_package(Qt5Svg CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp greeter.h)
target_link_libraries(${PROJECT_NAME} Qt5::Core Qt5::Gui Qt5::Svg)

configure_file(${CMAKE_CURRENT_BINARY_DIR}/qt.conf ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/qt.conf COPYONLY)