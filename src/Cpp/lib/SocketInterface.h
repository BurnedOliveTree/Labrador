#pragma once

class SocketInterface{
public:
    // SocketInterface(std::string ip, int port,  bool is_serv) = 0;
    virtual void Send(std::string msg) = 0;
    virtual std::vector<char> Receive() = 0;
};