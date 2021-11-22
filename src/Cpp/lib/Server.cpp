#include "Server.h"

Server::Server(std::string ip, int port): sock(ip,port,true){
    sock.Bind();
}

void Server::SendString(std::string msg){
    sock.Send(msg.c_str(),msg.length());
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

