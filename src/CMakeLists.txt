SET(G++_COVERAGE_COMPILE_FLAG = "-pthread")

add_library(
    ServerCpp
    Cpp/lib/Server.h
    Cpp/lib/Server.cpp
)

add_library(
    SocketCpp
    Cpp/lib/Socket.h
    Cpp/lib/Socket.cpp
)

add_library(
    SocketInterface
    Cpp/lib/SocketUDP.h
    Cpp/lib/SocketInterface.h
    Cpp/lib/SocketUDP.cpp
    Cpp/lib/SocketTCP.h
    Cpp/lib/SocketTCP.cpp
)

add_library(
    ClientCpp
    Cpp/lib/Client.h
    Cpp/lib/Client.cpp
)


add_library(
    ExitCpp
    Cpp/lib/Exit.h
    Cpp/lib/Exit.cpp
)



add_executable(ClientC Cpp/client.cpp)
target_link_libraries(ClientC PUBLIC SocketInterface)
target_link_libraries(ClientC PUBLIC ClientCpp )
target_link_libraries(ClientC PUBLIC SocketCpp )
add_executable(ServerC Cpp/server.cpp)
target_link_libraries(ServerC PUBLIC -pthread )
target_link_libraries(ServerC PUBLIC SocketInterface )
target_link_libraries(ServerC PUBLIC ServerCpp )
target_link_libraries(ServerC PUBLIC SocketCpp )
target_link_libraries(ServerC PUBLIC ExitCpp )


