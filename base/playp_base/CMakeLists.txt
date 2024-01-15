project(playp_base LANGUAGES CXX)

add_library(${PROJECT_NAME} INTERFACE)

target_include_directories(${PROJECT_NAME}
    INTERFACE
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:include>"
)

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc
"
prefix=${CMAKE_INSTALL_PREFIX}
includedir=\${prefix}/include

Name: ${PROJECT_NAME}
Description: Play Piano base header only lib
Version: 1.0.0
Cflags: -I\${includedir}
"
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h*"
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc
    DESTINATION lib/pkgconfig
)

target_compile_features(${PROJECT_NAME} INTERFACE cxx_std_11)

set(${PROJECT_NAME}_INCLUDE_DIRS ${PROJECT_SOURCE_DIR}/include
    CACHE INTERNAL "${PROJECT_NAME}: Include Directories" FORCE
)
