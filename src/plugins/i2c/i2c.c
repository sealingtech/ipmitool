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

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
//#include <linux/i2c.h>
//#include <linux/i2c-dev.h>

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
int ret = 1;
int fd;
int rfd;
int nfd;
int dfd;
int should_delete = 0;
char buf[20];
ssize_t bytes_read;
ssize_t last_bytes_read = 0;
struct timespec ts;
const char *new_device = "ipmi-slave-24c02 0x1066";
const char *delete_device = "0x1066";
//size_t new_device_len = strlen(new_device);
//size_t delete_device_len = strlen(delete_device);

extern int verbose;

/*
unsigned char
CalculateChecksum(unsigned char *hex, int n) {
    unsigned char ck = 0;
    for (int i=0; i<n; i+=1) {

        unsigned val;
        int cr = sscanf(hex + 2 * i, "%2x", &val);   // convert 2 hexa chars to a byte value
        if (cr == 1) ck += val;
    }
    printf("checksum before: %x", ck);
    return ck;
}


unsigned char
CalculateChecksum( char *buf, long bufLen )
{
	static char tmpBuf[ 4 ];
	long idx;
	unsigned int cks;

	for( idx = 0L, cks = 0; idx < bufLen; cks += (unsigned int)buf[ idx++ ] );
	printf("values added up: %d", cks);
	sprintf( tmpBuf, "%03d", (unsigned int)( cks % 256 ) );
	return( tmpBuf );
}
*/

unsigned char
CalculateChecksum(const unsigned char bytes[], size_t bytesSize, int startAt)
{
    int i;
    unsigned char checksum = 0;
    for (i = startAt; i < (bytesSize / sizeof(bytes[0])); i++) {
        checksum += bytes[i];
    }
    checksum = ~checksum + 1;
    return checksum;
}


static int ipmi_i2c_open(struct ipmi_intf * intf)
{
	printf("Info into The Open Space\n");

	return 0;
}

static void ipmi_i2c_close(struct ipmi_intf * intf)
{
	printf("Closing Time!  Every new beginning comes from some other beginnings ends YEAH\n");
	intf->opened = 0;
	intf->manufacturer_id = IPMI_OEM_UNKNOWN;
}

static struct ipmi_rs * ipmi_i2c_send_cmd(struct ipmi_intf *__UNUSED__(intf), struct ipmi_rq *req)
{

	I2CPACKET i2cPacket;
	static struct ipmi_rs rsp;
	int status, i;
	unsigned char ccode;
	unsigned char i2c_buf[20] = "";

	i2cPacket.imb.rsSa	= IPMI_BMC_SLAVE_ADDR;
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
		printf("I2C data    : %x\n", *i2cPacket.imb.data);
		printf("I2C dataLength : %d\n", i2cPacket.imb.dataLength);
		for (i = 0; i < i2cPacket.imb.dataLength ; i++) {
			printf("0x%02x ", i2cPacket.imb.data[i]);
		}

		i2c_buf[0] = ADDR << 1;
		i2c_buf[1] = i2cPacket.imb.netFn << 2; //netfn shifted to make way for the LUN.
		unsigned char checksum = CalculateChecksum(i2c_buf, sizeof(i2c_buf[0]) * 2, 0);
		i2c_buf[2] = checksum;
		i2c_buf[3] = i2cPacket.imb.rsSa << 1; //LUN is 0, no need to add it
		i2c_buf[4] = 0x00; // TODO: Not sure how to do the sequence
		i2c_buf[5] = i2cPacket.imb.cmdType;

		for(int i=0; i < i2cPacket.imb.dataLength; i++) {
			i2c_buf[6+i] = i2cPacket.imb.data[i];
		}

		printf("4\n");
		i2c_buf[6 + i2cPacket.imb.dataLength] = CalculateChecksum(i2c_buf, sizeof(i2c_buf[0]) * 17, 3);

		printf("i2c packet: ");
		for(int i=0; i < 20; i++) {
			printf("%02x ", i2c_buf[i]);
		}

	}

	//rsp.data_len = IPMI_IMB_BUF_SIZE;
	//memset(rsp.data, 0, rsp.data_len);

	// need this to continue
	rsp.ccode = 00;

	return 0;
}

struct ipmi_intf ipmi_i2c_intf = {
	.name = "i2c",
	.desc = "I2C Interface",
	.open = ipmi_i2c_open,
	.close = ipmi_i2c_close,
	.sendrecv = ipmi_i2c_send_cmd,
	.target_addr = IPMI_BMC_SLAVE_ADDR,
};

