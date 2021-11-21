#include "Client.h"

Client::Client(char* ip, int port){
    socket = Socket(ip,port);
}

void Client::Send(std::string msg){
    socket.Send(msg);
}

std::string Client::Receive(){
    return socket.Receive();
}
