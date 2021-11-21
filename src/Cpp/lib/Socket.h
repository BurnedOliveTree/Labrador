#pragma once

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include <memory>

class Socket{
    struct sockaddr_in desc_4;
    struct sockaddr_in6 desc_6;
    struct sockaddr* self_addr ;
    struct sockaddr dest_addr ;
    bool is_server;

    socklen_t socket_len;
    socklen_t dest_len;
    std::string socket_ip;
    int socket_port, sock;
    char buffer[4096];
public:
    Socket(std::string ip = "127.0.0.1" , int port = 8000, bool is_serv = false);
    ~Socket();
    void Bind();
    void Send(std::string);
    std::string Receive();
};