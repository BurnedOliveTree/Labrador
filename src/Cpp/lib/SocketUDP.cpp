#include "SocketUDP.h"

SocketUDP::SocketUDP(std::string ip, int port,  bool is_serv): sock(ip,port,is_serv,true){
    if(is_serv){
        sock.Bind();
    }
}

void SocketUDP::Send(std::string msg){
    sock.Send(std::vector<char>(msg.begin(), msg.end()));
}

std::vector<char> SocketUDP::Receive(){
    return sock.Receive();
}

