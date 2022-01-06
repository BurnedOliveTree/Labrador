#pragma once

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include "Socket.h"
#include "SocketInterface.h"

class SocketTCP: public SocketInterface{
    Socket sock;
public:
    SocketTCP(std::string ip = "127.0.0.1" , int port = 8000,  bool is_serv = false);
    void Send(std::string msg) override;
    std::vector<char> Receive() override;
};