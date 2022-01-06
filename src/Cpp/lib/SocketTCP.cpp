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

void SocketTCP::Send(std::string msg){
    sock.Write(std::vector<char>(msg.begin(), msg.end()));
}

std::vector<char> SocketTCP::Receive(){
    return sock.Read();
}
