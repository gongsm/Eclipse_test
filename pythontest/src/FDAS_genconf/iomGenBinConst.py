'''
Created on 30.11.2014

@author: dk

Common constants for IO Manager binary configuration
To be harmonized with IO Manager C Header File
'''

class IOM:
    SIGINTYPE_SIG32      = 0
    SIGINTYPE_SIG64      = 1
    SIGINTYPE_OPAQUE     = 2
    SIGINTYPE_BOOL       = 3
    SIGINTYPE_CODED32    = 4
    SIGINTYPE_CODED64    = 5
    SIGINTYPE_SIG32_I2F  = 6
    SIGINTYPE_SIG32_F2I  = 7
    SIGINTYPE_BNR        = 8
    SIGINTYPE_UBNR       = 9
    SIGINTYPE_BCD        = 10
    SIGINTYPE_UBCD       = 11
    SIGINTYPE_BNR_F2I    = 12
    SIGINTYPE_UBNR_F2I   = 13
    SIGINTYPE_BCD_F2I    = 14
    SIGINTYPE_UBCD_F2I   = 15
    SIGINTYPE_INT8       = 16
    SIGINTYPE_INT16      = 17
    SIGINTYPE_UINT8      = 18
    SIGINTYPE_UINT16     = 19
    SIGINTYPE_INT8_ADD   = 20
    SIGINTYPE_STRINGS    = 21                # not implemented yet
    SIGINTYPE_FLOATS     = 22
    
    SIGOUTTYPE_SIG32              = 0        # Input Mapping Type: Read 32bits word */
    SIGOUTTYPE_MULTIPLE_BYTES     = 1        # Input Mapping Type: Read Multiple Bytes */
    SIGOUTTYPE_A664_BOOLEAN       = 2        # Input Mapping Type: A664 Boolean */
    SIGOUTTYPE_BITFIELD32         = 3        # Input Mapping Type: A664 Boolean */
    SIGOUTTYPE_A429BNR_FLOAT      = 4        # A429 BNR conversion from Float*/
    SIGOUTTYPE_A429UBNR_FLOAT     = 5        # A429 UBNR conversion from Float*/
    SIGOUTTYPE_A429BNR_INTEGER    = 6        # A429 BNR conversion from Integer*/
    SIGOUTTYPE_A429UBNR_INTEGER   = 7        # A429 UBNR conversion from Integer*/
    SIGOUTTYPE_A429BCD_FLOAT      = 8        # A429 BCD conversion froom Float*/
    SIGOUTTYPE_A429BCD_INTEGER    = 9        # A429 BCD conversion froom Integer*/

    CONDTYPE_FRESHNESS     = 0
    CONDTYPE_A664FS        = 1
    CONDTYPE_MASKVALUE     = 2
    CONDTYPE_A429SSM_BNR   = 3
    CONDTYPE_A429SSM_DIS   = 4       
    CONDTYPE_A429SSM_BCD   = 5       
    
    A664_MESSAGE_PADDING                 = 64
    A664_MESSAGE_HEADER_LENGTH           = 64
    A664_MESSAGE_HEADER_FRESHNESS_OFFSET = 0


