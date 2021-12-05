#include "SocketUDP.h"

SocketUDP::SocketUDP(std::string ip, int port,  bool is_serv): sock(ip,port,is_serv,true){
    if(is_serv){
        sock.Bind();
    }
}

void SocketUDP::Send(std::vector<char> msg){
    PacketHeader ph = {htons(msg.size()), 0, 0};
    sock.Send(Utils::addHeader(Utils::serializeStruct<PacketHeader>(ph), msg));
}

std::vector<char> SocketUDP::Receive(){
    std::vector<char> rec = sock.Receive();
    auto [hd, msg] = Utils::divideHeader(4, rec);
    return msg;
}


