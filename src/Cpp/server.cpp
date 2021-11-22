#include "lib/Server.h"
#include <iostream>
#include <vector>

// int main(int argc, char* argv[])
// {
//     std::string ip = "127.0.0.1";
//     int port = 2137;
//     if(argc > 2){
//         ip = argv[1];
//         port = atoi(argv[2]);
//     }
//     Server* serv;
//     try{
//         serv = new Server(ip, port);
//     } catch (const std::exception& e){
//         std::cout << e.what() << std::endl;
//     }
//     std::string msg;
//     while (true){
//         try{
//             msg = serv->ReceiveString();
//         } catch (const std::exception& e){
//         std::cout << e.what() << std::endl;
//         }
//         std::cout << "Received message: " << msg.length() << std::endl;
//         if(serv->CheckQuit(msg)){
//             break;
//         }
//     }
// }


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
    std::shared_ptr<struct SimpStruct> msg;
    while (true){
        try{
            msg = serv->ReceiveStruct();
        } catch (const std::exception& e){
        std::cout << e.what() << std::endl;
        }
        std::cout << "Received struct: " << msg->a << ", " << msg->b << ", " << msg->c << std::endl;
        if(msg){
        break;
        }
    }
}
