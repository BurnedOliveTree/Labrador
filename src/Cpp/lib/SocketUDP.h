#pragma once

#include "SocketInterface.h"

class SocketUDP: public SocketInterface{
    Socket sock;
public:
    SocketUDP(std::string ip = "127.0.0.1" , int port = 8000,  bool is_serv = false);
    void Send(std::vector<char> msg) override;
    std::vector<char> Receive() override;
    std::vector<std::vector<char>> ReceiveAll() override;
};