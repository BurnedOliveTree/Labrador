add_library(
    ServerCpp
    Cpp/Server/Server.h
    Cpp/Server/Server.cpp
)

add_library(
    ClientCpp
    Cpp/Client/Client.h
    Cpp/Client/Client.cpp
)

add_executable(ClientC Cpp/Client/main.cpp)
target_link_libraries(ClientC PUBLIC ClientCpp )
add_executable(ServerC Cpp/Server/main.cpp)
target_link_libraries(ServerC PUBLIC ServerCpp )
