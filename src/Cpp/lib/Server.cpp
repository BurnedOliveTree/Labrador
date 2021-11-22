#include "Server.h"

Server::Server(std::string ip, int port): sock(ip,port,true){
    sock.Bind();
}

void Server::SendString(std::string msg){
    sock.Send(static_cast<const void*>(msg.c_str()),msg.length());
}

std::string Server::ReceiveString(){
    return std::string(sock.Receive().get());
}

std::shared_ptr<struct SimpStruct> Server::ReceiveStruct(){
    return (std::shared_ptr<struct SimpStruct>((struct SimpStruct*)sock.Receive().get()));
}

bool Server::CheckQuit(std::string msg){
    if (msg == "QUIT"){
        return true;
    }
    return false;
}

