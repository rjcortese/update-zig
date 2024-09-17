const std = @import("std");
const mem = std.mem;
const print = std.debug.print;

pub fn expandPath(path: []const u8) []const u8 {
    if (mem.eql(u8, path[0..1], "~")) {
        return path;
    } else {
        return "doesn't start with ~";
    }
}

test "we can expand ~" {
    const download_dir = "~/Downloads";

    const r = expandPath(download_dir);
    print("{s}\n", .{r});
}
