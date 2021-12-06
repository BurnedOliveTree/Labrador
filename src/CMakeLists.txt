SET(G++_COVERAGE_COMPILE_FLAG = "-pthread")
# /SET(G++_COVERAGE_COMPILE_FLAG = "-lstdc++")

# add_library(
#     HostCpp
#     Cpp/lib/Host.h
#     Cpp/lib/Host.cpp
# )

# add_library(
#     DataSerializer
#     Cpp/lib/DataSerializer.h
#     Cpp/lib/DataSerializer.cpp
# )

# add_library(
#     SocketCpp
#     Cpp/lib/Socket.h
#     Cpp/lib/Socket.cpp
# )

# add_library(
#     SocketInterface
#     Cpp/lib/SocketUDP.h
#     Cpp/lib/SocketInterface.h
#     Cpp/lib/SocketUDP.cpp
#     Cpp/lib/SocketTCP.h
#     Cpp/lib/SocketTCP.cpp
# )

# add_library(
#     ExitCpp
#     Cpp/lib/Exit.h
#     Cpp/lib/Exit.cpp
# )

# add_library(
#     UtilsCpp
#     Cpp/lib/Utils.h
#     Cpp/lib/Utils.cpp
# )

add_library(
    Everything
    Cpp/lib/Host.h
    Cpp/lib/Host.cpp
    Cpp/lib/DataSerializer.h
    Cpp/lib/DataSerializer.cpp
    Cpp/lib/Socket.h
    Cpp/lib/Socket.cpp
    Cpp/lib/SocketUDP.h
    Cpp/lib/SocketInterface.h
    Cpp/lib/SocketUDP.cpp
    Cpp/lib/SocketTCP.h
    Cpp/lib/SocketTCP.cpp
    Cpp/lib/Exit.h
    Cpp/lib/Exit.cpp
    Cpp/lib/Utils.h
    Cpp/lib/Utils.cpp
)


add_executable(ClientC Cpp/client.cpp)
target_link_libraries(ClientC PUBLIC Everything)


add_executable(ServerC Cpp/server.cpp)
target_link_libraries(ServerC PUBLIC -pthread )
target_link_libraries(ServerC PUBLIC Everything)


add_executable(Test Cpp/test.cpp)
target_link_libraries(Test PUBLIC Everything)

