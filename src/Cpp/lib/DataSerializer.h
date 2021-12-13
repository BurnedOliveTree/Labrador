#pragma once
#include <variant>

#include "SocketInterface.h"

struct TypeHeader{
    uint8_t type;
};   

struct SimpleStruct{
    uint16_t a;
    uint8_t b;
    uint8_t c;
};

class DataSerializer{
    SocketInterface* si;
public:
    DataSerializer(SocketInterface* _si);

    void Send(std::string msg);
    void Send(SimpleStruct msg);

    std::vector<std::variant<std::string, SimpleStruct>> ReceiveAll();
    std::variant<std::string, SimpleStruct> Receive();
    SimpleStruct HandleStruct(std::vector<char> data);
    std::string HandleString(std::vector<char> data);
};