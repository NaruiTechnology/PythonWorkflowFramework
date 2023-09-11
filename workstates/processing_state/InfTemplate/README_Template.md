**Copyright (c) 1995-2019 Intel Corporation.**

This software and the related documents are Intel copyrighted materials, and your use of them is governed by the express license under which they were provided to you ("License"). Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose or transmit this software or the related documents without Intel's prior written permission.

This software and the related documents are provided as is, with no express or implied warranties, other than those that are expressly stated in the License.

**Microcode Updates/System Configuration Data are platform specific and are intended for installation in the BIOS or the Operating System.**  

**DO NOT USE THESE MICROCODE UPDATES/SYSTEM CONFIGURATION DATA ON UNINTENDED PROCESSORS!**

Please see the following document for further information on Microcode Updates/System Configuration Data and the INT15 BIOS Update API: "Intel(R) 64 and IA-32 Architectures Software Developer's Manual Volume 3A: System Programming Guide", document # 253668 (253668-037US), Section 9.11 Microcode Update Facilities.

# ASCII-Encoded Binary File Name Format

The ASCII-encoded binary version of Microcode Updates use the following naming conventions:

"mxxyyyyy_zzzzzzzz.inc", where:  
   "m"        = Microcode Update (System Configuration Data).  
   "xx"       = Reflects the Processor Flags field from the Microcode Update Header.  
   "yyyyy"    = Reflects the processor signature as reported by CPUID instruction.  
   "zzzzzzzz" = Reflects the revision number of the System Configuration Data for the particular stepping.  

"m_xx_yyyyy_zzzzzzzz.inc", where:  
   "m"        = Microcode Update (System Configuration Data).  
   "xx"       = Reflects the Processor Flags field from the Microcode Update Header.  
   "yyyyy"    = Reflects the processor signature as reported by CPUID instruction.  
   "zzzzzzzz" = Reflects the revision number of the System Configuration Data for the particular stepping.  

"mxxyyyyyzz.inc", where:  
   "m"     = Microcode Update (System Configuration Data).  
   "xx"    = Reflects the Processor Flags field from the Microcode Update Header.  
   "yyyyy" = Reflects the processor signature as reported by CPUID instruction.  
   "zz"    = Reflects the revision number of the System Configuration Data for the particular stepping.  

"maabcdef.inc", where:  
   "m"   = Microcode Update (System Configuration Data).  
   "aa"  = Reflects the Processor Flags field from the Microcode Update Header.  
   "b"   = Reflects the family as reported by CPUID instruction.  
   "c"   = Reflects the model as reported by CPUID instruction.  
   "d"   = Reflects the stepping as reported by CPUID instruction.  
   "ef"  = Reflects the revision number of the System Configuration Data for the particular stepping.  

"muabcdef.inc", where:
   "mu"  = Microcode Update (System Configuration Data).  
   "a"   = Designates 1 for Value or Performance, 2 for Server/Workstation, etc.  
   "b"   = Reflects the family as reported by CPUID instruction.  
   "c"   = Reflects the model as reported by CPUID instruction.  
   "d"   = Reflects the stepping as reported by CPUID instruction.  
   "ef"  = Reflects the revision number of the System Configuration Data for the particular stepping.  

# Linux File Name Format

For use with Linux operating systems, microcode updates need to be first compiled from the assembly version into a binary.  The capability to perform this is now provided via the tool MicrocodeConverter.py.  Linux formated microcode updates use a different file naming format than the assembly files.  For Linux, they are represented in the following format:  

"F-MO-S", where:  
   "F"  = Processor Family  
   "MO" = Processor Model  
   "S"  = Processor Stepping  

For example, if a processor returns a CPUID value of "0x000906eb":

| Reserved | Extended Family | Extended Model | Reserved | Processor Type | Family Code | Model Number | Stepping ID
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 31:28 | 27:20 | 19:16 | 15:14 | 13:12 | 11:8 | 7:4 | 3:0
| xxxx | 00000000b | 1001b | xx | 00b | 0110b | 1110b | 1011b  

The corresponding Linux formatted file name will be "06-9e-0b", where:  
   Extended Family + Family  = 0x06  
   Extended Model + Model Number = 0x9e  
   Stepping ID  = 0xb

# Table of Available Microcode Updates  

The below table provides a list of Microcode update file names with the revision number removed from the end of the file name.  These are then cross-referenced to Intel's codename for the processor, CPUID information and links to the microprocessor specification update (where available) and the Intel Product specifications page for the related microprocessors.

