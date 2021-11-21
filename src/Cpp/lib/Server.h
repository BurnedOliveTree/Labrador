#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include "Socket.h"

class Server{
    Socket socket;
public:
    Server(char* ip = "127.0.0.1" , int port = 8000);
    void Send(std::string msg);
    std::string Receive();
    bool CheckQuit(std::string msg);
};