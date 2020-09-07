"""
TODO:
 - inval precommit hooks
  - no central caches.py, classpath scan + reflect
  - 'ver' and 'rev' keys - update in place, enforce mono for ver
  - get from git diff
  - autobust when src files change?
  - 'build' or 'dist' dir like tests, stripped?
   - subdirs? proto.dist, strip gen?
 - CACHE_VERSION somewhere, bump when formats change
  - precompile all jinjas - can’t make faster, dogshit slow - have to key off all included files..
  - parse all queries - cython
  - analysis?
 - ** cache busting machinery does flip tolerance - if new master understands op data allow otherwise kill **
"""
