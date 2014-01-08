"""
Copyright (c) 2013-2014, Jurriaan Bremer
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the darm developer(s) nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from tablegen import Instruction, Table, Node, Immediate, ScatteredField
from tablegen import ScatteredImmediate, Macro, AssignMacro
from tablegen import DoubleRegister, Register, ScatteredRegister, FieldPlus
from tablegen import DoubleScatteredRegister, Field, BranchNotXorImmediate


class ThumbTable(Table):
    def _init(self):
        self.thumb = Node()
        self.thumb2 = Node()
        return self.thumb, self.thumb2

    def _insert(self, ins):
        if ins.bitsize(len(ins.bits)) == 16:
            self.thumb.insert(ins)
        elif ins.bitsize(len(ins.bits)) == 32:
            self.thumb2.insert(ins)
        else:
            raise

    def _process(self):
        self.thumb.process()
        self.thumb2.process()

    def _create(self, sm, lut, fmt, bitsize):
        off = sm.alloc(4)
        off2 = lut.alloc(32)

        sm.update(off, 'SM_TBL5', bitsize-5, 'L(%d)' % off2, 'H(%d)' % off2)

        thumb = self.thumb.create(sm, lut, fmt, bitsize)
        thumb2 = self.thumb2.create(sm, lut, fmt, bitsize)

        is_thumb2 = lambda _: _ in (0b11101, 0b11110, 0b11111)
        tbl = [thumb2 if is_thumb2(_) else thumb for _ in xrange(32)]
        lut.update(off2, *tbl)


Rd = Register(4, 'Rd')
Rd3 = Register(3, 'Rd')
Rn = Register(4, 'Rn')
Rn3 = Register(3, 'Rn')
Rm = Register(4, 'Rm')
Rm3 = Register(3, 'Rm')
Ra = Register(4, 'Ra')
Rt = Register(4, 'Rt')
Rt3 = Register(3, 'Rt')
Rt2 = Register(4, 'Rt2')
RdHi = Register(4, 'RdHi')
RdLo = Register(4, 'RdLo')
Rdn3 = DoubleRegister(3, 'Rd', 'Rn')
Rdn1_3 = DoubleScatteredRegister(1, 'Rd', 'Rn', 3)
Rdm3 = DoubleRegister(3, 'Rd', 'Rm')
Rdm1_3 = DoubleScatteredRegister(1, 'Rd', 'Rm', 3)
Rd1_3 = ScatteredRegister(1, 'Rd', 3)
Rn1_3 = ScatteredRegister(1, 'Rn', 3)

typ = Field(2, 'shift_type')
cond = Field(4, 'cond')
S = Field(1, 'S')
W = Field(1, 'W')
P = Field(1, 'P')
U = Field(1, 'U')
sh = ScatteredField(1, 'shift_type', 1)

msb = Field(5, 'msb')
option = Field(4, 'option')
register_list = Field(16, 'register_list')
register_list8 = Field(8, 'register_list')
register_list13 = Field(13, 'register_list')
register_list1_14 = ScatteredField(1, 'register_list', 14)
register_list1_15 = ScatteredField(1, 'register_list', 15)
widthm1 = FieldPlus(5, 'width', 1)
E = Field(1, 'E')

firstcond = Field(4, 'first_cond')
it_mask = Field(4, 'it_mask')

msr_mask = Field(2, 'msr_mask')

imm1_6 = ScatteredImmediate(1, 'imm1', 6)
imm1_11 = ScatteredImmediate(1, 'imm1', 11)
imm1_18 = ScatteredImmediate(1, 'imm1', 18)
imm1_19 = ScatteredImmediate(1, 'imm1', 19)
imm1_22_bnxor = BranchNotXorImmediate(1, 'imm1', 22)
imm1_23_bnxor = BranchNotXorImmediate(1, 'imm1', 23)
imm1_20 = ScatteredImmediate(1, 'imm1', 20)
imm1_24 = ScatteredImmediate(1, 'imm1', 24)
imm2 = Immediate(2, 'imm2')
imm3 = Immediate(3, 'imm3')
imm3_2 = ScatteredImmediate(3, 'imm3', 2)
imm3_8 = ScatteredImmediate(3, 'imm3', 8)
imm4_12 = ScatteredImmediate(4, 'imm4', 12)
imm5 = Immediate(5, 'imm5')
imm5_1 = ScatteredImmediate(5, 'imm5', 1)
imm5_2 = ScatteredImmediate(5, 'imm5', 2)
imm6_12 = ScatteredImmediate(6, 'imm6', 12)
imm7 = Immediate(7, 'imm7')
imm7_2 = ScatteredImmediate(7, 'imm7', 2)
imm8 = Immediate(8, 'imm8')
imm8_1 = ScatteredImmediate(8, 'imm8', 1)
imm8_2 = ScatteredImmediate(8, 'imm8', 2)
imm10_2 = ScatteredImmediate(10, 'imm10', 2)
imm10_12 = ScatteredImmediate(10, 'imm10', 12)
imm11 = Immediate(11, 'imm11')
imm11_1 = ScatteredImmediate(11, 'imm11', 1)
imm12 = Immediate(12, 'imm12')

sat_imm5 = Field(5, 'sat_imm')
sat_imm4 = Field(4, 'sat_imm')
rotate = Field(2, 'rotate')

ThumbExpandImm = Macro('ThumbExpandImm')
SignExtend = Macro('SIGN')
RtReglist = Macro('RtReglist')
Assign = AssignMacro('Assign')
AssignS_IT = Assign(S='B_IT')

_table = [
    Instruction('ADC{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 0, 1, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('ADC{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 1, 0, 1, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('ADC{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('ADD{S}<c> <Rd3>, <Rn3>, #<imm3>', (0, 0, 0, 1, 1, 1, 0, imm3, Rn3, Rd3), macro=AssignS_IT),
    Instruction('ADD{S}<c> <Rdn3>, #<imm8>', (0, 0, 1, 1, 0, Rdn3, imm8), macro=AssignS_IT),
    Instruction('ADD{S}<c>.W <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 0, 0, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('ADDW<c> <Rd>, <Rn>, #<imm12>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 0, 0, 0, 0, Rn, 0, imm3_8, Rd, imm8)),
    Instruction('ADD{S}<c> <Rd>, <Rn>, <Rm>', (0, 0, 0, 1, 1, 0, 0, Rm3, Rn3, Rd3), macro=AssignS_IT),
    Instruction('ADD<c> <Rdn>, <Rm>', (0, 1, 0, 0, 0, 1, 0, 0, Rdn1_3, Rm, Rdn3)),
    Instruction('ADD{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('ADD<c> <Rd3>, <Rn=SP>, #<imm>', (1, 0, 1, 0, 1, Rd3, imm8_2), macro=Assign(Rn='SP')),
    Instruction('ADD<c> <Rdn=SP>, #<imm>', (1, 0, 1, 1, 0, 0, 0, 0, 0, imm7_2), macro=Assign(Rd='SP', Rn='SP')),
    # Instruction('ADD{S}<c>.W <Rd>, <Rn=SP>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 0, 0, 0, S, 1, 1, 0, 1, 0, imm3_8, Rd, imm8), macros=[ThumbExpandImm, Assign(Rn='SP')]),
    Instruction('ADDW<c> <Rd>, <Rn=SP>, #<imm12>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, imm3_8, Rd, imm8), macro=Assign(Rn='SP')),
    Instruction('ADD<c> <Rdm>, <Rn=SP>, <Rdm>', (0, 1, 0, 0, 0, 1, 0, 0, Rdm1_3, 1, 1, 0, 1, Rdm3), macro=Assign(Rn='SP')),
    # Instruction('ADD<c> <Rdn=SP>, <Rm>', (0, 1, 0, 0, 0, 1, 0, 0, 1, Rm, 1, 0, 1), macro=Assign(Rd='SP', Rn='SP')),
    # Instruction('ADD{S}<c>.W <Rd>, <Rn=SP>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, S, 1, 1, 0, 1, (0), imm3, Rd, imm2, typ, Rm), macro=Assign(Rn='SP')),
    Instruction('ADR<c> <Rd3>, <label>', (1, 0, 1, 0, 0, Rd3, imm8_2), macro=Assign(U=True, Rn='PC')),
    Instruction('ADR<c>.W <Rd>, <label>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, imm3_8, Rd, imm8), macro=Assign(U=False, Rn='PC')),
    Instruction('ADR<c>.W <Rd>, <label>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, imm3_8, Rd, imm8), macro=Assign(U=True, Rn='PC')),
    Instruction('AND{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 0, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('AND{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('AND{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('ASR{S}<c> <Rd3>, <Rm3>, #<imm>', (0, 0, 0, 1, 0, imm5, Rm3, Rd3), macro=AssignS_IT),
    Instruction('ASR{S}<c>.W <Rd>, <Rm>, #<imm>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3_2, Rd, imm2, 1, 0, Rm)),
    Instruction('ASR{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 1, 0, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('ASR{S}<c>.W <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('B<c> <label>', (1, 1, 0, 1, cond, imm8_1), macros=[SignExtend(9), Assign(Rn='PC')]),
    Instruction('B<c> <label>', (1, 1, 1, 0, 0, imm11_1), macros=[SignExtend(12), Assign(Rn='PC')]),
    Instruction('B<c>.W <label>', (1, 1, 1, 1, 0, imm1_20, cond, imm6_12, 1, 0, imm1_18, 0, imm1_19, imm11_1), macros=[SignExtend(21), Assign(Rn='PC')]),
    Instruction('B<c>.W <label>', (1, 1, 1, 1, 0, imm1_24, imm10_12, 1, 0, imm1_23_bnxor, 1, imm1_22_bnxor, imm11_1), macros=[SignExtend(25), Assign(Rn='PC')]),
    Instruction('BFC<c> <Rd>, #<lsb>, #<width>', (1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, imm3_2, Rd, imm2, (0), msb)),
    Instruction('BFI<c> <Rd>, <Rn>, #<lsb>, #<width>', (1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 1, 0, Rn, 0, imm3_2, Rd, imm2, (0), msb)),
    Instruction('BIC{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 0, 1, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('BIC{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 1, 1, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('BIC{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('BKPT #<imm8>', (1, 0, 1, 1, 1, 1, 1, 0, imm8)),
    Instruction('BL<c> <label>', (1, 1, 1, 1, 0, imm1_24, imm10_12, 1, 1, imm1_23_bnxor, 1, imm1_22_bnxor, imm11_1), macros=[SignExtend(25), Assign(Rn='PC')]),
    Instruction('BLX<c> <label>', (1, 1, 1, 1, 0, imm1_24, imm10_12, 1, 1, imm1_23_bnxor, 0, imm1_22_bnxor, imm10_2, 0), macros=[SignExtend(25), Assign(Rn='PC')]),
    Instruction('BLX<c> <Rm>', (0, 1, 0, 0, 0, 1, 1, 1, 1, Rm, (0), (0), (0))),
    Instruction('BX<c> <Rm>', (0, 1, 0, 0, 0, 1, 1, 1, 0, Rm, (0), (0), (0))),
    Instruction('BXJ<c> <Rm>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, Rm, 1, 0, (0), 0, (1), (1), (1), (1), (0), (0), (0), (0), (0), (0), (0), (0))),
    Instruction('CBZ <Rm>, <label>', (1, 0, 1, 1, 0, 0, imm1_6, 1, imm5_1, Rm3), macro=Assign(U=True, Rn='PC')),
    Instruction('CBNZ <Rm>, <label>', (1, 0, 1, 1, 1, 0, imm1_6, 1, imm5_1, Rm3), macro=Assign(U=True, Rn='PC')),
    Instruction('CLREX<c>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 0, 1, 0, (1), (1), (1), (1))),
    Instruction('CLZ<c> <Rd>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm)),
    Instruction('CMN<c> <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 0, 0, 0, 1, Rn, 0, imm3_8, 1, 1, 1, 1, imm8), macro=ThumbExpandImm),
    Instruction('CMN<c> <Rn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 0, 1, 1, Rm3, Rn3)),
    Instruction('CMN<c>.W <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, Rn, (0), imm3_2, 1, 1, 1, 1, imm2, typ, Rm)),
    Instruction('CMP<c> <Rn3>, #<imm8>', (0, 0, 1, 0, 1, Rn3, imm8)),
    Instruction('CMP<c>.W <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 1, 0, 1, 1, Rn, 0, imm3_8, 1, 1, 1, 1, imm8), macro=ThumbExpandImm),
    Instruction('CMP<c> <Rn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 0, 1, 0, Rm3, Rn3)),
    Instruction('CMP<c> <Rn>, <Rm>', (0, 1, 0, 0, 0, 1, 0, 1, Rn1_3, Rm, Rn3)),
    Instruction('CMP<c>.W <Rn>, <Rm> , <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, Rn, (0), imm3_2, 1, 1, 1, 1, imm2, typ, Rm)),
    Instruction('DBG<c> #<option>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 1, 1, 1, 1, option)),
    Instruction('DMB<c> #<option>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 0, 1, option)),
    Instruction('DSB<c> #<option>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 0, 0, option)),
    Instruction('EOR{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 1, 0, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('EOR{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 0, 0, 1, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('EOR{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('ISB<c> #<option>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, (1), (1), (1), (1), 1, 0, (0), 0, (1), (1), (1), (1), 0, 1, 1, 0, option)),
    Instruction('IT{<x>{<y>{<z>}}} <firstcond>', (1, 0, 1, 1, 1, 1, 1, 1, firstcond, it_mask)),
    Instruction('LDM<c> <Rn>{!}, <registers>', (1, 1, 0, 0, 1, Rn3, register_list8)),
    Instruction('LDM<c>.W <Rn>{!}, <registers>', (1, 1, 1, 0, 1, 0, 0, 0, 1, 0, W, 1, Rn, register_list)),
    Instruction('LDMDB<c> <Rn>{!}, <registers>', (1, 1, 1, 0, 1, 0, 0, 1, 0, 0, W, 1, Rn, register_list)),
    Instruction('LDR<c> <Rt3>, [<Rn3>{, #<imm>}]', (0, 1, 1, 0, 1, imm5, Rn3, Rt3)),
    Instruction('LDR<c> <Rt3>, [SP{, #<imm>}]', (1, 0, 0, 1, 1, Rt3, imm8)),
    Instruction('LDR<c>.W <Rt>, [<Rn>{, #<imm12>}]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, imm12)),
    Instruction('LDR<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 1, P, U, W, imm8)),
    Instruction('LDR<c> <Rt3>, <label>', (0, 1, 0, 0, 1, Rt3, imm8)),
    Instruction('LDR<c>.W <Rt>, <label>', (1, 1, 1, 1, 1, 0, 0, 0, U, 1, 0, 1, 1, 1, 1, 1, Rt, imm12)),
    Instruction('LDR<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 1, 0, 0, Rm3, Rn3, Rt3)),
    Instruction('LDR<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('LDRB<c> <Rt3>, [<Rn3>{, #<imm5>}]', (0, 1, 1, 1, 1, imm5, Rn3, Rt3)),
    Instruction('LDRB<c>.W <Rt>, [<Rn>{, #<imm12>}]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, Rn, Rt, imm12)),
    Instruction('LDRB<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 1, P, U, W, imm8)),
    # Instruction('LDRB<c> <Rt>, <label>', (1, 1, 1, 1, 1, 0, 0, 0, U, 0, 0, 1, 1, 1, 1, 1, Rt, imm12)),
    Instruction('LDRB<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 1, 1, 0, Rm3, Rn3, Rt3)),
    Instruction('LDRB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('LDRBT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('LDRD<c> <Rt>, <Rt2>, [<Rn>{, #+/-<imm>}]', (1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 1, Rn, Rt, Rt2, imm8)),
    # Instruction('LDRD<c> <Rt>, <Rt2>, <label>', (1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 1, 1, 1, 1, 1, Rt, Rt2, imm8)),
    Instruction('LDREX<c> <Rt>, [<Rn>{, #<imm>}]', (1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), imm8)),
    Instruction('LDREXB<c> <Rt>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 0, (1), (1), (1), (1))),
    Instruction('LDREXD<c> <Rt>, <Rt2>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, Rt2, 0, 1, 1, 1, (1), (1), (1), (1))),
    Instruction('LDREXH<c> <Rt>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 1, (1), (1), (1), (1))),
    Instruction('LDRH<c> <Rt3>, [<Rn3>{, #<imm>}]', (1, 0, 0, 0, 1, imm5, Rn3, Rt3)),
    Instruction('LDRH<c>.W <Rt>, [<Rn>{, #<imm12>}]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, Rn, Rt, imm12)),
    Instruction('LDRH<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 1, P, U, W, imm8)),
    # Instruction('LDRH<c> <Rt>, <label>', (1, 1, 1, 1, 1, 0, 0, 0, U, 0, 1, 1, 1, 1, 1, 1, Rt, imm12)),
    Instruction('LDRH<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 1, 0, 1, Rm3, Rn3, Rt3)),
    Instruction('LDRH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('LDRHT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('LDRSB<c> <Rt>, [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, Rn, Rt, imm12)),
    Instruction('LDRSB<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 1, P, U, W, imm8)),
    # Instruction('LDRSB<c> <Rt>, <label>', (1, 1, 1, 1, 1, 0, 0, 1, U, 0, 0, 1, 1, 1, 1, 1, Rt, imm12)),
    Instruction('LDRSB<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 0, 1, 1, Rm3, Rn3, Rt3)),
    Instruction('LDRSB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('LDRSBT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('LDRSH<c> <Rt>, [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, Rn, Rt, imm12)),
    Instruction('LDRSH<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 1, P, U, W, imm8)),
    # Instruction('LDRSH<c> <Rt>, <label>', (1, 1, 1, 1, 1, 0, 0, 1, U, 0, 1, 1, 1, 1, 1, 1, Rt, imm12)),
    Instruction('LDRSH<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 1, 1, 1, Rm3, Rn3, Rt3)),
    Instruction('LDRSH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('LDRSHT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('LDRT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('LSL{S}<c> <Rd3>, <Rm3>, #<imm5>', (0, 0, 0, 0, 0, imm5, Rm3, Rd3), macro=AssignS_IT),
    Instruction('LSL{S}<c>.W <Rd>, <Rm>, #<imm5>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3_2, Rd, imm2, 0, 0, Rm)),
    Instruction('LSL{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 0, 1, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('LSL{S}<c>.W <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('LSR{S}<c> <Rd3>, <Rm3>, #<imm>', (0, 0, 0, 0, 1, imm5, Rm3, Rd3), macro=AssignS_IT),
    Instruction('LSR{S}<c>.W <Rd>, <Rm>, #<imm>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3_2, Rd, imm2, 0, 1, Rm)),
    Instruction('LSR{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 0, 1, 1, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('LSR{S}<c>.W <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('MLA<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('MLS<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('MOV{S}<c> <Rd3>, #<imm8>', (0, 0, 1, 0, 0, Rd3, imm8), macro=AssignS_IT),
    Instruction('MOV{S}<c>.W <Rd>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 1, 0, S, 1, 1, 1, 1, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('MOVW<c> <Rd>, #<imm16>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 0, 1, 0, 0, imm4_12, 0, imm3_8, Rd, imm8)),
    Instruction('MOV<c> <Rd>, <Rm>', (0, 1, 0, 0, 0, 1, 1, 0, Rd1_3, Rm, Rd3)),
    Instruction('MOV{S} <Rd3>, <Rm3>', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Rm3, Rd3), macro=AssignS_IT),
    Instruction('MOV{S}<c>.W <Rd>, <Rm>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), 0, 0, 0, Rd, 0, 0, 0, 0, Rm)),
    Instruction('MOVT<c> <Rd>, #<imm16>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 1, 1, 0, 0, imm4_12, 0, imm3_8, Rd, imm8)),
    Instruction('MRS<c> <Rd>, <spec_reg>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, Rd, (0), (0), 0, (0), (0), (0), (0), (0))),
    Instruction('MSR<c> <spec_reg>, <Rn>', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, Rn, 1, 0, (0), 0, msr_mask, 0, 0, (0), (0), 0, (0), (0), (0), (0), (0))),
    Instruction('MUL{S}<c> <Rdm3>, <Rn3>, <Rdm3>', (0, 1, 0, 0, 0, 0, 1, 1, 0, 1, Rn3, Rdm3), macro=AssignS_IT),
    Instruction('MUL<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('MVN{S}<c> <Rd>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 1, 1, S, 1, 1, 1, 1, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('MVN{S}<c> <Rd3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 1, 1, 1, Rm3, Rd3), macro=AssignS_IT),
    Instruction('MVN{S}<c>.W <Rd>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, S, 1, 1, 1, 1, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('NOP<c>', (1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)),
    Instruction('NOP<c>.W', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    Instruction('ORN{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 1, 1, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('ORN{S}<c> <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('ORR{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 1, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('ORR{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 1, 0, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('ORR{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('PKHBT<c> <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, Rn, (0), imm3_2, Rd, imm2, 0, 0, Rm)),
    Instruction('PKHTB<c> <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, Rn, (0), imm3_2, Rd, imm2, 1, 0, Rm), macro=Assign(shift_type='S_ASR')),
    Instruction('PLD<c> [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, imm12)),
    Instruction('PLDW<c> [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, Rn, 1, 1, 1, 1, imm12)),
    Instruction('PLD<c> [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 1, 1, 0, 0, imm8)),
    Instruction('PLDW<c> [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, 1, 1, 1, 1, 1, 1, 0, 0, imm8)),
    Instruction('PLD<c> <label>', (1, 1, 1, 1, 1, 0, 0, 0, U, 0, (0), 1, 1, 1, 1, 1, 1, 1, 1, 1, imm12)),
    Instruction('PLD<c> [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('PLDW<c> [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, Rn, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('PLI<c> [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, Rn, 1, 1, 1, 1, imm12)),
    Instruction('PLI<c> [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 1, 1, 0, 0, imm8)),
    Instruction('PLI<c> <label>', (1, 1, 1, 1, 1, 0, 0, 1, U, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, imm12)),
    Instruction('PLI<c> [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('POP<c> <registers>', (1, 0, 1, 1, 1, 1, 0, register_list1_15, register_list8)),
    Instruction('POP<c>.W <registers>', (1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, register_list)),
    Instruction('POP<c>.W <registers>', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, Rt, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0), macro=RtReglist),
    Instruction('PUSH<c> <registers>', (1, 0, 1, 1, 0, 1, 0, register_list1_14, register_list8)),
    Instruction('PUSH<c>.W <registers>', (1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, register_list)),
    Instruction('PUSH<c>.W <registers>', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, Rt, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0), macro=RtReglist),
    Instruction('QADD<c> <Rd>, <Rm>, <Rn>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm)),
    Instruction('QADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('QADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('QASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('QDADD<c> <Rd>, <Rm>, <Rn>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 1, Rm)),
    Instruction('QDSUB<c> <Rd>, <Rm>, <Rn>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 1, 1, Rm)),
    Instruction('QSAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('QSUB<c> <Rd>, <Rm>, <Rn>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 1, 0, Rm)),
    Instruction('QSUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('QSUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('RBIT<c> <Rd>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 1, 0, Rm)),
    Instruction('REV<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 1, 0, 1, 0, 0, 0, Rm3, Rd3)),
    Instruction('REV<c>.W <Rd>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm)),
    Instruction('REV16<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 1, 0, 1, 0, 0, 1, Rm3, Rd3)),
    Instruction('REV16<c>.W <Rd>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 0, 1, Rm)),
    Instruction('REVSH<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 1, 0, 1, 0, 1, 1, Rm3, Rd3)),
    Instruction('REVSH<c>.W <Rd>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rm, 1, 1, 1, 1, Rd, 1, 0, 1, 1, Rm)),
    Instruction('ROR{S}<c> <Rd>, <Rm>, #<imm>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), imm3_2, Rd, imm2, 1, 1, Rm)),
    Instruction('ROR{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 1, 1, 1, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('ROR{S}<c>.W <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, S, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('RRX{S}<c> <Rd>, <Rm>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, S, 1, 1, 1, 1, (0), 0, 0, 0, Rd, 0, 0, 1, 1, Rm)),
    Instruction('RSB{S} <Rd3>, <Rn3>, #0', (0, 1, 0, 0, 0, 0, 1, 0, 0, 1, Rn3, Rd3), macro=AssignS_IT),
    Instruction('RSB{S}<c>.W <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 1, 1, 0, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('RSB{S}<c> <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('SADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SBC{S}<c> <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 0, 1, 1, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('SBC{S}<c> <Rdn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 0, 1, 1, 0, Rm3, Rdn3), macro=AssignS_IT),
    Instruction('SBC{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('SBFX<c> <Rd>, <Rn>, #<lsb>, #<width>', (1, 1, 1, 1, 0, (0), 1, 1, 0, 1, 0, 0, Rn, 0, imm3_2, Rd, imm2, (0), widthm1)),
    Instruction('SDIV<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, Rn, (1), (1), (1), (1), Rd, 1, 1, 1, 1, Rm)),
    Instruction('SEL<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 1, 0, 0, 0, Rm)),
    Instruction('SETEND <endian_specifier>', (1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, (1), E, (0), (0), (0))),
    Instruction('SEV<c>', (1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0)),
    Instruction('SEV<c>.W', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)),
    Instruction('SHADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SHADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SHASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SHSAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SHSUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SHSUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SMLABB<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMLABT<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMLATB<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, Ra, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SMLATT<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, Ra, Rd, 0, 0, 1, 1, Rm)),
    Instruction('SMLAD<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMLADX<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMLAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm)),
    Instruction('SMLALBB<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 0, 0, 0, Rm)),
    Instruction('SMLALBT<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 0, 0, 1, Rm)),
    Instruction('SMLALTB<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 0, 1, 0, Rm)),
    Instruction('SMLALTT<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 0, 1, 1, Rm)),
    Instruction('SMLALD<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 1, 0, 0, Rm)),
    Instruction('SMLALDX<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, Rn, RdLo, RdHi, 1, 1, 0, 1, Rm)),
    Instruction('SMLAWB<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMLAWT<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMLSD<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMLSDX<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMLSLD<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, Rn, RdLo, RdHi, 1, 1, 0, 0, Rm)),
    Instruction('SMLSLDX<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, Rn, RdLo, RdHi, 1, 1, 0, 1, Rm)),
    Instruction('SMMLA<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMMLAR<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMMLS<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMMLSR<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, Rn, Ra, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMMUL<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMMULR<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMUAD<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMUADX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMULBB<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMULBT<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMULTB<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 0, Rm)),
    Instruction('SMULTT<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 1, 1, Rm)),
    Instruction('SMULL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm)),
    Instruction('SMULWB<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMULWT<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SMUSD<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SMUSDX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 1, Rm)),
    Instruction('SSAT<c> <Rd>, #<sat_imm>, <Rn>, <shift>', (1, 1, 1, 1, 0, (0), 1, 1, 0, 0, sh, 0, Rn, 0, imm3_2, Rd, imm2, (0), sat_imm5)),
    Instruction('SSAT16<c> <Rd>, #<sat_imm>, <Rn>', (1, 1, 1, 1, 0, (0), 1, 1, 0, 0, 1, 0, Rn, 0, 0, 0, 0, Rd, 0, 0, (0), (0), sat_imm4)),
    Instruction('SSAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SSUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('SSUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('STM<c> <Rn>!, <registers>', (1, 1, 0, 0, 0, Rn3, register_list8), macro=Assign(W=True)),
    Instruction('STM<c>.W <Rn>{!}, <registers>', (1, 1, 1, 0, 1, 0, 0, 0, 1, 0, W, 0, Rn, (0), register_list1_14, (0), register_list13)),
    Instruction('STMDB<c> <Rn>{!}, <registers>', (1, 1, 1, 0, 1, 0, 0, 1, 0, 0, W, 0, Rn, (0), register_list1_14, (0), register_list13)),
    Instruction('STR<c> <Rt3>, [<Rn3>{, #<imm>}]', (0, 1, 1, 0, 0, imm5, Rn3, Rt3)),
    Instruction('STR<c> <Rt3>, [SP, #<imm>]', (1, 0, 0, 1, 0, Rt3, imm8)),
    Instruction('STR<c>.W <Rt>, [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, imm12)),
    Instruction('STR<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 1, P, U, W, imm8)),
    Instruction('STR<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 0, 0, 0, Rm3, Rn3, Rt3)),
    Instruction('STR<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('STRB<c> <Rt3>, [<Rn3>, #<imm5>]', (0, 1, 1, 1, 0, imm5, Rn3, Rt3)),
    Instruction('STRB<c>.W <Rt>, [<Rn>, #<imm12>]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, Rn, Rt, imm12)),
    Instruction('STRB<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 1, P, U, W, imm8)),
    Instruction('STRB<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 0, 1, 0, Rm3, Rn3, Rt3)),
    Instruction('STRB<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('STRBT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('STRD<c> <Rt>, <Rt2>, [<Rn>{, #+/-<imm>}]', (1, 1, 1, 0, 1, 0, 0, P, U, 1, W, 0, Rn, Rt, Rt2, imm8)),
    Instruction('STREX<c> <Rd>, <Rt>, [<Rn>{, #<imm>}]', (1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, Rd, imm8)),
    Instruction('STREXB<c> <Rd>, <Rt>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 0, Rd)),
    Instruction('STREXD<c> <Rd>, <Rt>, <Rt2>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, Rt2, 0, 1, 1, 1, Rd)),
    Instruction('STREXH<c> <Rd>, <Rt>, [<Rn>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, Rn, Rt, (1), (1), (1), (1), 0, 1, 0, 1, Rd)),
    Instruction('STRH<c> <Rt3>, [<Rn3>{, #<imm>}]', (1, 0, 0, 0, 0, imm5, Rn3, Rt3)),
    Instruction('STRH<c>.W <Rt>, [<Rn>{, #<imm12>}]', (1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, Rn, Rt, imm12)),
    Instruction('STRH<c> <Rt>, [<Rn>, #-<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 1, P, U, W, imm8)),
    Instruction('STRH<c> <Rt3>, [<Rn3>, <Rm3>]', (0, 1, 0, 1, 0, 0, 1, Rm3, Rn3, Rt3)),
    Instruction('STRH<c>.W <Rt>, [<Rn>, <Rm>{, LSL #<imm2>}]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 0, 0, 0, 0, 0, 0, imm2, Rm)),
    Instruction('STRHT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('STRT<c> <Rt>, [<Rn>, #<imm8>]', (1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, Rn, Rt, 1, 1, 1, 0, imm8)),
    Instruction('SUB{S}<c> <Rd3>, <Rn3>, #<imm3>', (0, 0, 0, 1, 1, 1, 1, imm3, Rn3, Rd3), macro=AssignS_IT),
    Instruction('SUB{S}<c> <Rdn3>, #<imm8>', (0, 0, 1, 1, 1, Rdn3, imm8), macro=AssignS_IT),
    Instruction('SUB{S}<c>.W <Rd>, <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 1, 1, 0, 1, S, Rn, 0, imm3_8, Rd, imm8), macro=ThumbExpandImm),
    Instruction('SUBW<c> <Rd>, <Rn>, #<imm12>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 1, 0, 1, 0, Rn, 0, imm3_8, Rd, imm8)),
    Instruction('SUB{S}<c> <Rd3>, <Rn3>, <Rm3>', (0, 0, 0, 1, 1, 0, 1, Rm3, Rn3, Rd3), macro=AssignS_IT),
    Instruction('SUB{S}<c>.W <Rd>, <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, S, Rn, (0), imm3_2, Rd, imm2, typ, Rm)),
    Instruction('SUB<c> <Rd=SP>, <Rn=SP>, #<imm>', (1, 0, 1, 1, 0, 0, 0, 0, 1, imm7), macro=Assign(Rd='SP', Rn='SP')),
    # Instruction('SUB{S}<c>.W <Rd>, <Rn=SP>, #<const>', (1, 1, 1, 1, 0, imm1, 0, 1, 1, 0, 1, S, 1, 1, 0, 1, 0, imm3, Rd, imm8), macros=[ThumbExpandImm, Assign(Rn='SP')]),
    Instruction('SUBW<c> <Rd>, <Rn=SP>, #<imm12>', (1, 1, 1, 1, 0, imm1_11, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, imm3_8, Rd, imm8), macro=Assign(Rn='SP')),
    # Instruction('SUB{S}<c> <Rd>, <Rn=SP>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, S, 1, 1, 0, 1, (0), imm3, Rd, imm2, typ, Rm), macro=Assign(Rn='SP')),
    Instruction('SVC<c> #<imm8>', (1, 1, 0, 1, 1, 1, 1, 1, imm8)),
    Instruction('SXTAB<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('SXTAB16<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('SXTAH<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('SXTB<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 0, 0, 1, 0, 0, 1, Rm3, Rd3)),
    Instruction('SXTB<c>.W <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('SXTB16<c> <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('SXTH<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 0, 0, 1, 0, 0, 0, Rm3, Rd3)),
    Instruction('SXTH<c>.W <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('TBB<c> [<Rn>+/-<Rm><shift>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, (1), (1), (1), (1), (0), (0), (0), (0), 0, 0, 0, 0, Rm), macro=Assign(U=True)),
    Instruction('TBH<c> [<Rn>+/-<Rm><shift>]', (1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, Rn, (1), (1), (1), (1), (0), (0), (0), (0), 0, 0, 0, 1, Rm), macro=Assign(U=True, shift_type='S_LSL', imm=1)),
    Instruction('TEQ<c> <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 1, 0, 0, 1, Rn, 0, imm3_8, 1, 1, 1, 1, imm8), macro=ThumbExpandImm),
    Instruction('TEQ<c> <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, Rn, (0), imm3_2, 1, 1, 1, 1, imm2, typ, Rm)),
    Instruction('TST<c> <Rn>, #<const>', (1, 1, 1, 1, 0, imm1_11, 0, 0, 0, 0, 0, 1, Rn, 0, imm3_8, 1, 1, 1, 1, imm8), macro=ThumbExpandImm),
    Instruction('TST<c> <Rn3>, <Rm3>', (0, 1, 0, 0, 0, 0, 1, 0, 0, 0, Rm3, Rn3)),
    Instruction('TST<c>.W <Rn>, <Rm>, <shift>', (1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, Rn, (0), imm3_2, 1, 1, 1, 1, imm2, typ, Rm)),
    Instruction('UADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('UADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('UASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('UBFX<c> <Rd>, <Rn>, #<lsb>, #<width>', (1, 1, 1, 1, 0, (0), 1, 1, 1, 1, 0, 0, Rn, 0, imm3_2, Rd, imm2, (0), widthm1)),
    Instruction('UDF<c> #<imm8>', (1, 1, 0, 1, 1, 1, 1, 0, imm8)),
    Instruction('UDF<c>.W #<imm16>', (1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, imm4_12, 1, 0, 1, 0, imm12)),
    Instruction('UDIV<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, Rn, (1), (1), (1), (1), Rd, 1, 1, 1, 1, Rm)),
    Instruction('UHADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UHADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UHASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UHSAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UHSUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UHSUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 1, 0, Rm)),
    Instruction('UMAAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, Rn, RdLo, RdHi, 0, 1, 1, 0, Rm)),
    Instruction('UMLAL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm)),
    Instruction('UMULL<c> <RdLo>, <RdHi>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, Rn, RdLo, RdHi, 0, 0, 0, 0, Rm)),
    Instruction('UQADD16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('UQADD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('UQASX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('UQSAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('UQSUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('UQSUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 1, Rm)),
    Instruction('USAD8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, Rn, 1, 1, 1, 1, Rd, 0, 0, 0, 0, Rm)),
    Instruction('USADA8<c> <Rd>, <Rn>, <Rm>, <Ra>', (1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, Rn, Ra, Rd, 0, 0, 0, 0, Rm)),
    Instruction('USAT<c> <Rd>, #<sat_imm>, <Rn>, <shift>', (1, 1, 1, 1, 0, (0), 1, 1, 1, 0, sh, 0, Rn, 0, imm3_2, Rd, imm2, (0), sat_imm5)),
    Instruction('USAT16<c> <Rd>, #<sat_imm>, <Rn>', (1, 1, 1, 1, 0, (0), 1, 1, 1, 0, 1, 0, Rn, 0, 0, 0, 0, Rd, 0, 0, (0), (0), sat_imm4)),
    Instruction('USAX<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('USUB16<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('USUB8<c> <Rd>, <Rn>, <Rm>', (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, Rn, 1, 1, 1, 1, Rd, 0, 1, 0, 0, Rm)),
    Instruction('UXTAB<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('UXTAB16<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('UXTAH<c> <Rd>, <Rn>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, Rn, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('UXTB<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 0, 0, 1, 0, 1, 1, Rm3, Rd3)),
    Instruction('UXTB<c>.W <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('UXTB16<c> <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('UXTH<c> <Rd3>, <Rm3>', (1, 0, 1, 1, 0, 0, 1, 0, 1, 0, Rm3, Rd3)),
    Instruction('UXTH<c>.W <Rd>, <Rm>, <rotation>', (1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, Rd, 1, (0), rotate, Rm)),
    Instruction('WFE<c>', (1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0)),
    Instruction('WFE<c>.W', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)),
    Instruction('WFI<c>', (1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0)),
    Instruction('WFI<c>.W', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)),
    Instruction('YIELD<c>', (1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0)),
    Instruction('YIELD<c>.W', (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, (1), (1), (1), (1), 1, 0, (0), 0, (0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)),
]

table = ThumbTable(_table, 32)