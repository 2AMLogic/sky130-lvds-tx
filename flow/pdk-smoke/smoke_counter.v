// PDK smoke design: a 4-bit synchronous counter. It exists only to prove the
// pinned sky130_fd_sc_hd synthesis and place-and-route path runs; it is not
// the serializer.
module smoke_counter (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [3:0] count
);
    always @(posedge clk) begin
        if (!rst_n) count <= 4'd0;
        else        count <= count + 4'd1;
    end
endmodule
