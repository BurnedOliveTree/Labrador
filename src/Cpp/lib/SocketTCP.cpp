#include "SocketTCP.h"

SocketTCP::SocketTCP(std::string ip, int port,  bool is_serv): sock(ip,port,is_serv,false){
    if(is_serv){
        sock.Bind();
        sock.Listen();
    }
    else{
        sock.Connect();
    }
}

void SocketTCP::Send(std::vector<char> msg){
    PacketHeader ph = {htons(msg.size()), 0, 0};
    sock.Write(Utils::addHeader(Utils::serializeStruct<PacketHeader>(ph), msg));
}

std::vector<char> SocketTCP::Receive(){
    PacketHeader ph = Utils::deserializeStruct<PacketHeader>(sock.Read(sizeof(PacketHeader)));
    return sock.Read(ntohs(ph.length));
}
