#include "lib/Server.h"
#include <iostream>
#include <vector>
#include "lib/Exit.h"
#include <thread>
#include <pthread.h>

void listener(Server* serv){
    std::string msg;
    while (true){
        try{
            msg = serv->ReceiveString();
        } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
        }
        std::cout << "Received message: " << msg.length() << std::endl;
        if(serv->CheckQuit(msg)){
            break;
        }
    }
}

int main(int argc, char* argv[])
{
    std::string ip = "127.0.0.1";
    int port = 2137;
    if(argc > 2){
        ip = argv[1];
        port = atoi(argv[2]);
    }
    Server* serv;
    try{
        serv = new Server(ip, port);
    } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
    }

    Exit e;
    std::thread listenerth(listener, serv);
    std::thread exitth(&Exit::exit, &e);

   exitth.join();
   listenerth.detach();
}

