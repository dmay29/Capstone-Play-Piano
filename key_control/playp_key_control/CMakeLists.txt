project(playp_key_control LANGUAGES CXX)

set(SRC_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/key_control_builder.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/mock_key_control_impl.cpp
)

add_library(${PROJECT_NAME} SHARED ${SRC_FILES})

target_include_directories(${PROJECT_NAME}
    PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:include>"
    PRIVATE
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>"
        "$<INSTALL_INTERFACE:src/include>"
    INTERFACE_INCLUDE_DIRECTORIES
        "$<BUILD_INTERFACE:${PLAYP_BASE_INCLUDE_DIRS}>"
)

target_link_libraries(${PROJECT_NAME}
    "${PLAYP_BASE_LIBRARIES}"
)

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc
"
prefix=${CMAKE_INSTALL_PREFIX}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: ${PROJECT_NAME}
Description: Play Piano key control library
Version: 1.0.0
Libs: -L\${libdir} -l${PROJECT_NAME}
Cflags: -I\${includedir}
"
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}.pc
    DESTINATION lib/pkgconfig
)

install(TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION lib
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h*"
)

add_executable(test_mock_key_ctrl ${CMAKE_CURRENT_SOURCE_DIR}/test/example_with_mock_key_ctrl.cpp)

target_include_directories(test_mock_key_ctrl
    PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<INSTALL_INTERFACE:include>"
)

target_link_libraries(test_mock_key_ctrl playp_key_control)