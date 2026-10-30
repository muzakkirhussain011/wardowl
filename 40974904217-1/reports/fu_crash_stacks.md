# Chroma: what the crashing processes printed

## G = 40,000 (fault handler on): crash, exit status -11

stderr_tail:

```
Fatal Python error: Segmentation fault

Current thread 0x00007f2863b89b80 (most recent call first):
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/rust.py", line 582 in _query
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/models/Collection.py", line 265 in query
  File "/home/runner/work/wardowl/wardowl/wardowl/backends/chroma.py", line 233 in search
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 502 in _run
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 285 in retrieve
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_filter_scaling.py", line 102 in measure
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 66 in child
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 164 in main
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 172 in <module>

Extension modules: numpy._core._multiarray_umath, numpy.linalg._umath_linalg, numpy.random._common, numpy.random.bit_generator, numpy.random._bounded_integers, numpy.random._pcg64, numpy.random._generator, numpy.random._mt19937, numpy.random._philox, numpy.random._sfc64, numpy.random.mtrand, pybase64._pybase64, zstandard.backend_c, yaml._yaml, grpc._cython.cygrpc, google._upb._message (total: 16)
```

stdout_tail:

```
child G=40000: built in 3.6 s, where of 2,657,983 characters, querying
```

## G = 25,000 (fault handler on): crash, exit status -11

stderr_tail:

```
Fatal Python error: Segmentation fault

Current thread 0x00007f5c65341b80 (most recent call first):
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/rust.py", line 582 in _query
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/models/Collection.py", line 265 in query
  File "/home/runner/work/wardowl/wardowl/wardowl/backends/chroma.py", line 233 in search
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 502 in _run
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 285 in retrieve
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_filter_scaling.py", line 102 in measure
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 66 in child
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 164 in main
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 172 in <module>

Extension modules: numpy._core._multiarray_umath, numpy.linalg._umath_linalg, numpy.random._common, numpy.random.bit_generator, numpy.random._bounded_integers, numpy.random._pcg64, numpy.random._generator, numpy.random._mt19937, numpy.random._philox, numpy.random._sfc64, numpy.random.mtrand, pybase64._pybase64, zstandard.backend_c, yaml._yaml, grpc._cython.cygrpc, google._upb._message (total: 16)
```

stdout_tail:

```
child G=25000: built in 3.6 s, where of 1,652,983 characters, querying
```

## G = 17,500 (fault handler on): crash, exit status -11

stderr_tail:

```
Fatal Python error: Segmentation fault

Current thread 0x00007f4b81ae5b80 (most recent call first):
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/rust.py", line 582 in _query
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/models/Collection.py", line 265 in query
  File "/home/runner/work/wardowl/wardowl/wardowl/backends/chroma.py", line 233 in search
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 502 in _run
  File "/home/runner/work/wardowl/wardowl/wardowl/retriever.py", line 285 in retrieve
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_filter_scaling.py", line 102 in measure
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 66 in child
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 164 in main
  File "/home/runner/work/wardowl/wardowl/benchmarks/paper/x3_chroma_bisect.py", line 172 in <module>

Extension modules: numpy._core._multiarray_umath, numpy.linalg._umath_linalg, numpy.random._common, numpy.random.bit_generator, numpy.random._bounded_integers, numpy.random._pcg64, numpy.random._generator, numpy.random._mt19937, numpy.random._philox, numpy.random._sfc64, numpy.random.mtrand, pybase64._pybase64, zstandard.backend_c, yaml._yaml, grpc._cython.cygrpc, google._upb._message (total: 16)
```

stdout_tail:

```
child G=17500: built in 3.7 s, where of 1,150,483 characters, querying
```

## G = 40,000 under gdb: crash, exit status 0

stdout_tail:

