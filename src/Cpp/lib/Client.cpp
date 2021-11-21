#include "Client.h"

Client::Client(std::string ip, int port):sock(ip,port, false){
}

void Client::Send(std::string msg){
    sock.Send(msg);
}

std::string Client::Receive(){
    return sock.Receive();
}
