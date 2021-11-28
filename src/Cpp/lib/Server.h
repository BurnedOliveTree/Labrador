#pragma once

#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <string>
#include <iostream>
#include <memory>
#include "Socket.h"
#include "SocketInterface.h"

class Server{
    SocketInterface* si;
public:
    Server(SocketInterface* _si);
    void Send(std::string msg);
    std::vector<char> Receive();
};