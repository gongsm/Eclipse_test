#ifndef __PROFILER_H__
#define __PROFILER_H__

#define PROFILING
#ifdef PROFILING
    #define START_PROFILING_FUNC	int var##__FUNCTION__;\
                                    StartProfilerAtom(__FUNCTION__);
    #define END_PROFILING_FUNC		var##__FUNCTION__=0;\
                                    EndProfilerAtom(__FUNCTION__);
    #define PROFILING_FLUSH			ProfilerFlush();
    #define INIT_PROFILING(name, num)          initProfiler(name, num);
#else
    #define START_PROFILING_FUNC
    #define END_PROFILING_FUNC
    #define PROFILING_FLUSH
    #define INIT_PROFILING(name, num)
#endif

void initProfiler(const char *name, int dumpNum);
void StartProfilerAtom(const char* name);
void ProfilerFlush();
void EndProfilerAtom(const char* name);
#endif
