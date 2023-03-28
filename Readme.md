# ROS Compression Test

Testing different Compression Algorithms on CDR encoded ROS2 messages.
The tests are using the CLI applications for the corresponding algorithms. For `LZMH` the [Code of this Repo](https://github.com/CenterForSecureEnergyInformatics/data-compressor) is used.

Algorithms:

- [LZMH](https://github.com/CenterForSecureEnergyInformatics/data-compressor)
- [zlib](https://github.com/rudi-cilibrasi/zlibcomplete)
  - `qpdf` Paket
- [bzip2](https://www.cs.cmu.edu/afs/cs/project/pscico-guyb/realworld/99/code/bzip2-0.9.5c/manual_3.html)
- [lzma](https://gist.github.com/phoe/c33e1f8ec651e7892f82596be6d0d3af)
- [zstd](https://github.com/facebook/zstd)
    - might profit from training?
    - can be further optimized
- [lzo](https://gist.github.com/himanshuo/62af1d81d78974ed444f)
- [brotli](https://manpages.ubuntu.com/manpages/bionic/man1/brotli.1.html)

Images:

- libpng
- libjpeg
