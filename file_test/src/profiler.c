/***************************************************************
 ***************************************************************
 *                     PROFILING TOOL
 *
 */


#include "string.h"
#include "stdio.h"
#define _WIN32
#ifdef _WIN32
    #include "windows.h"
#else
	#include "apex/apexLib.h"
    #include "configRecordLib.h "
#endif
#include "assert.h"
#include "profiler.h"

#define MAX_FUNCNAME	64
#define MAX_DATA		4*1024
#define MAX_CALL_STACK	128

#define MIN(a, b) ((a)>(b) ? (b) : (a) )
typedef struct{
	char funcName[MAX_FUNCNAME];
	char parentFuncName[MAX_FUNCNAME];
	unsigned long long startTime;
	unsigned long long endTime;
	unsigned int callLevel;
} tProfilerAtom;

tProfilerAtom Atoms[MAX_DATA];

typedef struct{
	unsigned long long totalWrite;
	unsigned int currentTop;
	unsigned int currentCallLevel;
	unsigned int callStack[MAX_CALL_STACK];
	unsigned int callStackTop;
	unsigned int retIdx;
	unsigned int initstack;
	//FILE *writeFile;
	int fileNum;
	char procName[64];
	unsigned int maxDump;
}tProfilerMngr;

tProfilerMngr Mngr;

#ifdef _WIN32
void initProfiler(const char* name, int dumpNum){
	Mngr.totalWrite = 0ULL;
	Mngr.currentTop = 0U;
	Mngr.currentCallLevel = 0U;
	Mngr.callStackTop = 0;
/*	Mngr.writeFile = 0;*/
	Mngr.fileNum = 0;
	Mngr.initstack = 0;
	Mngr.maxDump = dumpNum;
	memset(Mngr.callStack, 0, sizeof(Mngr.callStack));
	memcpy(Mngr.procName, name, strlen(name));
/*	Mngr.writeFile = fopen("file.txt", "wt");*/
}
#else

void initProfiler(const char* name, int dumpNum){
    char fileName[128];
    Mngr.totalWrite = 0ULL;
	Mngr.currentTop = 0U;
	Mngr.currentCallLevel = 0U;
	Mngr.callStackTop = 0;
	//Mngr.writeFile = 0;
	Mngr.fileNum = 0;
	Mngr.maxDump = dumpNum;
	memset(Mngr.callStack, 0, sizeof(Mngr.callStack));
    //configRecordFieldGet(PARTITION_NAME, &Mngr.procName);
    memcpy(Mngr.procName, name, strlen(name));

	//sprintf(fileName, "host:%s.txt", PARTITION_NAME);
	//Mngr.writeFile = fopen(fileName, "wt");
}
#endif

#ifdef _WIN32
unsigned long long GetCurrentSysTime(){
	unsigned long long time;
	time = GetTickCount();
	return time;
}
#else /*suppose to be VXWORKS*/
unsigned long long GetCurrentSysTime(){
	RETURN_CODE_TYPE retCode;
    SYSTEM_TIME_TYPE curTime;
    GET_TIME( &curTime, &retCode);
	return (unsigned long long)curTime;
}
#endif

void writeProfiler(){
#if 0
	unsigned int i;
	FILE *writeFile;
	char fileName[128];
	if(Mngr.fileNum >= Mngr.maxDump){
		return;
	}
	sprintf(fileName, "host:%s-%d.txt", Mngr.procName, Mngr.fileNum++);
	writeFile = fopen(fileName, "wt");
	for(i=0; i<Mngr.currentTop; i++){
		fprintf(writeFile, "%s %s 0x%64x 0x%64x\n", Atoms[i].funcName, Atoms[i].parentFuncName, Atoms[i].startTime, Atoms[i].endTime);
	}
	fflush(writeFile);
	fclose(writeFile);
#endif
}

void writeProfilerIndent(){
	unsigned int i,j;
	FILE *writeFile;
	char fileName[128];

	if(Mngr.fileNum >= Mngr.maxDump){
		return;
	}

	sprintf(fileName, "PFL_%s-%d.txt", Mngr.procName, Mngr.fileNum++);
	writeFile = fopen(fileName, "w");
	for(i=Mngr.initstack; i<Mngr.currentTop; i++){
		for(j=0; j<Atoms[i].callLevel; j++){
			fprintf(writeFile, "\t");
		}
		fprintf(writeFile, "%s %s %llu %llu %.3f\n", Atoms[i].funcName, Atoms[i].parentFuncName,
				Atoms[i].startTime, Atoms[i].endTime, (Atoms[i].endTime-Atoms[i].startTime)/1000000.0f);
	}
	fflush(writeFile);
	fclose(writeFile);
}


void ProfilerFlush(){
	writeProfilerIndent();
	Mngr.currentTop = Mngr.initstack;
}

void StartProfilerAtom(const char* name){
	int len = strlen(name);
	//flush
	if(MAX_DATA <= (Mngr.currentTop+1)){
		Mngr.initstack = Mngr.callStackTop;
		ProfilerFlush();
	}
	Mngr.callStack[Mngr.callStackTop] = Mngr.currentTop;
	Atoms[Mngr.currentTop].startTime = GetCurrentSysTime();
	Atoms[Mngr.currentTop].callLevel = Mngr.callStackTop;
	strncpy(Atoms[Mngr.currentTop].funcName, name, MIN(MAX_FUNCNAME, len));
	if(0 < Mngr.callStackTop){
		memcpy(Atoms[Mngr.currentTop].parentFuncName, Atoms[Mngr.callStack[Mngr.callStackTop-1]].funcName, MAX_FUNCNAME);
	}
	else{
		int length = strlen(Mngr.procName);
		memcpy(Atoms[Mngr.currentTop].parentFuncName, Mngr.procName, MIN(MAX_FUNCNAME, length));
	}
	Mngr.currentTop++;
	Mngr.callStackTop++;
}

void EndProfilerAtom(const char* name){
	//ensure the same func
	Mngr.callStackTop--;
	Atoms[Mngr.callStack[Mngr.callStackTop]].endTime = GetCurrentSysTime();
}