```
Thread 1 "python" received signal SIGSEGV, Segmentation fault.
  Id   Target Id                                          Frame 
* 1    Thread 0x7ffff7ec6b80 (LWP 3022) "python"          0x00007fffd2d9a449 in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
  2    Thread 0x7fffebbff6c0 (LWP 3030) "python"          0x00007ffff7498e51 in __futex_abstimed_wait_common64 (private=0, cancel=true, abstime=0x0, op=393, expected=0, futex_word=0x7ffff5fbd660 <thread_status+96>) at ./nptl/futex-internal.c:57
  3    Thread 0x7fffeabfe6c0 (LWP 3031) "python"          0x00007ffff7498e51 in __futex_abstimed_wait_common64 (private=0, cancel=true, abstime=0x0, op=393, expected=0, futex_word=0x7ffff5fbd6e0 <thread_status+224>) at ./nptl/futex-internal.c:57
  4    Thread 0x7fffe9bfd6c0 (LWP 3032) "python"          0x00007ffff7498e51 in __futex_abstimed_wait_common64 (private=0, cancel=true, abstime=0x0, op=393, expected=0, futex_word=0x7ffff5fbd760 <thread_status+352>) at ./nptl/futex-internal.c:57
  6    Thread 0x7fffdb1966c0 (LWP 3034) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  7    Thread 0x7fffdaf956c0 (LWP 3035) "tokio-rt-worker" 0x00007ffff752a2d2 in epoll_wait (epfd=4, events=0x555557093340, maxevents=1024, timeout=28671) at ../sysdeps/unix/sysv/linux/epoll_wait.c:30
  8    Thread 0x7fffdad946c0 (LWP 3036) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  9    Thread 0x7fffdab936c0 (LWP 3037) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  10   Thread 0x7fffda9926c0 (LWP 3038) "sqlx-sqlite-wor" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  11   Thread 0x7fffc03ff6c0 (LWP 3040) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  12   Thread 0x7fffbbfff6c0 (LWP 3041) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  13   Thread 0x7fffbbdfe6c0 (LWP 3042) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
  14   Thread 0x7fffbbbfd6c0 (LWP 3043) "tokio-rt-worker" syscall () at ../sysdeps/unix/sysv/linux/x86_64/syscall.S:38
#0  0x00007fffd2d9a449 in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#1  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#2  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#3  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#4  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#5  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#6  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#7  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#8  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#9  0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#10 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#11 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#12 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#13 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#14 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#15 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#16 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#17 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#18 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#19 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#20 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#21 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#22 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#23 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#24 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#25 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#26 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#27 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#28 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#29 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#30 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#31 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#32 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#33 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#34 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#35 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#36 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#37 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#38 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#39 0x00007fffd2d9a46c in ?? () from /opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb_rust_bindings/chromadb_rust_bindings.abi3.so
#16521 0x00007ffff798d830 in _PyEval_EvalFrameDefault (tstate=<optimized out>, frame=0x7ffff7ea1560, throwflag=<optimized out>) at Python/bytecodes.c:3263
#16522 0x00007ffff7ae8f36 in PyEval_EvalCode (co=co@entry=0x7ffff7764730, globals=globals@entry=0x7ffff779eac0, locals=locals@entry=0x7ffff779eac0) at Python/ceval.c:580
#16523 0x00007ffff7b09f77 in run_eval_code_obj (tstate=tstate@entry=0x7ffff7e8c6f0 <_PyRuntime+458992>, co=co@entry=0x7ffff7764730, globals=globals@entry=0x7ffff779eac0, locals=locals@entry=0x7ffff779eac0) at Python/pythonrun.c:1757
#16524 0x00007ffff7b09aab in run_mod (mod=mod@entry=0x55555569af68, filename=filename@entry=0x7ffff76f14c0, globals=globals@entry=0x7ffff779eac0, locals=locals@entry=0x7ffff779eac0, flags=flags@entry=0x7fffffffcf00, arena=arena@entry=0x7ffff76c3e30) at Python/pythonrun.c:1778
#16525 0x00007ffff7b099f2 in pyrun_file (fp=fp@entry=0x555555559490, filename=filename@entry=0x7ffff76f14c0, start=start@entry=257, globals=globals@entry=0x7ffff779eac0, locals=locals@entry=0x7ffff779eac0, closeit=closeit@entry=1, flags=0x7fffffffcf00) at Python/pythonrun.c:1674
#16526 0x00007ffff7b09853 in _PyRun_SimpleFileObject (fp=0x555555559490, filename=0x7ffff76f14c0, closeit=1, flags=0x7fffffffcf00) at Python/pythonrun.c:459
#16527 0x00007ffff7b09668 in _PyRun_AnyFileObject (fp=fp@entry=0x555555559490, filename=filename@entry=0x7ffff76f14c0, closeit=closeit@entry=1, flags=flags@entry=0x7fffffffcf00) at Python/pythonrun.c:78
#16528 0x00007ffff7b12944 in pymain_run_file_obj (skip_source_first_line=0, filename=0x7ffff76f14c0, program_name=0x7ffff7341110) at Modules/main.c:361
#16529 pymain_run_file (config=0x7ffff7e2f2d0 <_PyRuntime+77008>) at Modules/main.c:380
#16530 pymain_run_python (exitcode=0x7fffffffced4) at Modules/main.c:634
#16531 Py_RunMain () at Modules/main.c:714
#16532 0x00007ffff7b1243b in Py_BytesMain (argc=<optimized out>, argv=<optimized out>) at Modules/main.c:768
#16533 0x00007ffff742a1ca in __libc_start_call_main (main=main@entry=0x555555555060 <main>, argc=argc@entry=11, argv=argv@entry=0x7fffffffd168) at ../sysdeps/nptl/libc_start_call_main.h:58
#16534 0x00007ffff742a28b in __libc_start_main_impl (main=0x555555555060 <main>, argc=11, argv=0x7fffffffd168, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffd158) at ../csu/libc-start.c:360
#16535 0x0000555555555095 in _start ()
```

