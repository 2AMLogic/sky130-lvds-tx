module serializer (clk,
    word_clk,
    rst,
    din,
    dout);
 input clk;
 output word_clk;
 input rst;
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
 wire clknet_1_1__leaf_clk;
 wire clknet_0_clk;
 wire clknet_1_0__leaf_clk;
 wire _023_;
 wire _024_;
 wire _025_;
 wire _026_;
 wire _028_;
 wire _029_;
 wire _030_;
 wire _031_;
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
 wire [7:0] cap;
 wire [1:0] cnt;
 wire [7:0] sr;

 sky130_fd_sc_hd__inv_1 _042_ (.A(cap[0]),
    .Y(_018_));
 sky130_fd_sc_hd__nand2b_1 _043_ (.A_N(cnt[0]),
    .B(cnt[1]),
    .Y(_019_));
 sky130_fd_sc_hd__nor3b_1 _047_ (.A(din[0]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_023_));
 sky130_fd_sc_hd__clkbuf_1 _048_ (.A(rst),
    .X(_024_));
 sky130_fd_sc_hd__a211oi_1 _049_ (.A1(_018_),
    .A2(_019_),
    .B1(_023_),
    .C1(_024_),
    .Y(_000_));
 sky130_fd_sc_hd__a21oi_1 _050_ (.A1(cnt[1]),
    .A2(cnt[0]),
    .B1(_024_),
    .Y(_025_));
 sky130_fd_sc_hd__and3b_1 _051_ (.A_N(rst),
    .B(cnt[0]),
    .C(cnt[1]),
    .X(_026_));
 sky130_fd_sc_hd__a22o_1 _053_ (.A1(sr[6]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[4]),
    .X(_001_));
 sky130_fd_sc_hd__a22o_1 _054_ (.A1(sr[5]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[3]),
    .X(_002_));
 sky130_fd_sc_hd__a22o_1 _055_ (.A1(sr[4]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[2]),
    .X(_003_));
 sky130_fd_sc_hd__nor2_1 _056_ (.A(cnt[0]),
    .B(_024_),
    .Y(_004_));
 sky130_fd_sc_hd__inv_1 _057_ (.A(cap[6]),
    .Y(_028_));
 sky130_fd_sc_hd__nor3b_1 _058_ (.A(din[6]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_029_));
 sky130_fd_sc_hd__a211oi_1 _059_ (.A1(_028_),
    .A2(_019_),
    .B1(_029_),
    .C1(_024_),
    .Y(_005_));
 sky130_fd_sc_hd__o21a_1 _060_ (.A1(cnt[1]),
    .A2(cnt[0]),
    .B1(_025_),
    .X(_006_));
 sky130_fd_sc_hd__inv_1 _061_ (.A(cap[7]),
    .Y(_030_));
 sky130_fd_sc_hd__nor3b_1 _062_ (.A(din[7]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_031_));
 sky130_fd_sc_hd__a211oi_1 _063_ (.A1(_030_),
    .A2(_019_),
    .B1(_031_),
    .C1(_024_),
    .Y(_007_));
 sky130_fd_sc_hd__and2_1 _064_ (.A(cap[7]),
    .B(_026_),
    .X(_008_));
 sky130_fd_sc_hd__a22o_1 _065_ (.A1(sr[7]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[5]),
    .X(_009_));
 sky130_fd_sc_hd__a22o_1 _066_ (.A1(sr[3]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[1]),
    .X(_010_));
 sky130_fd_sc_hd__inv_1 _067_ (.A(cap[4]),
    .Y(_032_));
 sky130_fd_sc_hd__nor3b_1 _068_ (.A(din[4]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_033_));
 sky130_fd_sc_hd__a211oi_1 _069_ (.A1(_032_),
    .A2(_019_),
    .B1(_033_),
    .C1(_024_),
    .Y(_011_));
 sky130_fd_sc_hd__a22o_1 _070_ (.A1(sr[2]),
    .A2(_025_),
    .B1(_026_),
    .B2(cap[0]),
    .X(_012_));
 sky130_fd_sc_hd__and2_1 _071_ (.A(cap[6]),
    .B(_026_),
    .X(_013_));
 sky130_fd_sc_hd__inv_1 _072_ (.A(cap[2]),
    .Y(_034_));
 sky130_fd_sc_hd__nor3b_1 _073_ (.A(din[2]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_035_));
 sky130_fd_sc_hd__a211oi_1 _074_ (.A1(_034_),
    .A2(_019_),
    .B1(_035_),
    .C1(_024_),
    .Y(_014_));
 sky130_fd_sc_hd__inv_1 _075_ (.A(cap[1]),
    .Y(_036_));
 sky130_fd_sc_hd__nor3b_1 _076_ (.A(din[1]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_037_));
 sky130_fd_sc_hd__a211oi_1 _077_ (.A1(_036_),
    .A2(_019_),
    .B1(_037_),
    .C1(_024_),
    .Y(_015_));
 sky130_fd_sc_hd__inv_1 _078_ (.A(cap[5]),
    .Y(_038_));
 sky130_fd_sc_hd__nor3b_1 _079_ (.A(din[5]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_039_));
 sky130_fd_sc_hd__a211oi_1 _080_ (.A1(_038_),
    .A2(_019_),
    .B1(_039_),
    .C1(_024_),
    .Y(_016_));
 sky130_fd_sc_hd__inv_1 _081_ (.A(cap[3]),
    .Y(_040_));
 sky130_fd_sc_hd__nor3b_1 _082_ (.A(din[3]),
    .B(cnt[0]),
    .C_N(cnt[1]),
    .Y(_041_));
 sky130_fd_sc_hd__a211oi_1 _083_ (.A1(_040_),
    .A2(_019_),
    .B1(_041_),
    .C1(_024_),
    .Y(_017_));
 sky130_fd_sc_hd__dfxtp_1 _084_ (.CLK(clknet_1_1__leaf_clk),
    .D(_013_),
    .Q(sr[6]));
 sky130_fd_sc_hd__dfxtp_1 _085_ (.CLK(clknet_1_0__leaf_clk),
    .D(_008_),
    .Q(sr[7]));
 sky130_fd_sc_hd__dfxtp_1 _086_ (.CLK(clknet_1_1__leaf_clk),
    .D(_012_),
    .Q(sr[0]));
 sky130_fd_sc_hd__dfxtp_1 _087_ (.CLK(clknet_1_1__leaf_clk),
    .D(_010_),
    .Q(sr[1]));
 sky130_fd_sc_hd__dfxtp_1 _088_ (.CLK(clknet_1_1__leaf_clk),
    .D(_003_),
    .Q(sr[2]));
 sky130_fd_sc_hd__dfxtp_1 _089_ (.CLK(clknet_1_1__leaf_clk),
    .D(_002_),
    .Q(sr[3]));
 sky130_fd_sc_hd__dfxtp_1 _090_ (.CLK(clknet_1_1__leaf_clk),
    .D(_001_),
    .Q(sr[4]));
 sky130_fd_sc_hd__dfxtp_1 _091_ (.CLK(clknet_1_1__leaf_clk),
    .D(_009_),
    .Q(sr[5]));
 sky130_fd_sc_hd__dfxtp_1 _092_ (.CLK(clknet_1_0__leaf_clk),
    .D(_000_),
    .Q(cap[0]));
 sky130_fd_sc_hd__dfxtp_1 _093_ (.CLK(clknet_1_0__leaf_clk),
    .D(_015_),
    .Q(cap[1]));
 sky130_fd_sc_hd__dfxtp_1 _094_ (.CLK(clknet_1_0__leaf_clk),
    .D(_014_),
    .Q(cap[2]));
 sky130_fd_sc_hd__dfxtp_1 _095_ (.CLK(clknet_1_1__leaf_clk),
    .D(_017_),
    .Q(cap[3]));
 sky130_fd_sc_hd__dfxtp_1 _096_ (.CLK(clknet_1_1__leaf_clk),
    .D(_011_),
    .Q(cap[4]));
 sky130_fd_sc_hd__dfxtp_1 _097_ (.CLK(clknet_1_0__leaf_clk),
    .D(_016_),
    .Q(cap[5]));
 sky130_fd_sc_hd__dfxtp_1 _098_ (.CLK(clknet_1_1__leaf_clk),
    .D(_005_),
    .Q(cap[6]));
 sky130_fd_sc_hd__dfxtp_1 _099_ (.CLK(clknet_1_0__leaf_clk),
    .D(_007_),
    .Q(cap[7]));
 sky130_fd_sc_hd__dfxtp_1 _100_ (.CLK(clknet_1_0__leaf_clk),
    .D(_004_),
    .Q(cnt[0]));
 sky130_fd_sc_hd__dfxtp_1 _101_ (.CLK(clknet_1_0__leaf_clk),
    .D(_006_),
    .Q(cnt[1]));
 sky130_fd_sc_hd__buf_4 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__buf_4 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__buf_4 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkinv_1 clkload0 (.A(clknet_1_0__leaf_clk));
 assign word_clk = cnt[1];
 assign dout[0] = sr[0];
 assign dout[1] = sr[1];
endmodule
