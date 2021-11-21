#include "lib/Client.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[])
{
    std::vector<std::string> messages{"abc1", "0001", "hello", "world", "QUIT", "Hmmm?"};
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }   
    std::cout << ip << " " << port << std::endl;
    Client* cl;
    try{
        cl = new Client(ip, port);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }
    for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
        try{
            cl->Send(*it);
            } catch (const std::exception& e){
            std::cout << e.what() << std::endl;
            }
    }

}

