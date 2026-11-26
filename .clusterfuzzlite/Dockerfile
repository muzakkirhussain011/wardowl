# The OSS-Fuzz Python builder, pinned by digest. ClusterFuzzLite builds fuzz/*_fuzzer.py with it.
FROM gcr.io/oss-fuzz-base/base-builder-python@sha256:6ccbb6b02fcbb8e07d15680e933a6d835cdb579636032cec7d256d0f25d483e4
COPY . $SRC/wardowl
WORKDIR $SRC/wardowl
COPY .clusterfuzzlite/build.sh $SRC/
