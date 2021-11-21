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

class Client{
    Socket sock;
public:
    Client(std::string ip, int port);
    void Send(std::string msg);
    std::string Receive();
};