class Client{
    Client();
    ~Client();
    int Send(char* buffer);
    int Receive(char* buffer);
};
