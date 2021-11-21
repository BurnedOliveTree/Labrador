#include "Server.h"

Server::Server(char* ip, int port){
    socket = Socket(ip,port);
    socket.Bind();
}

void Server::Send(std::string msg){
    socket.Send(msg);
}

std::string Server::Receive(){
    return socket.Receive();
}

bool Server::CheckQuit(std::string msg){
    if (msg == "QUIT"){
        return true;
    }
    return false;
}

