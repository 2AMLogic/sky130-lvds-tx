// NEGATIVE CONTROL: counter wraps one cycle late (÷5). Must fail the bench.
// 8:1 -> 2:1 serializer reduction (spec S1/S2, DR-003, DR-004).
//
// Runs on the 500 MHz DDR bit clock `clk`. Each cycle presents two bits on
// `dout` (bit 0 first on the DDR mux, bit 1 second); the standard-cell
// partition ends here, the DDR mux onward is the custom analog partition.
//
//   - cnt:    divide-by-WIDTH/2 word counter (÷4 for WIDTH = 8)
//   - word_clk: registered 125 MHz word clock (÷4, 50 % duty), the S1 output
//   - cap:    capture register; samples `din` once per word, mid-word, so the
//             parallel input has a full word period of setup
//   - sr:     loadable shift register, one mux2 level per bit: loads `cap`
//             on the last cycle of a word, otherwise shifts right by two
//
// Bit order: din[0] is transmitted first. `din` is sampled at the rising clk
// edge that ends the cycle with cnt == CYC-2 (word_clk is high); the word
// appears on dout starting with the cycle in which word_clk next falls.
//
// WIDTH must be even and >= 4 (WIDTH/2 cycles per word); the parameter lets
// the 400 Mb/s fallback reuse this file, it is not a separate verified mode.
module serializer #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,       // synchronous, active high
    input  wire [WIDTH-1:0] din,
    output wire [1:0]       dout,
    output reg              word_clk
);
    localparam CYC = WIDTH / 2;
    localparam CW  = $clog2(CYC + 1);

    // Constants kept 32-bit, then sliced to the counter width (lint-clean).
    localparam [31:0] LAST_W = CYC;
    localparam [31:0] CAPT_W = CYC - 2;
    localparam [31:0] HALF_W = CYC / 2;
    localparam [CW-1:0] LAST = LAST_W[CW-1:0];
    localparam [CW-1:0] CAPT = CAPT_W[CW-1:0];
    localparam [CW-1:0] HALF = HALF_W[CW-1:0];

    reg [CW-1:0]    cnt;
    reg [WIDTH-1:0] cap;
    reg [WIDTH-1:0] sr;

    wire             last     = (cnt == LAST);
    wire [CW-1:0]    cnt_next = last ? {CW{1'b0}} : cnt + {{(CW-1){1'b0}}, 1'b1};

    assign dout = sr[1:0];

    always @(posedge clk) begin
        if (rst) begin
            cnt      <= {CW{1'b0}};
            word_clk <= 1'b0;
            cap      <= {WIDTH{1'b0}};
            sr       <= {WIDTH{1'b0}};
        end else begin
            cnt      <= cnt_next;
            word_clk <= (cnt_next >= HALF);
            if (cnt == CAPT) cap <= din;
            if (last) sr <= cap;
            else      sr <= {2'b00, sr[WIDTH-1:2]};
        end
    end
endmodule
