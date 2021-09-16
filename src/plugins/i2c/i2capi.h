/*M*
//  PVCS:
//      $Workfile:   imb_api.h  $
//      $Revision: 1.2 $
//      $Modtime:   Jul 22 2002 16:40:32  $
//      $Author: iceblink $
// 
//  Combined include files needed for imbapi.c
//
 *M*/
/*----------------------------------------------------------------------* 
The BSD License 
Copyright (c) 2002, Intel Corporation
All rights reserved.
Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:
  a.. Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer. 
  b.. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution. 
  c.. Neither the name of Intel Corporation nor the names of its contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *----------------------------------------------------------------------*/

#pragma once

#ifndef	_WINDEFS_H
#define	_WINDEFS_H

#include <stddef.h>

#ifndef FALSE
#define FALSE   0
#endif
#ifndef TRUE
#define TRUE    1
#endif
#ifndef NULL
#define NULL 0
#endif
#ifndef WIN32   
/* WIN32 defines this in stdio.h */
#include <wchar.h>
#endif

#define far
#define near
#define FAR                 far
#define NEAR                near
#ifndef CONST
#define CONST               const
#endif
typedef unsigned long       DWORD;
typedef int                 BOOL;
typedef unsigned char       BYTE;
typedef unsigned short      WORD;
typedef float               FLOAT;
typedef FLOAT               *PFLOAT;
typedef BOOL near           *PBOOL;
typedef BOOL far            *LPBOOL;
typedef BYTE near           *PBYTE;
typedef BYTE far            *LPBYTE;
typedef int near            *PINT;
typedef int far             *LPINT;
typedef WORD near           *PWORD;
typedef WORD far            *LPWORD;
typedef long far            *LPLONG;
typedef DWORD near          *PDWORD;
typedef DWORD far           *LPDWORD;
typedef void far            *LPVOID;
typedef CONST void far      *LPCVOID;
typedef int                 INT;
typedef unsigned int        UINT;
typedef unsigned int        *PUINT;
typedef DWORD NTSTATUS;
#endif
/*

/*
 Define the method codes for how buffers are passed for I/O and FS controls
*/
#define METHOD_BUFFERED                 0
/*
 Define the access check value for any access
 The FILE_READ_ACCESS and FILE_WRITE_ACCESS constants are also defined in
 ntioapi.h as FILE_READ_DATA and FILE_WRITE_DATA. The values for these
 constants *MUST* always be in sync.
*/
#define FILE_ANY_ACCESS                 0
/*
  These are the generic rights.
*/
#define    MAX_PATH        260
#define	GetLastError()	(NTstatus.Status)
/*
 Macro definition for defining IOCTL and FSCTL function control codes.  Note
 that function codes 0-2047 are reserved for Microsoft Corporation, and
 2048-4095 are reserved for customers.
*/
/*
 * Linux drivers expect ioctls defined using macros defined in ioctl.h.
 * So, instead of using the CTL_CODE defined for NT and UW, I define CTL_CODE
 * using these macros. That way imb_if.h, where the ioctls are defined get
 * to use the correct ioctl command we expect. 
 * Notes: I am using the generic _IO macro instead of the more specific
 * ones. The macros expect 8bit entities, so I am cleaning what is sent to
 * us from imb_if.h  - Mahendra
 */

#define CTL_CODE( DeviceType, Function, Method, Access ) ((ULONG)(	\
    ((ULONG)(DeviceType) << 16) | ((ULONG)(Access) << 14) | ((ULONG)(Function) << 2) | ((ULONG)Method) \
))

/*
 * This is the structure passed in to the IOCTL_IMB_SHUTDOWN_CODE request
 */
typedef struct {
	int	code;		
	int	delayTime;  
} ShutdownCmdBuffer;
#define		SD_NO_ACTION				0
#define		SD_RESET				1
#define		SD_POWER_OFF				2
#pragma pack(1)

/*
 * This is the generic IMB packet format, the final checksum can't be
 * represented in this structure and will show up as the last data byte
 */
typedef struct {
	BYTE rsSa;
	BYTE nfLn;
	BYTE cSum1;
	BYTE rqSa;
	BYTE seqLn;
	BYTE cmd;
	BYTE data[1];
} ImbPacket;




