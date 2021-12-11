#pragma once
#include "Socket.h"
#include "Utils.h"

struct PacketHeader{
    uint16_t length;
    uint8_t max_packet;
    uint8_t curr_packet;
};

class SocketInterface{
public:
    virtual void Send(std::vector<char> msg) = 0;
    virtual std::vector<char> Receive() = 0;
    virtual std::vector<std::vector<char>> Poll() = 0;
};