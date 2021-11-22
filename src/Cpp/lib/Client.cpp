#include "Client.h"

Client::Client(std::string ip, int port):sock(ip,port, false){
}

void Client::SendString(std::string msg){
    sock.Send(static_cast<const void*>(msg.c_str()),msg.length());
}

void Client::SendStruct(struct SimpStruct msg){
    sock.Send(static_cast<const void*>(&msg),sizeof(msg));
}

std::string Client::ReceiveString(){
    return std::string(sock.Receive().get());   
}

std::shared_ptr<struct SimpStruct> Client::ReceiveStruct(){
    return (std::shared_ptr<struct SimpStruct>((struct SimpStruct*)sock.Receive().get()));
}