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

extern int verbose;

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
	printf("Pew Pew\n");

	IMBREQUESTDATA imbreq;
	static struct ipmi_rs rsp;
	int status, i;
	unsigned char ccode;

	imbreq.rsSa	= IPMI_BMC_SLAVE_ADDR;
	imbreq.rsLun	= 0;
	imbreq.busType	= 0;
	imbreq.netFn	= req->msg.netfn;
	imbreq.cmdType	= req->msg.cmd;

	imbreq.data = req->msg.data;
	imbreq.dataLength = req->msg.data_len;

	if (verbose > 1) {
		printf("I2C rsSa       : %x\n", imbreq.rsSa);
		printf("I2C netFn      : %x\n", imbreq.netFn);
		printf("I2C cmdType    : %x\n", imbreq.cmdType);
		printf("I2C data    : %x\n", *imbreq.data);
		printf("I2C dataLength : %d\n", imbreq.dataLength);
		for (i = 0; i < imbreq.dataLength ; i++) {
			printf("0x%02x ", imbreq.data[i]);
		}
		printf("\n");

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

