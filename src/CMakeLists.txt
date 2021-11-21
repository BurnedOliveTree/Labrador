
add_library(
    SocketCpp
    Cpp/lib/Socket.h
    Cpp/lib/Socket.cpp
)

add_library(
    ServerCpp
    Cpp/lib/Server.h
    Cpp/lib/Server.cpp
)

add_library(
    ClientCpp
    Cpp/lib/Client.h
    Cpp/lib/Client.cpp
)



add_executable(ClientC Cpp/client.cpp)
target_link_libraries(ClientC PUBLIC ClientCpp )
target_link_libraries(ClientC PUBLIC SocketCpp )
add_executable(ServerC Cpp/server.cpp)
target_link_libraries(ServerC PUBLIC ServerCpp )
target_link_libraries(ServerC PUBLIC SocketCpp )

