 /*************************************************************************
 * Author: Abhinav Jain
 * Contact: abhinavjain241@gmail.com, abhinav.jain@heig-vd.ch
 * Date: 28/06/2016
 *
 * This file contains source code to the client node of the ROS package
 * comm_tcp developed at LaRA (Laboratory of Robotics and Automation)
 * as part of my project during an internship from May 2016 - July 2016.
 *
 * (C) All rights reserved. LaRA, HEIG-VD, 2016 (http://lara.populus.ch/)
 ***************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define MESSAGE_FREQ 1

void error(const char *msg) {
    perror(msg);
    exit(0);
}


extern "C" int distribute_seeds() {
    int sockfd, portno, n, choice = 1;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char buffer[1];
    uint port_num = 8088;
    const char *host_name = "192.168.1.4"; // ---------> subject to change?
    bool echoMode = true; //want terminal to read back values

    // send characters to start and stop seed distrubution
    const char start_seed = 'y';
    const char stop_seed = 'n';
    
    portno = port_num;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0) 
        error("ERROR opening socket");

    server = gethostbyname(host_name);
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(portno);


    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");
    
    //zero out buffer
    //bzero(buffer, 1);

    //copy message to buffer to begin seed distribition
    //strcpy(buffer, start_seed);
    //write message to microntroller to begin seed distribution
    n = write(sockfd, &start_seed, 1);

    if (n < 0) 
         error("ERROR writing to socket");
    if (echoMode) {
		bzero(buffer, 1);
	    n = read(sockfd,buffer, 1);
	    if (n < 0)
			error("ERROR reading reply");
	    printf("%s\n", buffer);
    }

    //zero out buffer
    //bzero(buffer, 1);

    //copy message to buffer to stop seed distribution
    //strcpy(buffer, stop_seed)
    //write message to microcontroller to stop seed distribution
    n = write(sockfd, &stop_seed, 1);

    if (n < 0) 
         error("ERROR writing to socket");
    if (echoMode) {
        bzero(buffer, 1);
        n = read(sockfd,buffer, 1);
        if (n < 0)
            error("ERROR reading reply");
        printf("%s\n", buffer);
    }

	return 0;
}
