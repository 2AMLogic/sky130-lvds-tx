// Negative control: same module name and ports as ../smoke.v, one deliberate
// bug (counts by two). The unmodified test module must fail against this.
module smoke (
    input  wire       clk,
    input  wire       rst,
    output reg  [3:0] count
);
    always @(posedge clk) begin
        if (rst) count <= 4'd0;
        else     count <= count + 4'd2;
    end
endmodule
