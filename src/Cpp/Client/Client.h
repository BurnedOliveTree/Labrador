#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include <memory>

class Client{
    struct sockaddr_in server_4;
    struct sockaddr_in6 server_6;
    struct sockaddr* server ;

    socklen_t server_len;
    char* server_ip;
    int server_port, client_socket;
    char buffer[4096];
public:
    Client(char* ip = "127.0.0.1" , int port = 2137);
    ~Client();
    void Send(std::string msg);
    std::string Receive();
};