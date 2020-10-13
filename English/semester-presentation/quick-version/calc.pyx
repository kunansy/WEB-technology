from libc.math cimport sqrt


cpdef void do_math(float start = 0,
                  float iters_count = 0):
    cdef float pos = start
    cdef float k_sq = 1_000_000

    with nogil:
        while pos < iters_count:
            pos += 1
            sqrt((pos - k_sq)**2)
