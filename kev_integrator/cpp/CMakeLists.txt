cmake_minimum_required(VERSION 3.20)
project(kev_integrator VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(CURL REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(SQLite3 REQUIRED)

add_library(kev_integrator STATIC
    src/kev_entry.cpp
    src/fetcher.cpp
    src/cache.cpp
    src/state.cpp
    src/circuit_breaker.cpp
)

target_link_libraries(kev_integrator
    CURL::libcurl
    nlohmann_json::nlohmann_json
    SQLite::SQLite3
)

add_executable(kev_sync src/cli.cpp)
target_link_libraries(kev_sync kev_integrator)
