#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>

class Server{
    struct sockaddr_in server_4;
    struct sockaddr_in6 server_6;
    struct sockaddr* server; 
    struct sockaddr curr_client;
    socklen_t server_len;
    char* server_ip;
    int server_port, server_socket;
    char buffer[4096];
public:
    Server(char* ip = "127.0.0.1" , int port = 2137);
    ~Server();
    void Send(std::string msg);
    std::string Receive();
    bool CheckQuit(std::string msg);
};