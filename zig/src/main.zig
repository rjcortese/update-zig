//!
//! checks the zig website for the latest master version of zig
//! if that version is newer than the currently used version,
//! install that version:
//!   * download
//!   * untar at install location
//!   * update symlink in binary location
//!
const std = @import("std");
const print = std.debug.print;
const Dir = std.fs.Dir;

// the system architecture we want to install
const arc = "x86_64-linux";
// where to download the tarball
const download_dir = "~/Downloads";
// we will install zig by making a new directory in this dir
const install_dir = "~/.zig/zigs";
// this dir contains a `zig` symlink to the version of the binary want to use
// this dir should be in the PATH
const binary_dir = "~/.local/bin";

const zig_download_index_url = "https://ziglang.org/download/index.json";

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    // Prints to stderr (it's a shortcut based on `std.io.getStdErr()`)
    print("Checking\n  {s}\nfor latest version of zig\n", .{zig_download_index_url});
    const fullpath = Dir.realpathAlloc(allocator, download_dir);

    print("{s}", .{fullpath});
}