| CPU Segment | Microcode File Name | CPU Code Name | CPU Core Stepping | Platform ID | CPUID | CPU Public Spec Update | Intel Product Specifications
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Desktop | m0110661 | Conroe L | A-1 | 01 | 00010661 | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m01106c2 | Silverthorne | C-0 | 01 | 000106C2 | N/A | [Specs](https://ark.intel.com/products/codename/24976/Silverthorne#@Silverthorne)
| Desktop | m01106ca | Pineview SC | A-0 | 01 | 000106CA | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-n400-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32201/Pineview#@Pineview)
| Desktop | m016f2 | Conroe | L-2 | 01 | 000006F2 | [Update](https://www.intel.com/content/www/us/en/support/articles/000008591/processors.html?wapkw=legacy+pentium) | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m016f6 | Conroe | B-2 | 01 | 000006F6 | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m016f6 | Conroe XE | B-2 | 01 | 000006F6 | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m016fb | Conroe | G-0 | 01 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m016fd | Conroe | M-0 | 01 | 000006FD | [Update](https://www.intel.com/content/www/us/en/support/articles/000008591/processors.html?wapkw=legacy+pentium) | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@desktop)
| Desktop | m01f07 | Willamette (423-pin) | B-2 | 01 | 00000F07 | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m01f0a | Willamette (423-pin) | C-1 | 01 | 00000F0A | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m01f12 | Willamette (423-pin) | D-0 | 01 | 00000F12 | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m02906eb | Coffee Lake-S + CNL PCH | B-0 | 02 | 000906EB | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m02906eb | Coffee Lake-S + KBL PCH | B-0 | 02 | 000906EB | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m03106a4 | Bloomfield | C-0 | 03 | 000106A4 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-900-ee-and-desktop-processor-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/28102/Bloomfield#@Bloomfield)
| Desktop | m03106a5 | Bloomfield | D-0 | 03 | 000106A5 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-900-ee-and-desktop-processor-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/28102/Bloomfield#@Bloomfield)
| Desktop | m03206C2 | Gulftown | B-1 | 03 | 000206C2 | N/A | [Specs](https://ark.intel.com/products/codename/29886/Gulftown#@Gulftown)
| Desktop | m04106ca | Pineview SC | B-0 | 04 | 000106CA | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-processor-n500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32201/Pineview#@Pineview)
| Desktop | m04106C2 | Diamondville SC | C-0 | 04 | 000106C2 | N/A | [Specs](https://ark.intel.com/products/codename/32202/Diamondville#@Diamondville)
| Desktop | m04f0a | Willamette-N (478-pin) | C-1 | 04 | 00000F0A | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m04f12 | Willamette-N (478-pin) | D-0 | 04 | 00000F12 | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m04f13 | Willamette-N (478-pin) | E-0 | 04 | 00000F13 | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m04f13 | Willamette-N ICP (478-pin) | E-0 | 04 | 00000F13 | N/A | [Specs](https://ark.intel.com/products/codename/1777/Willamette#@Willamette)
| Desktop | m04f24 | Northwood-N | B-0 | 04 | 00000F24 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f25 | Northwood-N | M-0 | 04 | 00000F25 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f27 | Northwood-N | C-1 | 04 | 00000F27 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f27 | Northwood-N ICP | C-1 | 04 | 00000F27 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f29 | Northwood-N | D-1 | 04 | 00000F29 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f29 | Northwood-N ICP | D-1 | 04 | 00000F29 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m04f62 | Cedar Mill | B-1 | 04 | 00000F62 | N/A | [Specs](https://ark.intel.com/products/codename/2679/Cedarmill#@Cedarmill)
| Desktop | m04f62 | Presler | B-1 | 04 | 00000F62 | N/A | [Specs](https://ark.intel.com/products/codename/8020/Presler#@Presler)
| Desktop | m04f65 | Cedar Mill | D-0 | 04 | 00000F65 | N/A | [Specs](https://ark.intel.com/products/codename/2679/Cedarmill#@Cedarmill)
| Desktop | m04f65 | Cedar Mill ICP | D-0 | 04 | 00000F65 | N/A | [Specs](https://ark.intel.com/products/codename/2679/Cedarmill#@Cedarmill)
| Desktop | m04f65 | Presler | D-0 | 04 | 00000F65 | N/A | [Specs](https://ark.intel.com/products/codename/8020/Presler#@Presler)
| Desktop | m08106c2 | Diamondville DC | C-0 | 08 | 000106C2 | N/A | [Specs](https://ark.intel.com/products/codename/32202/Diamondville#@Diamondville)
| Desktop | m08106ca | Pineview DC | B-0 | 08 | 000106CA | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-d500-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32201/Pineview#@Pineview)
| Desktop | m0c30673 | Baytrail | B-2 | 0C | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Desktop | m0c30673 | Baytrail | B-3 | 0C | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Desktop | m0c30678 | Baytrail | C-0 | 0C | 00030678 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Desktop | m0df32 | Prescott-N ICP | B-1 | 0D | 00000F32 | N/A | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m0df33 | Prescott-N | C-0 | 0D | 00000F33 | N/A | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m0df33 | Prescott-N ICP | C-0 | 0D | 00000F33 | N/A | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m0f30679 | Baytrail | D-0 | 0F | 00030679 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Desktop | m0f30679 | Baytrail | D-1 | 0F | 00030679 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Desktop | m1010677 | Yorkfield | C-1 | 10 | 00010677 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@desktop)
| Desktop | m1010677 | Yorkfield | M-1 | 10 | 00010677 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@desktop)
| Desktop | m1010677 | Yorkfield XE | C-1 | 10 | 00010677 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@desktop)
| Desktop | m10106ca | Pineview DC | B-0 | 10 | 000106CA | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-d500-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32201/Pineview#@Pineview)
| Desktop | m106f7 | Kentsfield | B-3 | 10 | 000006F7 | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield#@desktop)
| Desktop | m106f7 | Kentsfield XE | B-3 | 10 | 000006F7 | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield#@desktop)
| Desktop | m106fb | Kentsfield | G-0 | 10 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield#@desktop)
| Desktop | m106fb | Kentsfield XE | G-0 | 10 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield#@desktop)
| Desktop | m10f25 | Northwood-T | M-0 | 10 | 00000F25 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Desktop | m1220652 | Clarkdale | C-2 | 12 | 00020652 | N/A | [Specs](https://ark.intel.com/products/codename/29890/Clarkdale?q=clarkdale#@desktop)
| Desktop | m12206a7 | Sandy Bridge | Q-0 | 12 | 000206A7 | [Update](https://www.intel.com/content/www/us/en/embedded/products/sugar-bay/2nd-gen-core-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29900/Sandy-Bridge#@desktop)
| Desktop | m12206a7 | Sandy Bridge | D-2 | 12 | 000206A7 | [Update](https://www.intel.com/content/www/us/en/embedded/products/sugar-bay/2nd-gen-core-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29900/Sandy-Bridge#@desktop)
| Desktop | m12306a9 | Ivy Bridge | E-1 | 12 | 000306A9 | N/A | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@desktop)
| Desktop | m12306a9 | Ivy Bridge | L-1 | 12 | 000306A9 | N/A | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@desktop)
| Desktop | m13106e5 | Lynnfield | B-1 | 13 | 000106E5 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-800-i5-700-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29896/Lynnfield#@desktop)
| Desktop | m1df34 | Prescott-N ICP, Prescott-T ICP | D-0 | 1D | 00000F34 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m1df34 | Prescott-N, Prescott-T | D-0 | 1D | 00000F34 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m2240671 | Broadwell-H | E-0 | 22 | 00040671 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-mobile-5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@desktop)
| Desktop | m2240671 | Broadwell-H | G-0 | 22 | 00040671 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-mobile-5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@desktop)
| Desktop | m22906ea | Coffee Lake-S + CNL PCH | U-0 | 22 | 000906EA | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m22906ea | Coffee Lake-S + KBL PCH | U-0 | 22 | 000906EA | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m22906ec | Coffee Lake-S + CNL PCH | P-0 | 22 | 000906EC | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m22906ec | Coffee Lake-S + KBL PCH | P-0 | 22 | 000906EC | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m22906ed | Coffee Lake-S + CNL PCH | R-0 | 22 | 000906ED | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m22906ed | Coffee Lake-S + KBL PCH | R-0 | 22 | 000906ED | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@desktop)
| Desktop | m2a906e9 | Kaby Lake-S | B-0 | 2A | 000906E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@desktop)
| Desktop | m2a906e9 | Kaby Lake-X | B-0 | 2A | 000906E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@desktop)
| Desktop | m32306c3 | Haswell | C-0 | 32 | 000306C3 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@desktop)
| Desktop | m3240661 | Haswell Perf Halo | C-0 | 32 | 00040661 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@desktop)
| Desktop | m34f64 | Cedar Mill | C-1 | 34 | 00000F64 | N/A | [Specs](https://ark.intel.com/products/codename/2679/Cedarmill#@Cedarmill)
| Desktop | m34f64 | Cedar Mill ICP | C-1 | 34 | 00000F64 | N/A | [Specs](https://ark.intel.com/products/codename/2679/Cedarmill#@Cedarmill)
| Desktop | m34f64 | Presler | C-1 | 34 | 00000F64 | N/A | [Specs](https://ark.intel.com/products/codename/8020/Presler#@Presler)
| Desktop | m34f64 | Presler XE | C-1 | 34 | 00000F64 | N/A | [Specs](https://ark.intel.com/products/codename/8020/Presler#@Presler)
| Desktop | m36506e3 | Skylake-S | R-0 | 36 | 000506E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@desktop)
| Desktop | m36506e3 | Skylake-S | S-0 | 36 | 000506E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@desktop)
| Desktop | m5cf4a | Prescott 2M-T | R-0 | 5C | 00000F4A | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m6d206d6 | Sandy Bridge-E | C-1 | 6D | 000206D6 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-lga-2011-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/63378/Sandy-Bridge-E#@Sandy-Bridge-E)
| Desktop | m6d206d6 | Sandy Bridge-E | M-0 | 6D | 000206D6 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-lga-2011-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/63378/Sandy-Bridge-E#@Sandy-Bridge-E)
| Desktop | m6d206d7 | Sandy Bridge-E | C-2 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-lga-2011-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/63378/Sandy-Bridge-E#@Sandy-Bridge-E)
| Desktop | m6d206d7 | Sandy Bridge-E | M-1 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-lga-2011-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/63378/Sandy-Bridge-E#@Sandy-Bridge-E)
| Desktop | m6f306f2 | Haswell-E | R-2 | 6F | 000306F2 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-lga2011-3-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/79427/Haswell-E#@Haswell-E)
| Desktop | m9110676 | Wolfdale | M-0 | 91 | 00010676 | [Update](https://www.intel.com/content/www/us/en/support/articles/000008591/processors.html?wapkw=legacy+pentium) | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale#@Wolfdale)
| Desktop | m9220655 | Clarkdale | K-0 | 92 | 00020655 | N/A | [Specs](https://ark.intel.com/products/codename/29890/Clarkdale?q=clarkdale#@desktop)
| Desktop | m9df43 | Prescott 2M-T | N-0 | 9D | 00000F43 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | m9df44 | Smithfield | A-0 | 9D | 00000F44 | N/A | [Specs](https://ark.intel.com/products/codename/5788/Smithfield#@Smithfield)
| Desktop | m9df47 | Smithfield | B-0 | 9D | 00000F47 | N/A | [Specs](https://ark.intel.com/products/codename/5788/Smithfield#@Smithfield)
| Desktop | mb11067a | Wolfdale | E-0 | B1 | 0001067A | [Update](https://www.intel.com/content/www/us/en/support/articles/000008591/processors.html?wapkw=legacy+pentium) | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale#@Wolfdale)
| Desktop | mb11067b | Wolfdale | R-0 | B1 | 0001067A | [Update](https://www.intel.com/content/www/us/en/support/articles/000008591/processors.html?wapkw=legacy+pentium) | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale#@Wolfdale)
| Desktop | mb11067a | Yorkfield | E-0 | B1 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@desktop)
| Desktop | mb11067a | Yorkfield | R-0 | B1 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@desktop)
| Desktop | mb750654 | Skylake-X | M-0 | B7 | 00050654 | [Update](https://www.intel.com/content/www/us/en/products/processors/core/6th-gen-x-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@desktop)
| Desktop | mb750654 | Skylake-X | U-0 | B7 | 00050654 | [Update](https://www.intel.com/content/www/us/en/products/processors/core/6th-gen-x-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@desktop)
| Desktop | mbf50657 | Cascade Lake | L-1  | BF | 00050657 | N/A | N/A
| Desktop | mbdf41 | Prescott-N ICP, Prescott-T ICP | E-0 | BD | 00000F41 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | mbdf41 | Prescott-N, Prescott-T | E-0 | BD | 00000F41 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | mbdf49 | Prescott-N ICP, Prescott-T ICP | G-1 | BD | 00000F49 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | mbdf49 | Prescott-N, Prescott-T | G-1 | BD | 00000F49 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1791/Prescott#@Prescott)
| Desktop | med306e4 | Ivy Bridge-E | S-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/67456/Ivy-Bridge-E#@Ivy-Bridge-E)
| Desktop | mef406f1 | Broadwell-E | R-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/core/core-i7-6xxx-lga2011-v3-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@desktop)
| Desktop | mu1633 | Klamath | C-0 | 1 | 00000633 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1634 | Klamath | C-1 | 1 | 00000634 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1650 | Covington ICP | A-0 | 1 | 00000650 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1650 | Deschutes | A-0 | 1 | 00000650 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1651 | Covington ICP | A-1 | 1 | 00000651 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1651 | Deschutes | A-1 | 1 | 00000651 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1652 | Deschutes | B-0 | 1 | 00000652 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1653 | Deschutes | B-1 | 1 | 00000653 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Desktop | mu1660 | Mendicino ICP | A-0 | 1 | 00000660 | N/A | [Specs](https://ark.intel.com/products/codename/26586/Mendocino#@Mendocino)
| Desktop | mu1665 | Mendicino ICP | B-0 | 1 | 00000665 | N/A | [Specs](https://ark.intel.com/products/codename/26586/Mendocino#@Mendocino)
| Desktop | mu166a | Dixon | A-1 | 1 | 0000066A | N/A | [Specs](https://ark.intel.com/products/codename/1912/Dixon?q=dixon)
| Desktop | mu166d | Dixon | A-1 | 1 | 0000066D | N/A | [Specs](https://ark.intel.com/products/codename/1912/Dixon?q=dixon)
| Desktop | mu1672 | Katmai (SECC2) | B-0 | 1 | 00000672 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1938/Katmai#@Katmai)
| Desktop | mu1673 | Katmai (SECC2) | C-0 | 1 | 00000673 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1938/Katmai#@Katmai)
| Desktop | mu1681 | Coppermine (FCPGA) | A-2 | 1 | 00000681 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1681 | Coppermine (SECC2) | A-2 | 1 | 00000681 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1683 | Coppermine (FCPGA) | B-0 | 1 | 00000683 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1683 | Coppermine (SECC2) | B-0 | 1 | 00000683 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1683 | Coppermine ICP | B-0 | 1 | 00000683 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1686 | Coppermine (FCPGA) | C-0 | 1 | 00000686 | [Update](https://downloadcenter.intel.com/download/24320/Archived-documents-for-Intel-Pentium-II-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1686 | Coppermine (SECC2) | C-0 | 1 | 00000686 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu1686 | Coppermine ICP (FCPGA) | C-0 | 1 | 00000686 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu168a | Coppermine (PGA370) | D-0 | 1 | 0000068A | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu168a | Coppermine ICP | D-0 | 1 | 0000068A | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1903/Coppermine#@Coppermine)
| Desktop | mu16b1 | Tualatin (FC-PGA2) | A-1 | 1 | 000006B1 | [Update](https://downloadcenter.intel.com/download/24361/Archived-documents-for-Mobile-Intel-Pentium-III-Processor) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@Tualatin)
| Desktop | mu16b1 | Tualatin ICP (FC-PGA2) | A-1 | 1 | 000006B1 | [Update](https://downloadcenter.intel.com/download/24361/Archived-documents-for-Mobile-Intel-Pentium-III-Processor) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@Tualatin)
| Desktop | mu16b4 | Tualatin (FC-PGA2) | B-1 | 1 | 000006B4 | [Update](https://downloadcenter.intel.com/download/24361/Archived-documents-for-Mobile-Intel-Pentium-III-Processor) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@Tualatin)
| Desktop | mu16b4 | Tualatin ICP (FC-PGA2) | B-1 | 1 | 000006B4 | [Update](https://downloadcenter.intel.com/download/24361/Archived-documents-for-Mobile-Intel-Pentium-III-Processor) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@Tualatin)
| Mobile | m01406a8 | Tangier | B-0 | 01 | 000406A8 | N/A | [Specs](https://ark.intel.com/products/codename/41559/Merrifield)
| Mobile | m01406a8 | Tangier | C-0 | 01 | 000406A8 | N/A | [Specs](https://ark.intel.com/products/codename/41559/Merrifield)
| Mobile | m0210661 | Penryn | A-1 | 02 | 00010661 | N/A | [Specs](https://ark.intel.com/products/codename/26543/Penryn#@Penryn)
| Mobile | m08f27 | Northwood-N | E-1 | 08 | 00000F27 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Mobile | m08f29 | Northwood-N | I-0 | 08 | 00000F29 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood#@Northwood)
| Mobile | m0c30673 | Baytrail | B-2 | 0C | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Mobile | m0c30673 | Baytrail | B-3 | 0C | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Mobile | m0c30678 | Baytrail | C-0 | 0C | 00030678 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Mobile | m0f30679 | Baytrail | D-0 | 0F | 00030679 | N/A | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Mobile | m0f30679 | Baytrail | D-1 | 0F | 00030679 | N/A | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| Mobile | m10695 | Banias | B-1 | 10 | 00000695 | N/A | [Specs](https://ark.intel.com/products/codename/1788/Banias?q=banias)
| Mobile | m10806e9 | Amber Lake-Y/22  | H-0 | 10 | 000806E9 | N/A | [Specs](https://ark.intel.com/products/codename/186968/Amber-Lake-Y#@Amber-Lake-Y)
| Mobile | m10f24 | Northwood-N | B-0 | 10 | 00000F24 | N/A | [Specs](https://ark.intel.com/products/codename/1837/Northwood?q=Northwood)
| Mobile | m1220652 | Arrandale | C-2 | 12 | 00020652 | [Update](https://www.intel.com/content/www/us/en/embedded/products/calpella/core-mobile-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32724/Arrandale#@Arrandale)
| Mobile | m12206a7 | Sandy Bridge | D-2 | 12 | 000206A7 | [Update](https://www.intel.com/content/www/us/en/embedded/products/sugar-bay/2nd-gen-core-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29900/Sandy-Bridge#@mobile)
| Mobile | m12206a7 | Sandy Bridge | J-1 | 12 | 000206A7 | [Update](https://www.intel.com/content/www/us/en/embedded/products/sugar-bay/2nd-gen-core-desktop-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29900/Sandy-Bridge#@mobile)
| Mobile | m12306a9 | Ivy Bridge | E-1 | 12 | 000306A9 | N/A | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@mobile)
| Mobile | m12306a9 | Ivy Bridge | L-1 | 12 | 000306A9 | N/A | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@mobile)
| Mobile | m13106e5 | Clarksfield | B-1 | 13 | 000106E5 | N/A | [Specs](https://ark.intel.com/products/codename/29898/Clarksfield#@Clarksfield)
| Mobile | m20695 | Banias | B-1 | 20 | 00000695 | N/A | [Specs](https://ark.intel.com/products/codename/1788/Banias?q=banias)
| Mobile | m206d6 | Dothan | B-0 | 20 | 000006D6 | N/A | [Specs](https://ark.intel.com/products/codename/2643/Dothan?q=dothan)
| Mobile | m206e8 | Yonah | C-0 | 20 | 000006E8 | N/A | [Specs](https://ark.intel.com/products/codename/2673/Yonah?q=yonah)
| Mobile | m206ec | Yonah | E-0 | 20 | 000006EC | N/A | [Specs](https://ark.intel.com/products/codename/2673/Yonah?q=yonah)
| Mobile | m206f2 | Merom | L-2 | 20 | 000006F2 | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m206f6 | Merom | B-2 | 20 | 000006F6 | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m206fb | Merom | G-0 | 20 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m206fd | Merom | M-0 | 20 | 000006FD | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m2240671 | Broadwell-H | G-0 | 22 | 00040671 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-mobile-5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@mobile)
| Mobile | m22906ea | Coffee Lake-H | U-0 | 22 | 000906EA | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@mobile)
| Mobile | m22906ed | Coffee Lake-H | R-0 | 22 | 000906ED | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/core/8th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@mobile)
| Mobile | m22906ed | Comet Lake-H82 ES | R-0 | 22 | 000906ED | N/A | N/A
| Mobile | m22a0650 | Comet Lake-S62 | G-0 | 22 | 000A0650 | N/A | N/A
| Mobile | m22a0651 | Comet Lake-S102 | P-0 | 22 | 000A0651 | N/A | N/A
| Mobile | m2a906e9 | Kaby Lake-G | B-0 | 2A | 000906E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/136847/Kaby-Lake-G#@Kaby-Lake-G)
| Mobile | m2a906e9 | Kaby Lake-H | B-0 | 2A | 000906E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@mobile)
| Mobile | m32306c3 | Haswell M | C-0 | 32 | 000306C3 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-mobile-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@mobile)
| Mobile | m3240661 | Haswell Perf Halo | C-0 | 32 | 00040661 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-mobile-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@mobile)
| Mobile | m36506e3 | Skylake-H | N-0 | 36 | 000506E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@mobile)
| Mobile | m36506e3 | Skylake-H | R-0 | 36 | 000506E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@mobile)
| Mobile | m7240651 | Haswell ULT | C-0 | 72 | 00040651 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-mobile-specification-update.html?wapkw=4th+generation+update+spec) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@mobile)
| Mobile | m7240651 | Haswell ULT | D-0 | 72 | 00040651 | [Update](https://www.intel.com/content/www/us/en/processors/core/4th-gen-core-family-mobile-specification-update.html?wapkw=4th+generation+update+spec) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@mobile)
| Mobile | m8010661 | Penryn | A-1 | 80 | 00010661 | N/A | [Specs](https://ark.intel.com/products/codename/26543/Penryn#@Penryn)
| Mobile | m80695 | Banias | B-1 | 80 | 00000695 | N/A | [Specs](https://ark.intel.com/products/codename/1788/Banias?q=banias)
| Mobile | m806ec | Yonah | E-0 | 80 | 000006EC | N/A | [Specs](https://ark.intel.com/products/codename/2673/Yonah?q=yonah)
| Mobile | m806fa | Merom | E-1 | 80 | 000006FA | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m806fb | Merom | G-0 | 80 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m806fd | Merom | M-0 | 80 | 000006FD | N/A | [Specs](https://ark.intel.com/products/codename/2683/Merom?q=merom)
| Mobile | m8060663 | Cannon Lake U | D-0 | 80 | 00060663 | N/A | N/A
| Mobile | m80706e1 | Ice Lake Y42/U42 ES1 | B-0 | 80 | 000706E1 | N/A | N/A
| Mobile | m80706e1 | Ice Lake Y42/U42 ES2 | B-4 | 80 | 000706E2 | N/A | N/A
| Mobile | m80706e5 | Ice Lake Y42 | D-1 | 80 | 000706E5 | N/A | N/A
| Mobile | m80706e5 | Ice Lake U42 | D-1 | 80 | 000706E5 | N/A | N/A
| Mobile | m80806c0 | Tiger Lake U | A-0 | 80 | 000806c0 | N/A | N/A
| Mobile | m80a0660 | Comet Lake U62 | A-0 | 80 | 000A0660 | N/A | N/A
| Mobile | m80a0661 | Comet Lake U62 V2 | K-0 | 80 | 000A0661 | N/A | N/A
| Mobile | m90806ec | Whiskey Lake U42 | V-0 | 90 | 000806EC | N/A | N/A
| Mobile | m9220655 | Arrandale | K-0 | 92 | 00020655 | [Update](https://www.intel.com/content/www/us/en/embedded/products/calpella/core-mobile-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/32724/Arrandale#@Arrandale)
| Mobile | m94806ec | Amber Lake Y42 | V-0 | 94 | 000806EC | N/A | N/A
| Mobile | m94806ec | Comet Lake U42 v1 | V-0 | 94 | 000806EC | N/A | N/A
| Mobile | m94806ec | Whiskey Lake U42 | V-0 | 94 | 000806EC | N/A | N/A
| Mobile | mc0306d4 | Broadwell U | E-0 | C0 | 000306D4 | [Update](https://www.intel.com/content/www/us/en/processors/core/5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@mobile)
| Mobile | mc0306d4 | Broadwell U | F-0 | C0 | 000306D4 | [Update](https://www.intel.com/content/www/us/en/processors/core/5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@mobile)
| Mobile | mc0306d4 | Broadwell Y | E-0 | C0 | 000306D4 | [Update](https://www.intel.com/content/www/us/en/processors/core/5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@mobile)
| Mobile | mc0306d4 | Broadwell Y | F-0 | C0 | 000306D4 | [Update](https://www.intel.com/content/www/us/en/processors/core/5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@mobile)
| Mobile | mc0406e3 | Skylake-U/Y | D-0 | C0 | 000406E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@mobile)
| Mobile | mc0406e3 | Skylake-U23e | K-1 | C0 | 000406E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake#@mobile)
| Mobile | mc0806e9 | Kaby Lake-U/Y | H-0 | C0 | 000806E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@mobile)
| Mobile | mc0806e9 | Kaby Lake-U23e | J-1 | C0 | 000806E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@mobile)
| Mobile | mc0806ea | Coffee Lake-U43e | D-0 | C0 | 000806EA | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@mobile)
| Mobile | mc0806ea | Kaby Lake Refresh U | Y-0 | C0 | 000806EA | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/126287/Kaby-Lake-R#@Kaby-Lake-R)
| Mobile | mc0806ec | Whiskey Lake-U42 | W-0 | D0 | 000806EB | N/A | [Specs](https://ark.intel.com/products/codename/135883/Whiskey-Lake#@Whiskey-Lake)
| Mobile | md0806ec | Whiskey Lake-U42 | W-0 | D0 | 000806EB | N/A | [Specs](https://ark.intel.com/products/codename/135883/Whiskey-Lake#@Whiskey-Lake)
| Server | m01406d8 | Avoton/Rangeley | B-0 | 01 | 000406D8 | N/A | [Specs](https://ark.intel.com/products/codename/54859/Avoton?q=avoton)
| Server | m01406d8 | Avoton/Rangeley | C-0 | 01 | 000406D8 | N/A | [Specs](https://ark.intel.com/products/codename/54859/Avoton?q=avoton)
| Server | m016f2 | Conroe Xeon | L-2 | 01 | 000006F2 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-dual-core-desktop-e2000-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@server)
| Server | m016f6 | Conroe Xeon | B-2 | 01 | 000006F6 | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@server)
| Server | m016fb | Conroe Xeon | G-0 | 01 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/2680/Conroe#@server)
| Server | m01f25 | Prestonia x-M | M-0 | 01 | 00000F25 | N/A | [Specs](https://ark.intel.com/products/codename/1838/Prestonia?q=prestonia)
| Server | m01f48 | Paxville DP | A-0 | 01 | 00000F48 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-7000-series-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/6191/Paxville?q=paxville)
| Server | m01f64 | Dempsey | C-1 | 01 | 00000F64 | N/A | [Specs](https://ark.intel.com/products/codename/8019/Dempsey#@Dempsey)
| Server | m01f65 | Dempsey | D-0 | 01 | 00000F65 | N/A | [Specs](https://ark.intel.com/products/codename/8019/Dempsey?q=dempsey)
| Server | m02906eb | Coffee Lake S 4+2 Xeon E3 | B-0 | 02 | 000906EB | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@server)
| Server | m02f07 | Foster DP | B-2 | 02 | 00000F07 | N/A | [Specs](https://ark.intel.com/products/codename/1923/Foster#@Foster)
| Server | m02f0a | Foster DP | C-1 | 02 | 00000F0A | N/A | [Specs](https://ark.intel.com/products/codename/1923/Foster#@Foster)
| Server | m02f11 | Foster MP | C-0 | 02 | 00000F11 | N/A | [Specs](https://ark.intel.com/products/codename/1923/Foster#@Foster)
| Server | m02f12 | Foster DP | D-0 | 02 | 00000F12 | N/A | [Specs](https://ark.intel.com/products/codename/1923/Foster#@Foster)
| Server | m02f22 | Gallatin | A-0 | 02 | 00000F22 | N/A | [Specs](https://ark.intel.com/products/codename/1927/Gallatin#@Gallatin)
| Server | m02f24 | Prestonia | B-0 | 02 | 00000F24 | N/A | [Specs](https://ark.intel.com/products/codename/1838/Prestonia?q=prestonia)
| Server | m02f25 | Gallatin | B-1 | 02 | 00000F25 | N/A | [Specs](https://ark.intel.com/products/codename/1927/Gallatin#@Gallatin)
| Server | m02f26 | Gallatin | C-0 | 02 | 00000F26 | N/A | [Specs](https://ark.intel.com/products/codename/1927/Gallatin#@Gallatin)
| Server | m02f27 | Prestonia | C-1 | 02 | 00000F27 | N/A | [Specs](https://ark.intel.com/products/codename/1838/Prestonia?q=prestonia)
| Server | m02f29 | Prestonia | D-1 | 02 | 00000F29 | N/A | [Specs](https://ark.intel.com/products/codename/1838/Prestonia?q=prestonia)
| Server | m02f41 | Potomac | C-0 | 02 | 00000F41 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/2684/Potomac#@Potomac)
| Server | m02f48 | Paxville MP | A-0 | 02 | 00000F48 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-7000-series-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/6191/Paxville?q=paxville)
| Server | m03106a5 | Nehalem-EP | D-0 | 03 | 000106A5 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-5500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/54499/Nehalem-EP#@Nehalem-EP)
| Server | m03106a5 | Nehalem-WS 1S | D-0 | 03 | 000106A5 | N/A | [Specs](https://ark.intel.com/products/codename/54499/Nehalem-EP#@Nehalem-EP)
| Server | m03206c2 | Westmere-EP | B-1 | 03 | 000206C2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-5600-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/54534/Westmere-EP#@Westmere-EP)
| Server | m03206c2 | Westmere-WS 1S | B-1 | 03 | 000206C2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-3600-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/54534/Westmere-EP#@Westmere-EP)
| Server | m0410676 | Wolfdale-DP | C-0 | 04 | 00010676 | N/A | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale#@server)
| Server | m04206e6 | Nehalem-EX | D-0 | 04 | 000206E6 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-processor-7500-series-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64238/Nehalem-EX#@Nehalem-EX)
| Server | m046f6 | Woodcrest | B-2 | 04 | 000006F6 | N/A | [Specs](https://ark.intel.com/products/codename/22796/Woodcrest#@Woodcrest)
| Server | m046fb | Woodcrest | G-0 | 04 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/22796/Woodcrest#@Woodcrest)
| Server | m05206f2 | Westmere-EX | A-2 | 05 | 000206F2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e7-8800-4800-2800-families-specification-update.html?wapkw=processor+specification+update)  | [Specs](https://ark.intel.com/products/codename/33175/Westmere-EX#@Westmere-EX)
| Server | m08106d1 | Dunnington | A-1 | 08 | 000106D1 | N/A | [Specs](https://ark.intel.com/products/codename/25006/Dunnington?q=dunnington)
| Server | m086fb | Tigerton | G-0 | 08 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/25005/Tigerton#@Tigerton)
| Server | m0880650 | Knights Mill | A-0 | 08 | 00080650 | N/A | [Specs](https://ark.intel.com/products/codename/57723/Knights-Mill?q=knights%20mill)
| Server | m09106e4 | Jasper Forest | B-0 | 09 | 000106E4 | N/A | N/A
| Server | m1010677 | Yorkfield Xeon | C-1 | 10 | 00010677 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@server)
| Server | m1010677 | Yorkfield Xeon | M-1 | 10 | 00010677 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@server)
| Server | m1050662 | Broadwell-DE | V-1 | 10 | 00050662 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-d-1500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m1050663 | Broadwell-DE | V-2 | 10 | 00050663 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-d-1500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m1050663 | Broadwell-DE | V-3 | 10 | 00050663 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-d-1500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m1050664 | Broadwell-DE | Y-0 | 10 | 00050664 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-d-1500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m1050665 | Broadwell-NS | A-0 | 10 | 00050665 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-d-1500-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m106f7 | Kentsfield Xeon | B-3 | 10 | 000006F7 | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield?q=kentsfield#@server)
| Server | m106fb | Kentsfield Xeon | G-0 | 10 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/23489/Kentsfield?q=kentsfield#@server)
| Server | m1220652 | Clarkdale Xeon | C-2 | 12 | 00020652 | N/A | [Specs](https://ark.intel.com/products/codename/29890/Clarkdale?q=clarkdale#@server)
| Server | m12206a7 | Sandy Bridge Xeon E3 | D-2 | 12 | 000206A7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e3-1200-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29900/Sandy-Bridge#@server)
| Server | m12306a9 | Ivy Bridge Xeon E3 | E-1 | 12 | 000306A9 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e3-1200v2-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@server)
| Server | m12306a9 | Ivy Bridge Xeon E3| L-1 | 12 | 000306A9 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e3-1200v2-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@server)
| Server | m13106e5 | Lynnfield Xeon | B-1 | 13 | 000106E5 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-3400-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/29896/Lynnfield?q=lynnfield#@server)
| Server | m1df34 | Nocona | D-0 | 1D | 00000F34 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1789/Nocona#@Nocona)
| Server | m2240671 | Broadwell Xeon E3 | G-0 | 22 | 00040671 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-mobile-5th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | m22906ea | Coffee Lake-S 4+2 Xeon E | U-0 | 22 | 000906EA | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake?q=coffee%20lake#@server)
| Server | m22906ea | Coffee Lake-S 6+2 Xeon E | U-0 | 22 | 000906EA | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake?q=coffee%20lake#@server)
| Server | m22906ec | Coffee Lake-S 8+2 Xeon E | P-0 | 22 | 000906EC | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@server)
| Server | m22906ed | Coffee Lake-S 8+2 Xeon E | P-0 | 22 | 000906ED | N/A | [Specs](https://ark.intel.com/products/codename/97787/Coffee-Lake#@server)
| Server | m22f68 | Tulsa | B-0 | 22 | 00000F68 | N/A | [Specs](https://ark.intel.com/products/codename/3374/Tulsa?q=tulsa)
| Server | m2a906e9 | Kaby Lake Xeon E3 | B-0 | 2A | 000906E9 | [Update](https://www.intel.com/content/www/us/en/processors/core/7th-gen-core-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/82879/Kaby-Lake#@server)
| Server | m32306c3 | Haswell Xeon E3 | C-0 | 32 | 000306C3 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e3-1200v3-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@server)
| Server | m36506e3 | Skylake Xeon E3 | R-0 | 36 | 000506E3 | [Update](https://www.intel.com/content/www/us/en/processors/core/desktop-6th-gen-core-family-spec-update.html) | [Specs](https://ark.intel.com/products/codename/37572/Skylake?q=skylake#@server)
| Server | m4010676 | Harpertown | C-0 | 40 | 00010676 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-5400-spec-update.html?wapkw=processor+specification+update)  | [Specs](https://ark.intel.com/products/codename/26555/Harpertown#@Harpertown)
| Server | m406f7 | Clovertown | B-3 | 40 | 000006F7 | N/A | [Specs](https://ark.intel.com/products/codename/23349/Clovertown#@Clovertown)
| Server | m406fb | Clovertown | G-0 | 40 | 000006FB | N/A | [Specs](https://ark.intel.com/products/codename/23349/Clovertown#@Clovertown)
| Server | m441067a | Harpertown | E-0 | 44 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/26555/Harpertown#@Harpertown)
| Server | m441067a | Wolfdale-DP | E-0 | 44 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale#@server)
| Server | m5df4a | Irwindale | R-0 | 5D | 00000F4A | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/5960/Irwindale?q=irwindale)
| Server | m6d206d6 | Sandy Bridge-EP | C-1 | 6D | 000206D6 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64276/Sandy-Bridge-EP#@Sandy-Bridge-EP)
| Server | m6d206d7 | Sandy Bridge-EN | C-2 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64275/Sandy-Bridge-EN#@Sandy-Bridge-EN)
| Server | m6d206d7 | Sandy Bridge-EN | M-1 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64275/Sandy-Bridge-EN#@Sandy-Bridge-EN)
| Server | m6d206d7 | Sandy Bridge-EP | C-2 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64276/Sandy-Bridge-EP#@Sandy-Bridge-EP)
| Server | m6d206d7 | Sandy Bridge-EP | M-1 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64276/Sandy-Bridge-EP#@Sandy-Bridge-EP)
| Server | m6d206d7 | Sandy Bridge-EP 4S | M-1 | 6D | 000206D7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/64276/Sandy-Bridge-EP#@Sandy-Bridge-EP)
| Server | m6f306f2 | Haswell-EP | C-0 | 6F | 000306F2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v3-spec-update.html?wapkw=processor+spec+update+e5) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@server)
| Server | m6f306f2 | Haswell-EP | C-1 | 6F | 000306F2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v3-spec-update.html?wapkw=processor+spec+update+e5) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@server)
| Server | m6f306f2 | Haswell-EP | M-1 | 6F | 000306F2 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v3-spec-update.html?wapkw=processor+spec+update+e5) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@server)
| Server | m7850671 | Knights Landing | B-0 | 78 | 00050671 |[Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-phi-processor-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/family/75557/Intel-Xeon-Phi-Processors#@Intel-Xeon-Phi-Processors)
| Server | m80306f4 | Haswell-EX | E-0 | 80 | 000306F4 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e7-v3-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/42174/Haswell#@server)
| Server | m9110676 | Wolfdale Xeon | C-0 | 91 | 00010676 | N/A | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale?q=wolfdale#@server)
| Server | m9110676 | Yorkfield Xeon | C-0  | 91 | 00010676 | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@server)
| Server | m9750653 | Skylake Server | B-1 | 97 | 00050653 | N/A | N/A
| Server | m97606a0 | Ice Lake Server | A-0 | 97 | 000606A0 | N/A | N/A
| Server | m9df43 | Irwindale | N-0 | 9D | 00000F43 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/5960/Irwindale?q=irwindale)
| Server | mb11067a | Wolfdale Xeon | E-0 | B1 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/24736/Wolfdale?q=wolfdale#@server)
| Server | mb11067a | Yorkfield Xeon | E-0 | B1 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@server)
| Server | mb11067a | Yorkfield Xeon | R-0 | B1 | 0001067A | N/A | [Specs](https://ark.intel.com/products/codename/26553/Yorkfield#@server)
| Server | mb750654 | Skylake Server | H-0 | B7 | 00050654 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/scalable/xeon-scalable-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/37572/Skylake?q=skylake#@server)
| Server | mb750654 | Skylake Server | M-0 | B7 | 00050654 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/scalable/xeon-scalable-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/37572/Skylake?q=skylake#@server)
| Server | mb750654 | Skylake Server | U-0 | B7 | 00050654 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/scalable/xeon-scalable-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/37572/Skylake?q=skylake#@server)
| Server | mb750654 | Skylake-D | M-1 | B7 | 00050654 | N/A | [Specs](https://ark.intel.com/products/codename/37572/Skylake?q=skylake#@server)
| Server | mbdf41 | Cranford | A-0 | BD | 00000F41 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/5956/Cranford?q=cranford)
| Server | mbdf41 | Nocona | E-0 | BD | 00000F41 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1789/Nocona#@Nocona)
| Server | mbdf49 | Cranford | B-0 | BD | 00000F49 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/5956/Cranford?q=cranford)
| Server | mbdf49 | Nocona | G-1 | BD | 00000F49 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-with-800-mhz-system-bus-specification-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/1789/Nocona#@Nocona)
| Server | mbf50655 | Cascade Lake | A-0  | BF | 00050655 | N/A | N/A
| Server | mbf50656 | Cascade Lake | B-0  | BF | 00050656 | N/A | N/A
| Server | mbf50657 | Cascade Lake | B-1  | BF | 00050657 | N/A | N/A
| Server | mbf5065a | Cooper Lake | A-0  | BF | 0005065a | N/A | N/A
| Server | med306e4 | Ivy Bridge-EN | M-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/67492/Ivy-Bridge-EN#@Ivy-Bridge-EN)
| Server | med306e4 | Ivy Bridge-EN | S-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/67492/Ivy-Bridge-EN#@Ivy-Bridge-EN)
| Server | med306e4 | Ivy Bridge-EP | C-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/68926/Ivy-Bridge-EP#@Ivy-Bridge-EP)
| Server | med306e4 | Ivy Bridge-EP | M-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/68926/Ivy-Bridge-EP#@Ivy-Bridge-EP)
| Server | med306e4 | Ivy Bridge-EP | S-1 | ED | 000306E4 | N/A | [Specs](https://ark.intel.com/products/codename/68926/Ivy-Bridge-EP#@Ivy-Bridge-EP)
| Server | med306e7 | Ivy Bridge-EX | D-1 | ED | 000306E7 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e7-v2-spec-update.html) | [Specs](https://ark.intel.com/products/codename/29902/Ivy-Bridge#@server)
| Server | mef406f1 | Broadwell-EP | B-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v4-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | mef406f1 | Broadwell-EP | M-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v4-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | mef406f1 | Broadwell-EP | R-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v4-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | mef406f1 | Broadwell-EP 4S | B-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e5-v4-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | mef406f1 | Broadwell-EX | B-0 | EF | 000406F1 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-e7-v4-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/38530/Broadwell#@server)
| Server | mu1632 | Deschutes | B-0 | 1 | 00001632 | [Update](https://downloadcenter.intel.com/download/24360/Archived-documents-for-Intel-Pentium-II-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Server | mu16b1 | Tualatin (FC-PGA2) | A-1 | 1 | 000006B1 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@server)
| Server | mu16b4 | Tualatin (FC-PGA2) | B-1 | 1 | 000006B4 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1991/Tualatin#@server)
| Server | mu2652 | Deschutes | B-0 | 2 | 00000652 | [Update](https://downloadcenter.intel.com/download/24360/Archived-documents-for-Intel-Pentium-II-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Server | mu2653 | Deschutes | B-1 | 2 | 00000653 | [Update](https://downloadcenter.intel.com/download/24360/Archived-documents-for-Intel-Pentium-II-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/series/78132/Legacy-Intel-Pentium-Processor)
| Server | mu2671 | Katmai (SECC2) | B-0 | 2 | 00000671 | [Update](https://downloadcenter.intel.com/download/24363/Archived-documents-for-Intel-Pentium-III-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1938/Katmai#@Katmai)
| Server | mu2672 | Tanner | B-0 | 2 | 00000672 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1983/Tanner#@Tanner)
| Server | mu2673 | Tanner | C-0 | 2 | 00000673 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1983/Tanner#@Tanner)
| Server | mu2681 | Cascades | A-2 | 2 | 00000681 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| Server | mu2683 | Cascades | B-0 | 2 | 00000683 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| Server | mu2686 | Cascades | C-0 | 2 | 00000686 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| Server | mu26a0 | Cascades | A-0 | 2 | 000006A0 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| Server | mu26a1 | Cascades | A-1 | 2 | 000006A1 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| Server | mu26a4 | Cascades | B-0 | 2 | 000006A4 | [Update](https://downloadcenter.intel.com/download/24362/Archived-documents-for-Intel-Pentium-III-Xeon-Processor?product=595) | [Specs](https://ark.intel.com/products/codename/1896/Cascades#@Cascades)
| SOC | m0130673 | Baytrail | B-2 | 01 | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m0130673 | Baytrail | B-3 | 01 | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m01406a8 | Tangier | B-0 | 01 | 000406A8 | N/A | [Specs](https://ark.intel.com/products/codename/41559/Merrifield)
| SOC | m01406a8 | Tangier | C-0 | 01 | 000406A8 | N/A | [Specs](https://ark.intel.com/products/codename/41559/Merrifield)
| SOC | m01406c3 | Cherryview | C-0 | 01 | 000406C3 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/46629/Cherry-Trail#@Cherry-Trail)
| SOC | m01406c4 | Cherryview | D-0 | 01 | 000406C4 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/46629/Cherry-Trail#@Cherry-Trail)
| SOC | m01406c4 | Cherryview | D-1 | 01 | 000406C4 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/46629/Cherry-Trail#@Cherry-Trail)
| SOC | m01506a0 | Anniedale | A-0 | 01 | 000506A0 | N/A | [Specs](https://ark.intel.com/products/codename/71167/Moorefield#@Moorefield)
| SOC | m01506a0 | Anniedale | B-0 | 01 | 000506A0 | N/A | [Specs](https://ark.intel.com/products/codename/71167/Moorefield#@Moorefield)
| SOC | m01506c2 | Broxton | C-0 | 01 | 000506C2 | N/A | N/A
| SOC | m01506f1 | Denverton | B-0 | 01 | 000506F1 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-c3000-family-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/63508/Denverton?q=Denverton)
| SOC | m01606e1 | Cougar Mountain | B-0 | 01 | 000606E1 | N/A | [Specs](https://ark.intel.com/products/codename/80750/Cougar-Mountain#@Cougar-Mountain)
| SOC | m01606e1 | Cougar Mountain | C-0 | 01 | 000606E1 | N/A | [Specs](https://ark.intel.com/products/codename/63508/Denverton?q=Denverton)
| SOC | m01706a1 | Gemini Lake | B-0 | 01 | 000706A1 | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/pentium/silver-celeron-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/83915/Gemini-Lake#@Gemini-Lake)
| SOC | m01706a8 | Gemini Lake | R-0 | 01 | 000706A8 | [Update](https://www.intel.com/content/www/us/en/products/docs/processors/pentium/silver-celeron-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/83915/Gemini-Lake#@Gemini-Lake)
| SOC | m\_01\_80660\_80661 | Snow Ridge | A-0 | 01 | 00080660 | N/A | N/A
| SOC | m\_01\_80660\_80661 | Snow Ridge | A-1 | 01 | 00080661 | N/A | N/A
| SOC | m\_01\_806a0 | Lakefield | A-0 | 01 | 000806a0 | N/A | N/A
| SOC | m\_01\_806a0 | Lakefield | A-1 | 01 | 000806a0 | N/A | N/A
| SOC | m0120661 | Lincroft | B-0 | 01 | 00020661 | N/A | [Link](https://ark.intel.com/products/codename/29967/Lincroft?q=lincroft)
| SOC | m0220661 | Tunnel Creek | B-1 | 02 | 00020661 | N/A | [Link](https://ark.intel.com/products/codename/37567/Tunnel-Creek#@Tunnel-Creek)
| SOC | m0230673 | Baytrail | B-2 | 02 | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m0230673 | Baytrail | B-3 | 02 | 00030673 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m0230678 | Baytrail | C-0 | 02 | 00030678 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m02506d1 | SoFIA 3G ES2.1 | E-S | 02 | 000506D1 | N/A | [Specs](https://ark.intel.com/products/codename/84260/SoFIA-3G-R#@SoFIA-3G-R)
| SOC | m03506c9 | Apollo Lake | B-0 | 03 | 000506C9 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-j-series-datasheet-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m03506c9 | Apollo Lake | B-1 | 03 | 000506C9 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-j-series-datasheet-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m03506c9 | Apollo Lake | B-2 | 03 | 000506C9 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-j-series-datasheet-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m03506c9 | Apollo Lake | D-0 | 03 | 000506C9 | [Update](https://www.intel.com/content/www/us/en/processors/pentium/pentium-celeron-n-series-j-series-datasheet-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m03506ca | Apollo Lake | E-0 | 03 | 000506CA | N/A | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m03506ca | Apollo Lake | F-1 | 03 | 000506CA | N/A | [Specs](https://ark.intel.com/products/codename/80644/Apollo-Lake?q=apollo%20lake)
| SOC | m04506d1 | SoFIA 3G Granite | E-S | 04 | 000506D1 | N/A | [Specs](https://ark.intel.com/products/codename/84260/SoFIA-3G-R#@SoFIA-3G-R)
| SOC | m0f30679 | Baytrail | D-0 | 0F | 00030679 | [Update](https://www.intel.com/content/www/us/en/processors/atom/atom-z36xxx-z37xxx-spec-update.html?wapkw=processor+specification+update) | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m0f30679 | Baytrail | D-1 | 0F | 00030679 | [Update](https://www.intel.com/content/www/us/en/processors/xeon/xeon-7000-series-specification-update.html?wapkw=processor+specification+update)  | [Specs](https://ark.intel.com/products/codename/55844/Bay-Trail?q=bay%20trail)
| SOC | m\_10\_806a1 | Lakefield | B-2 | 10 | 000806a1 | N/A | N/A