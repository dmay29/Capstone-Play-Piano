cmake_minimum_required(VERSION 3.10)

project(PLAYPBase)

set_property(DIRECTORY . APPEND PROPERTY COMPILE_OPTIONS
    -Wall
    -Werror
)

set_property(DIRECTORY . APPEND PROPERTY LINK_OPTIONS
    -Wl
    --fatal-warnings
)

add_subdirectory(playp_base)
