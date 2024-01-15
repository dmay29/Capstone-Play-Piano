cmake_minimum_required(VERSION 3.10)

project(PLAYPKeyControl)

find_package(PkgConfig)
pkg_check_modules(PLAYP_BASE playp_base REQUIRED)

set_property(DIRECTORY . APPEND PROPERTY COMPILE_OPTIONS
    -Wall
    -Werror
)

set_property(DIRECTORY . APPEND PROPERTY LINK_OPTIONS
    -Wl
    --fatal-warnings
)

add_subdirectory(playp_key_control)
