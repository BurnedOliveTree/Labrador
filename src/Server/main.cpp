#include "Server.h"
#include <iostream>
#include <vector>

#define SERWER_PORT 8888
#define SERWER_IP "127.0.0.1"

int main(int argc, char* argv[])
{
    char* ip = "127.0.0.1";
    if(argc > 1){
        ip = argv[1];
    }
    std::vector<std::string> messages;

    Server serv(ip);
    while (true){
        std::string msg = serv.Receive();
        messages.push_back(msg);
        if(serv.CheckQuit(msg)){
            break;
        }
    }

    for(std::vector<std::string>::iterator it = messages.begin(); it != messages.end(); ++it) {
        std::cout << *it << std::endl;
    }
}
