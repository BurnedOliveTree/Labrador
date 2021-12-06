#include "DataSerializer.h"

DataSerializer::DataSerializer(SocketInterface* _si): si(_si){}

void DataSerializer::Send(std::string msg){
    TypeHeader th = {0};
    std::vector<char> data = Utils::serializeString(msg);
    si->Send(Utils::addHeader<TypeHeader>(th, data));
}

void DataSerializer::Send(SimpleStruct msg){
    TypeHeader th = {1};
    msg.a = htons(msg.a);
    std::vector<char> data = Utils::serializeStruct<SimpleStruct>(msg);
    si->Send(Utils::addHeader<TypeHeader>(th, data));
}

std::variant<std::string, SimpleStruct> DataSerializer::Receive(){
    auto [header, msg] = Utils::divideHeader(1,si->Receive());
    TypeHeader th = Utils::deserializeStruct<TypeHeader>(header);
    switch (th.type)
    {
    case 0:
        return HandleString(msg);
    case 1:
        return HandleStruct(msg);
    default:
        return "Error: type of message unknown";
    }
}

SimpleStruct DataSerializer::HandleStruct(std::vector<char> data){
    SimpleStruct msg =  Utils::deserializeStruct<SimpleStruct>(data);
    msg.a = ntohs(msg.a);
    return msg;
}

std::string DataSerializer::HandleString(std::vector<char> data){
    return Utils::deserializeString(data);        
}
