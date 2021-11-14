#include "Server.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[])
{
    char* ip = "127.0.0.1";
    if(argc > 1){
        ip = argv[1];
    }
    std::vector<std::string> messages;

    Server serv(ip, 8000);
    while (true){
        std::string msg = serv.Receive();
        serv.Send(std::string("Received: " + msg));
        messages.push_back(msg);
        if(serv.CheckQuit(msg)){
            break;
        }
    }

    for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
        std::cout << *it << std::endl;
    }
}
