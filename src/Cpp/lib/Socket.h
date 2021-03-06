#pragma once

#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <iostream>
#include <vector>
#include <arpa/inet.h>


constexpr int MAX_PACKET_SIZE = 7;

class Socket{
    struct sockaddr_in desc_4;
    struct sockaddr_in6 desc_6;
    struct sockaddr* self_addr ;
    struct sockaddr dest_addr ;
    bool is_server;
    bool is_datagram;

    socklen_t socket_len;
    socklen_t dest_len;
    std::string socket_ip;
    int socket_port, sock, msgsock;

public:
    Socket(std::string ip = "127.0.0.1" , int port = 8000, bool is_serv = false, bool is_UDP = true);
    ~Socket();
    void Bind();
    void Connect();
    void Listen();
    void Write(std::vector<char> msg);
    void Send(std::vector<char> msg);
    std::vector<char> Receive();
    std::vector<char> Read(size_t n_bytes);

};

struct SockHeader{
    int16_t length;
    int8_t packet_max;
    int8_t packet_id;
};