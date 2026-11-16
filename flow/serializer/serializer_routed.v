module serializer (clk,
    rst,
    word_clk,
    din,
    dout);
 input clk;
 input rst;
 output word_clk;
 input [7:0] din;
 output [1:0] dout;

 wire _000_;
 wire _001_;
 wire _002_;
 wire _003_;
 wire _004_;
 wire _005_;
 wire _006_;
 wire _007_;
 wire _008_;
 wire _009_;
 wire _010_;
 wire _011_;
 wire _012_;
 wire _013_;
 wire _014_;
 wire _015_;
 wire _016_;
 wire _017_;
 wire _018_;
 wire _019_;
 wire _020_;
 wire _021_;
 wire net3;
 wire _023_;
 wire _024_;
 wire _025_;
 wire net2;
 wire _027_;
 wire _028_;
 wire _029_;
 wire _030_;
 wire net6;
 wire _032_;
 wire _033_;
 wire _034_;
 wire _035_;
 wire _036_;
 wire _037_;
 wire _038_;
 wire _039_;
 wire _040_;
 wire _041_;
 wire _042_;
 wire _043_;
 wire _044_;
 wire _045_;
 wire _046_;
 wire _047_;
 wire _048_;
 wire _049_;
 wire _050_;
 wire _051_;
 wire _052_;
 wire _053_;
 wire _054_;
 wire _055_;
 wire capture;
 wire load;
 wire net4;
 wire net5;
 wire clknet_0_clk;
 wire clknet_1_0__leaf_clk;
 wire clknet_1_1__leaf_clk;
 wire [7:0] cap;
 wire [0:0] cnt;
 wire [7:0] sr;

 sky130_fd_sc_hd__nand2_1 _057_ (.A(net6),
    .B(din[2]),
    .Y(_023_));
 sky130_fd_sc_hd__nand2b_1 _058_ (.A_N(net4),
    .B(cap[2]),
    .Y(_024_));
 sky130_fd_sc_hd__clkbuf_1 _059_ (.A(rst),
    .X(_025_));
 sky130_fd_sc_hd__a21oi_1 _061_ (.A1(_024_),
    .A2(_023_),
    .B1(_025_),
    .Y(_000_));
 sky130_fd_sc_hd__nand2_1 _062_ (.A(net6),
    .B(din[1]),
    .Y(_027_));
 sky130_fd_sc_hd__nand2b_1 _063_ (.A_N(net4),
    .B(cap[1]),
    .Y(_028_));
 sky130_fd_sc_hd__a21oi_1 _064_ (.A1(_028_),
    .A2(_027_),
    .B1(_025_),
    .Y(_001_));
 sky130_fd_sc_hd__nand2_1 _065_ (.A(net6),
    .B(din[0]),
    .Y(_029_));
 sky130_fd_sc_hd__nand2b_1 _066_ (.A_N(net4),
    .B(cap[0]),
    .Y(_030_));
 sky130_fd_sc_hd__a21oi_1 _067_ (.A1(_030_),
    .A2(_029_),
    .B1(_025_),
    .Y(_002_));
 sky130_fd_sc_hd__nand2b_1 _069_ (.A_N(load),
    .B(sr[6]),
    .Y(_032_));
 sky130_fd_sc_hd__nand2_1 _070_ (.A(cap[4]),
    .B(load),
    .Y(_033_));
 sky130_fd_sc_hd__a21oi_1 _071_ (.A1(_032_),
    .A2(_033_),
    .B1(_025_),
    .Y(_003_));
 sky130_fd_sc_hd__nor2_1 _072_ (.A(net3),
    .B(_025_),
    .Y(_004_));
 sky130_fd_sc_hd__nand2b_1 _073_ (.A_N(_025_),
    .B(net3),
    .Y(_034_));
 sky130_fd_sc_hd__nor3b_2 _074_ (.A(cnt[0]),
    .B(_025_),
    .C_N(word_clk),
    .Y(_008_));
 sky130_fd_sc_hd__o21bai_1 _075_ (.A1(word_clk),
    .A2(_034_),
    .B1_N(_008_),
    .Y(_005_));
 sky130_fd_sc_hd__nand2_1 _076_ (.A(net6),
    .B(din[7]),
    .Y(_035_));
 sky130_fd_sc_hd__nand2b_1 _077_ (.A_N(net4),
    .B(cap[7]),
    .Y(_036_));
 sky130_fd_sc_hd__a21oi_1 _078_ (.A1(_036_),
    .A2(_035_),
    .B1(_025_),
    .Y(_006_));
 sky130_fd_sc_hd__inv_1 _079_ (.A(cap[7]),
    .Y(_037_));
 sky130_fd_sc_hd__nand2b_1 _080_ (.A_N(_025_),
    .B(load),
    .Y(_038_));
 sky130_fd_sc_hd__nor2_1 _081_ (.A(_037_),
    .B(_038_),
    .Y(_007_));
 sky130_fd_sc_hd__nor2_1 _082_ (.A(word_clk),
    .B(_034_),
    .Y(_009_));
 sky130_fd_sc_hd__nand2b_1 _083_ (.A_N(load),
    .B(sr[7]),
    .Y(_039_));
 sky130_fd_sc_hd__nand2_1 _084_ (.A(cap[5]),
    .B(load),
    .Y(_040_));
 sky130_fd_sc_hd__a21oi_1 _085_ (.A1(_039_),
    .A2(_040_),
    .B1(_025_),
    .Y(_010_));
 sky130_fd_sc_hd__nand2b_1 _086_ (.A_N(load),
    .B(sr[5]),
    .Y(_041_));
 sky130_fd_sc_hd__nand2_1 _087_ (.A(cap[3]),
    .B(load),
    .Y(_042_));
 sky130_fd_sc_hd__a21oi_1 _088_ (.A1(_041_),
    .A2(_042_),
    .B1(_025_),
    .Y(_011_));
 sky130_fd_sc_hd__nand2b_1 _089_ (.A_N(load),
    .B(sr[4]),
    .Y(_043_));
 sky130_fd_sc_hd__nand2_1 _090_ (.A(cap[2]),
    .B(load),
    .Y(_044_));
 sky130_fd_sc_hd__a21oi_1 _091_ (.A1(_043_),
    .A2(_044_),
    .B1(_025_),
    .Y(_012_));
 sky130_fd_sc_hd__nand2_1 _092_ (.A(net6),
    .B(din[5]),
    .Y(_045_));
 sky130_fd_sc_hd__nand2b_1 _093_ (.A_N(net4),
    .B(cap[5]),
    .Y(_046_));
 sky130_fd_sc_hd__a21oi_1 _094_ (.A1(_046_),
    .A2(_045_),
    .B1(_025_),
    .Y(_013_));
 sky130_fd_sc_hd__nand2b_1 _095_ (.A_N(load),
    .B(sr[3]),
    .Y(_047_));
 sky130_fd_sc_hd__nand2_1 _096_ (.A(cap[1]),
    .B(load),
    .Y(_048_));
 sky130_fd_sc_hd__a21oi_1 _097_ (.A1(_047_),
    .A2(_048_),
    .B1(_025_),
    .Y(_014_));
 sky130_fd_sc_hd__nand2b_1 _098_ (.A_N(load),
    .B(sr[2]),
    .Y(_049_));
 sky130_fd_sc_hd__nand2_1 _099_ (.A(cap[0]),
    .B(load),
    .Y(_050_));
 sky130_fd_sc_hd__a21oi_1 _100_ (.A1(_049_),
    .A2(_050_),
    .B1(_025_),
    .Y(_015_));
 sky130_fd_sc_hd__inv_1 _101_ (.A(cap[6]),
    .Y(_051_));
 sky130_fd_sc_hd__nor2_1 _102_ (.A(_051_),
    .B(_038_),
    .Y(_016_));
 sky130_fd_sc_hd__nand2_4 _103_ (.A(net6),
    .B(din[3]),
    .Y(_052_));
 sky130_fd_sc_hd__nand2b_1 _104_ (.A_N(net5),
    .B(cap[3]),
    .Y(_053_));
 sky130_fd_sc_hd__a21oi_1 _105_ (.A1(_053_),
    .A2(_052_),
    .B1(_025_),
    .Y(_017_));
 sky130_fd_sc_hd__nand2_1 _106_ (.A(net4),
    .B(din[6]),
    .Y(_054_));
 sky130_fd_sc_hd__nand2b_1 _107_ (.A_N(net5),
    .B(cap[6]),
    .Y(_055_));
 sky130_fd_sc_hd__a21oi_1 _108_ (.A1(_055_),
    .A2(_054_),
    .B1(_025_),
    .Y(_018_));
 sky130_fd_sc_hd__nand2_4 _109_ (.A(din[4]),
    .B(net6),
    .Y(_020_));
 sky130_fd_sc_hd__nand2b_1 _110_ (.A_N(net4),
    .B(cap[4]),
    .Y(_021_));
 sky130_fd_sc_hd__a21oi_1 _111_ (.A1(_021_),
    .A2(_020_),
    .B1(_025_),
    .Y(_019_));
 sky130_fd_sc_hd__dfxtp_4 _112_ (.CLK(clknet_1_0__leaf_clk),
    .D(_009_),
    .Q(capture));
 sky130_fd_sc_hd__dfxtp_4 _113_ (.CLK(clknet_1_0__leaf_clk),
    .D(net2),
    .Q(load));
 sky130_fd_sc_hd__dfxtp_1 _114_ (.CLK(clknet_1_0__leaf_clk),
    .D(_016_),
    .Q(sr[6]));
 sky130_fd_sc_hd__dfxtp_1 _115_ (.CLK(clknet_1_1__leaf_clk),
    .D(_007_),
    .Q(sr[7]));
 sky130_fd_sc_hd__dfxtp_1 _116_ (.CLK(clknet_1_1__leaf_clk),
    .D(_015_),
    .Q(sr[0]));
 sky130_fd_sc_hd__dfxtp_1 _117_ (.CLK(clknet_1_0__leaf_clk),
    .D(_014_),
    .Q(sr[1]));
 sky130_fd_sc_hd__dfxtp_1 _118_ (.CLK(clknet_1_1__leaf_clk),
    .D(_012_),
    .Q(sr[2]));
 sky130_fd_sc_hd__dfxtp_1 _119_ (.CLK(clknet_1_0__leaf_clk),
    .D(_011_),
    .Q(sr[3]));
 sky130_fd_sc_hd__dfxtp_1 _120_ (.CLK(clknet_1_1__leaf_clk),
    .D(_003_),
    .Q(sr[4]));
 sky130_fd_sc_hd__dfxtp_1 _121_ (.CLK(clknet_1_1__leaf_clk),
    .D(_010_),
    .Q(sr[5]));
 sky130_fd_sc_hd__dfxtp_1 _122_ (.CLK(clknet_1_1__leaf_clk),
    .D(_002_),
    .Q(cap[0]));
 sky130_fd_sc_hd__dfxtp_1 _123_ (.CLK(clknet_1_0__leaf_clk),
    .D(_001_),
    .Q(cap[1]));
 sky130_fd_sc_hd__dfxtp_1 _124_ (.CLK(clknet_1_1__leaf_clk),
    .D(_000_),
    .Q(cap[2]));
 sky130_fd_sc_hd__dfxtp_1 _125_ (.CLK(clknet_1_0__leaf_clk),
    .D(_017_),
    .Q(cap[3]));
 sky130_fd_sc_hd__dfxtp_1 _126_ (.CLK(clknet_1_1__leaf_clk),
    .D(_019_),
    .Q(cap[4]));
 sky130_fd_sc_hd__dfxtp_1 _127_ (.CLK(clknet_1_1__leaf_clk),
    .D(_013_),
    .Q(cap[5]));
 sky130_fd_sc_hd__dfxtp_1 _128_ (.CLK(clknet_1_0__leaf_clk),
    .D(_018_),
    .Q(cap[6]));
 sky130_fd_sc_hd__dfxtp_1 _129_ (.CLK(clknet_1_1__leaf_clk),
    .D(_006_),
    .Q(cap[7]));
 sky130_fd_sc_hd__dfxtp_1 _130_ (.CLK(clknet_1_0__leaf_clk),
    .D(_004_),
    .Q(cnt[0]));
 sky130_fd_sc_hd__dfxtp_1 _131_ (.CLK(clknet_1_0__leaf_clk),
    .D(_005_),
    .Q(word_clk));
 sky130_fd_sc_hd__buf_4 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__buf_4 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__buf_4 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__inv_1 clkload0 (.A(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkbuf_16 clone6 (.A(capture),
    .X(net6));
 sky130_fd_sc_hd__buf_4 place2 (.A(_008_),
    .X(net2));
 sky130_fd_sc_hd__buf_4 place3 (.A(cnt[0]),
    .X(net3));
 sky130_fd_sc_hd__buf_12 place4 (.A(capture),
    .X(net4));
 sky130_fd_sc_hd__buf_4 place5 (.A(capture),
    .X(net5));
 assign dout[0] = sr[0];
 assign dout[1] = sr[1];
endmodule
