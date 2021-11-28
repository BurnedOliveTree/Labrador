#include "Server.h"

Server::Server(SocketInterface* _si): si(_si){}

void Server::Send(std::string msg){
    si->Send(msg);
}

std::vector<char> Server::Receive(){
    return si->Receive();
}
