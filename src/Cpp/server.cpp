#include "lib/Server.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[])
{
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    std::vector<std::string> messages;
    Server* serv;
    try{
        serv = new Server(ip, port);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }
    std::string msg;
    while (true){
        try{
            msg = serv->Receive();
        } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
        }
        messages.push_back(msg);
        if(serv->CheckQuit(msg)){
            break;
        }
    }

    for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
        std::cout << *it << std::endl;
    }
}
