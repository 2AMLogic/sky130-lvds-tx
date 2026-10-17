// Placeholder DUT for the cold-start harness smoke test. Not part of the
// design: rtl/ stays empty until the real serializer lands.
module smoke (
    input  wire       clk,
    input  wire       rst,
    output reg  [3:0] count
);
    always @(posedge clk) begin
        if (rst) count <= 4'd0;
        else     count <= count + 4'd1;
    end
endmodule
