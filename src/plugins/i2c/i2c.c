/*
 * Copyright (c) 2003 Sun Microsystems, Inc.  All Rights Reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 
 * Redistribution of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 * 
 * Redistribution in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 * 
 * Neither the name of Sun Microsystems, Inc. or the names of
 * contributors may be used to endorse or promote products derived
 * from this software without specific prior written permission.
 * 
 * This software is provided "AS IS," without a warranty of any kind.
 * ALL EXPRESS OR IMPLIED CONDITIONS, REPRESENTATIONS AND WARRANTIES,
 * INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE OR NON-INFRINGEMENT, ARE HEREBY EXCLUDED.
 * SUN MICROSYSTEMS, INC. ("SUN") AND ITS LICENSORS SHALL NOT BE LIABLE
 * FOR ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
 * OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.  IN NO EVENT WILL
 * SUN OR ITS LICENSORS BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA,
 * OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR
 * PUNITIVE DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF
 * LIABILITY, ARISING OUT OF THE USE OF OR INABILITY TO USE THIS SOFTWARE,
 * EVEN IF SUN HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pigpio.h>
#include <sys/ioctl.h>
#define __USE_MISC
#include <sys/types.h>
#include <sys/time.h>
#include <time.h>

#include <ipmitool/ipmi.h>
#include <ipmitool/ipmi_intf.h>
#include <ipmitool/helper.h>
#include <ipmitool/ipmi_sel.h>
#include <ipmitool/log.h>

#include "i2capi.h"

#define IPMI_I2C_TIMEOUT	(1000 * 1000)
#define IPMI_I2C_MAX_RETRY	3
#define IPMI_I2C_DEV		"/dev/i2c-2"
#define IPMI_I2C_BUF_SIZE	64




//I2C information
#define ADDR 0x10
extern int verbose;


void runSlave();
void writeSlave();
void closeSlave();
int getControlBits(int, bool);
const int slaveAddress = 0x66; // <-- Your address of choice
bsc_xfer_t xfer; // Struct to control data flow
struct timespec ts;



static int ipmi_i2c_open(struct ipmi_intf * intf)
{
	gpioInitialise();
    printf("Initialized GPIOs\n");
    // Close old device (if any)
    xfer.control = getControlBits(slaveAddress, false); // To avoid conflicts when restarting
    bscXfer(&xfer);
    // Open and set Set I2C slave Address
    xfer.control = getControlBits(slaveAddress, true);
    int status = bscXfer(&xfer); // Should now be visible in I2C-Scanners
    if (status >= 0)
    {
        printf("Opened slave\n");
        xfer.rxCnt = 0;
    }else
        printf("Failed to open slave!!!\n");
}

static void ipmi_i2c_close(struct ipmi_intf * intf)
{
	printf("Closing Time!  Every new beginning comes from some other beginnings ends YEAH\n");


    printf("Initialized GPIOs\n");
    xfer.control = getControlBits(slaveAddress, false);
    bscXfer(&xfer);
    printf("Closed slave.\n");
    gpioTerminate();
    printf("Terminated GPIOs.\n");

	intf->opened = 0;
	intf->manufacturer_id = IPMI_OEM_UNKNOWN;
}

static struct ipmi_rs * ipmi_i2c_send_cmd(struct ipmi_intf *__UNUSED__(intf), struct ipmi_rq *req)
{

	I2CPACKET i2cPacket;
	int status, i;
	unsigned char ccode;
	unsigned char i2c_buf[50] = "";  //I2C information is data + 7 bytes

	//Response data structures
	static struct ipmi_rs rsp; //This needs to be the final IPMI packet passed back
	BYTE responseData[MAX_IMB_RESP_SIZE]; // raw array
	ImbResponseBuffer *resp = (ImbResponseBuffer *)responseData; //IMB data structure

	i2cPacket.imb.rsSa	= 0x66;
	i2cPacket.imb.rsLun	= 0;
	i2cPacket.imb.busType	= 0;
	i2cPacket.imb.netFn	= req->msg.netfn;
	i2cPacket.imb.cmdType	= req->msg.cmd;

	i2cPacket.imb.data = req->msg.data;
	i2cPacket.imb.dataLength = req->msg.data_len;

	if (verbose > 1) {
		printf("I2C rsSa       : %x\n", i2cPacket.imb.rsSa);
		printf("I2C netFn      : %x\n", i2cPacket.imb.netFn);
		printf("I2C cmdType    : %x\n", i2cPacket.imb.cmdType);
		//printf("I2C data    : %x\n", *i2cPacket.imb.data); //can't print data... not all commands have data
		printf("I2C dataLength : %d\n", i2cPacket.imb.dataLength);
		for (i = 0; i < i2cPacket.imb.dataLength ; i++) {
			printf("0x%02x ", i2cPacket.imb.data[i]);
		}
	}

	i2c_buf[0] = ADDR << 1;
	i2c_buf[1] = i2cPacket.imb.netFn << 2; //netfn shifted to make way for the LUN.
	unsigned char checksum = CalculateChecksum(i2c_buf, sizeof(i2c_buf[0]) * 2);
	i2c_buf[2] = checksum;
	i2c_buf[3] = i2cPacket.imb.rsSa << 1; //LUN is 0, no need to add it
	i2c_buf[4] = 0x00; // TODO: Not sure how to do the sequence
	i2c_buf[5] = i2cPacket.imb.cmdType;

	for(int i=0; i < i2cPacket.imb.dataLength; i++) {
		i2c_buf[6+i] = i2cPacket.imb.data[i];
	}

	i2c_buf[6 + i2cPacket.imb.dataLength] = CalculateChecksum(i2c_buf, sizeof(i2c_buf[0]) * 17);

	size_t newSize = i2cPacket.imb.dataLength + 6;
	char* final_i2c_buf = malloc( newSize * sizeof(char) );
	memcpy(final_i2c_buf, i2c_buf + 1, newSize * sizeof(char) );

	printf("i2c packet: ");
	for(int i=0; i < newSize; i++) {
		printf("%02x ", final_i2c_buf[i]);
	}



	printf("going to write\n");
	int handle = i2cOpen(1, 0x10, 0);
	i2cWriteDevice(handle, final_i2c_buf , newSize);

	ts.tv_sec = 0;
	ts.tv_nsec = 5000000;
	nanosleep(&ts, NULL);

	bscXfer(&xfer);
	printf("We're going in!\n 1..2..3 and go... like a kamikazee.  rxCnt: %d\n", xfer.rxCnt);
    if(xfer.rxCnt > 0) {
	    for(int i = 0; i < xfer.rxCnt; i++)
	        printf(" %02x ", xfer.rxBuf[i]);
	    	responseData[i] = xfer.rxBuf[i];
    	printf("\n");
    }

	// need this to continue
	size_t respDataLen = sizeof(responseData) - 1;
	//if ((respDataLen) && (responseData)) {
	resp->cCode = responseData[3];
	memcpy(responseData - 2, resp->data, respDataLen - 2);
	//}

	printf("Returning the ccode: %02x\n", resp->cCode);

	

	return &rsp;
}

struct ipmi_intf ipmi_i2c_intf = {
	.name = "i2c",
	.desc = "I2C Interface",
	.open = ipmi_i2c_open,
	.close = ipmi_i2c_close,
	.sendrecv = ipmi_i2c_send_cmd,
	.target_addr = IPMI_BMC_SLAVE_ADDR,
};


int getControlBits(int address /* max 127 */, bool open) {
    /*
    Excerpt from http://abyz.me.uk/rpi/pigpio/cif.html#bscXfer regarding the control bits:
    22 21 20 19 18 17 16 15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
    a  a  a  a  a  a  a  -  -  IT HC TF IR RE TE BK EC ES PL PH I2 SP EN
    Bits 0-13 are copied unchanged to the BSC CR register. See pages 163-165 of the Broadcom
    peripherals document for full details.
    aaaaaaa defines the I2C slave address (only relevant in I2C mode)
    IT  invert transmit status flags
    HC  enable host control
    TF  enable test FIFO
    IR  invert receive status flags
    RE  enable receive
    TE  enable transmit
    BK  abort operation and clear FIFOs
    EC  send control register as first I2C byte
    ES  send status register as first I2C byte
    PL  set SPI polarity high
    PH  set SPI phase high
    I2  enable I2C mode
    SP  enable SPI mode
    EN  enable BSC peripheral
    */
    // Flags like this: 0b/*IT:*/0/*HC:*/0/*TF:*/0/*IR:*/0/*RE:*/0/*TE:*/0/*BK:*/0/*EC:*/0/*ES:*/0/*PL:*/0/*PH:*/0/*I2:*/0/*SP:*/0/*EN:*/0;
    int flags;
    if(open)
        flags = /*RE:*/ (1 << 9) | /*TE:*/ (1 << 8) | /*I2:*/ (1 << 2) | /*EN:*/ (1 << 0);
    else // Close/Abort
        flags = /*BK:*/ (1 << 7) | /*I2:*/ (0 << 2) | /*EN:*/ (0 << 0);
    return (address << 16 /*= to the start of significant bits*/) | flags;
}

