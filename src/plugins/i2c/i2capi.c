/*
 * Copyright (c) 2002, Intel Corporation
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
 * Neither the name of Intel Corporation nor the names of its
 * contributors may be used to endorse or promote products derived
 * from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

/* Purpose: This file contains the entry point that opens the IMB device in
 * order to issue the  IMB driver API related IOCTLs. This file implements the
 * IMB driver API for the Server Management Agents
 */


/* Use -DLINUX_DEBUG_MAX in the Makefile, resp. CFLAGS if you want a dump of the
 * memory to debug mmap system call in MapPhysicalMemory() below.
 */

#define IMB_API


# include <fcntl.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/ioctl.h>
# include <sys/mman.h>
# include <sys/param.h>
# include <sys/stat.h>
# include <sys/types.h>
# include <unistd.h>


#include "i2capi.h"
#include <sys/socket.h>
#include <ipmitool/helper.h>
#include <ipmitool/log.h>


unsigned char
CalculateChecksum(const unsigned char bytes[], size_t bytesSize)
{
    int i;
    unsigned char checksum = 0;
    for (i = 0; i < (bytesSize / sizeof(bytes[0])); i++) {
        checksum += bytes[i];
    }
    checksum = ~checksum + 1;
    return checksum;
}
