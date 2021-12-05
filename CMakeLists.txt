cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 17)
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=0)
set(CMAKE_CXX_STANDARD_REQUIRED True)


set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

project(ProjectPSI)

include_directories(src)
add_subdirectory(src)