#define MIN_IMB_PACKET_SIZE	7 	
#define MAX_IMB_PACKET_SIZE	33
/*
 * This is the standard IMB response format where the first byte of
 * IMB packet data is interpreted as a command completion code.
*/
typedef struct {
	BYTE rsSa;
	BYTE nfLn;
	BYTE cSum1;
	BYTE rqSa;
	BYTE seqLn;
	BYTE cmd;
	BYTE cCode;
	BYTE data[1];
} ImbRespPacket;
#define MIN_IMB_RESPONSE_SIZE	7	/* min packet + completion code */
#define MAX_IMB_RESPONSE_SIZE	MAX_IMB_PACKET_SIZE
/************************
 *  ImbRequestBuffer
 ************************/
/*D*
//  Name:       ImbRequestBuffer
//  Purpose:    Structure definition for holding IMB message data
//  Context:    Used by SendTimedImbpMessage and SendTimedI2cMessge
//              functions in the library interface. In use, it is overlayed on a
//				char buffer of size MIN_IMB_REQ_BUF_SIZE + 
//  Fields:     
//              respBufSize     size of the response buffer
//
//              timeout         timeout value in milli seconds   
//                     
//              req		body of request to send
//              
*D*/			
typedef struct {
	BYTE rsSa;
	BYTE cmd;
	BYTE netFn;
	BYTE rsLun;	
	BYTE dataLength;
	BYTE data[1];	
} ImbRequest;

/************************
 *  ImbResponseBuffer
 ************************/
/*D*
//  Name:       ImbResponseBuffer
//  Purpose:    Structure definition for response of a previous send 
//  Context:    Used by DeviceIoControl to pass the message to be sent to
//              MISSMIC port
//  Fields:     
//  		cCode		completion code returned by firmware
//              data		buffer for  response data from firmware
*D*/
typedef struct {
	BYTE       cCode;	
	BYTE       data[1];	
} ImbResponseBuffer;

#define MIN_IMB_RESP_BUF_SIZE	1	
#define MAX_IMB_RESP_SIZE		(MIN_IMB_RESP_BUF_SIZE + MAX_IMB_RESPONSE_SIZE)
#pragma pack()


#ifndef IMBAPI_H__
#define IMBAPI_H__
#include <sys/types.h>
#define	WRITE_READ_I2C		0x52
#define	WRITE_EMP_BUFFER	0x7a
#define	GET_DEVICE_ID		0x1
#define SEND_MESSAGE		0x34
#define BMC_SA			0x20
#define BMC_LUN			0
#define APP_NETFN		0x06
#define	IPMI_09_VERSION		0x90
#define	IPMI_10_VERSION		0x01

#define	IPMI_15_VERSION		0x51

#ifndef IPMI10_GET_DEVICE_ID_RESP_LENGTH
#define IPMI10_GET_DEVICE_ID_RESP_LENGTH	12
#endif

#define IPMB_CHANNEL			0x0
#define	EMP_CHANNEL			0x1
#define LAN_CHANNEL			0x2
#define	RESERVED_LUN			0x3
#define	IPMB_LUN			0x2
#define	EMP_LUN				0x0

#pragma pack(1)
/*
 * Request structure provided to SendTimedImbpRequest()
*/
typedef struct {
	unsigned char	cmdType;
	unsigned char	rsSa;
	unsigned char	busType;	
	unsigned char	netFn;	
	unsigned char	rsLun;	
	unsigned char *	data;	
	int		dataLength;
} IMBREQUESTDATA;

/*
 * Encapsulates ImbPacket inside of an I2C address
 *
 */
typedef struct {
	BYTE i2cAddress; // Need to shift this once, only "writes" are used
	IMBREQUESTDATA imb;
	BYTE cSum2;
} I2CPACKET;

/*
 * Request structure provided to SendTimedI2cRequest()
*/
typedef struct {
	unsigned char	rsSa;				
	unsigned char	busType;		
	unsigned char	numberOfBytesToRead;
	unsigned char *	data;			
	int		dataLength;	
} I2CREQUESTDATA;
#pragma pack()

unsigned char
CalculateChecksum(const unsigned char bytes[], size_t bytesSize);
#endif /* I2CAPI_H__ */
