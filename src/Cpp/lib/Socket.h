#pragma once

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include <memory>
#include <vector>

constexpr int max_buffer_size = 32768;

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

public:
    Socket(std::string ip = "127.0.0.1" , int port = 8000, bool is_serv = false, bool is_UDP = true);
    ~Socket();
    void Bind();
    void Send(std::vector<char> msg);
    std::vector<char> Receive();
};

struct SimpStruct{
    int a;
    int b;
    long c;
};