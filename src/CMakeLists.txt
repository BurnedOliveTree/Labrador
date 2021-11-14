add_library(
    ServerCpp
    Server/Server.h
    Server/Server.cpp
)

add_library(
    ClientCpp
    Client/Client.h
    Client/Client.cpp
)

add_executable(ClientC Client/main.cpp)
target_link_libraries(ClientC PUBLIC ClientCpp )
add_executable(ServerC Server/main.cpp)
target_link_libraries(ServerC PUBLIC ServerCpp )
