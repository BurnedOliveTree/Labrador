#include "Client.h"

Client::Client(SocketInterface* _si): si(_si){}

void Client::Send(std::string msg){
    si->Send(msg);
}

std::vector<char> Client::Receive(){
    return si->Receive();
}
