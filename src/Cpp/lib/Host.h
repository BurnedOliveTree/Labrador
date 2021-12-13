#pragma once

#include "DataSerializer.h"

class Host{
    DataSerializer ws;
public:
    Host(SocketInterface* _si);
    void Send(std::variant<std::string, SimpleStruct> msg);
    std::variant<std::string, SimpleStruct> Receive();
    std::vector<std::variant<std::string, SimpleStruct>> ReceiveAll();
};