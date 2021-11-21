#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include <memory>

class Socket{
    struct sockaddr_in server_4;
    struct sockaddr_in6 server_6;
    struct sockaddr* server ;

    socklen_t server_len;
    char* server_ip;
    int server_port, client_socket;
    char buffer[4096];
public:
    Socket(char* ip = "127.0.0.1" , int port = 8000);
    ~Socket();
    void Bind();
    void Send(std::string);
    std::string Receive();
};