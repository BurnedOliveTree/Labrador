#include "Server.h"

Server::Server(char* ip, int port): sock(ip,port,true){
    sock.Bind();
}

void Server::Send(std::string msg){
    sock.Send(msg);
}

std::string Server::Receive(){
    return sock.Receive();
}

bool Server::CheckQuit(std::string msg){
    if (msg == "QUIT"){
        return true;
    }
    return false;
}

