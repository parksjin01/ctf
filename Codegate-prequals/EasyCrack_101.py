import os
import angr

addr = [[1, 0x16, 0x400def],
[2, 0x1a, 0x0400ca3],
[3, 0x19, 0x0401025],
[4, 0x14, 0x00400c70],
[5, 0x19, 0x0040112b],
[6, 0x14, 0x004011e7],
[7, 0x17, 0x0400cd3],
[8, 0x16, 0x00400c93],
[9, 0x1c, 0x0400c07],
[10, 0x1b, 0x04011c8],
[11, 0x19, 0x0401094],
[12, 0x1b, 0x00401183],
[13, 0x1b, 0x00400ebe],
[14, 0x17, 0x04012c4],
[15, 0x19, 0x0400e25],
[16, 0x1b, 0x0400ced],
[17, 0x1c, 0x00400fee],
[18, 0x19, 0x0400f9e],
[19, 0x1b, 0x0400dac],
[20, 0x16, 0x0400e2d],
[21, 0x14, 0x0040126e],
[22, 0x18, 0x0400c59],
[23, 0x1c, 0x00400e71],
[24, 0x1c, 0x0400e40],
[25, 0x14, 0x000400bb9],
[26, 0x19, 0x00400fa2],
[27, 0x14, 0x00400d25],
[28, 0x15, 0x00400dbb],
[29, 0x19, 0x00400e0c],
[30, 0x1c, 0x00400ff4],
[31, 0x17, 0x00400fe4],
[32, 0x18, 0x040116d],
[33, 0x1d, 0x00400cb8],
[34, 0x1b, 0x0400f45],
[35, 0x17, 0x0400c29],
[36, 0x1d, 0x0401074],
[37, 0x19, 0x00400dbd],
[38, 0x1b, 0x0401197],
[39, 0x18, 0x04010e0],
[40, 0x16, 0x00401280],
[41, 0x15, 0x00400ce0],
[42, 0x1d, 0x00400fe5],
[43, 0x1d, 0x00400ed3],
[44, 0x17, 0x004010d3],
[45, 0x15, 0x0040101d],
[46, 0x18, 0x00400d7f],
[47, 0x15, 0x00400e2e],
[48, 0x16, 0x00401068],
[49, 0x17, 0x00400f7a],
[50, 0x16, 0x00400ce9],
[51, 0x1b, 0x040112e],
[52, 0x1d, 0x000400f06],
[53, 0x1c, 0x00400ec2],
[54, 0x14, 0x0400f82],
[55, 0x1d, 0x00401183],
[56, 0x1c, 0x00400f01],
[57, 0x1d, 0x00400e47],
[58, 0x1b, 0x00400f01],
[59, 0x17, 0x0040107f],
[60, 0x18, 0x00400fa0],
[61, 0x1d, 0x00401066],
[62, 0x16, 0x00400e1c],
[63, 0x14, 0x00400f6e],
[64, 0x1b, 0x004010a7],
[65, 0x1a, 0x00400ec7],
[66, 0x18, 0x00400ea2],
[67, 0x16, 0x00400faf],
[68, 0x1a, 0x004010e4],
[69, 0x14, 0x0400fbb],
[70, 0x18, 0x00401053],
[71, 0x15, 0x004010e8],
[72, 0x1a, 0x00401148],
[73, 0x18, 0x00400e9a],
[74, 0x16, 0x004010c3],
[75, 0x14, 0x0040110e],
[76, 0x16, 0x00400d59],
[77, 0x18, 0x00400cf5],
[78, 0x16, 0x0400c7c],
[79, 0x16, 0x00400f4c],
[80, 0x1a, 0x004011b6],
[81, 0x19, 0x004011ae],
[82, 0x1c, 0x00400d73],
[83, 0x1c, 0x00400d69],
[84, 0x1a, 0x00401048],
[85, 0x18, 0x000401156],
[86, 0x16, 0x0040117b],
[87, 0x15, 0x00400dac],
[88, 0x1c, 0x00400faf],
[89, 0x15, 0x0400eff],
[90, 0x19, 0x00400fcf],
[91, 0x15, 0x00400c1a],
[92, 0x19, 0x00400e8e],
[93, 0x18, 0x004010f9],
[94, 0x1a, 0x00400db8],
[95, 0x16, 0x00400e3f],
[96, 0x1c, 0x00401290],
[97, 0x1d, 0x040112d],
[98, 0x1a, 0x00400e63],
[99, 0x18, 0x00400f06],
[100, 0x17, 0x004010b5],
[101, 0x1c, 0x00400fcd]]

def crack(num):
        binary = angr.Project('./prob/prob'+str(num+1), load_options={'auto_load_libs':False})
        argv = angr.claripy.BVS('argv', addr[num][1]*8)
        init_state = binary.factory.path(args=['./prob/prob', argv])
        path_group = binary.factory.path_group(init_state, threads=4)
        path_group.explore(find=addr[num][2])
        print 'prob%d:' %(num+1), path_group.found[0].state.se.any_str(argv)

for i in range(101):
        try:
                crack(i)
        except Exception, e:
                print e
                print 'prob%d has error' %i