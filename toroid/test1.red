 ;name Imp
 ; This is an ultra basic test of CORE WAR
;author A.K. Dewdney
;assert CORESIZE==8000
;assert PSPACESIZE>0
;assert MAXCYCLES==80000
;assert MAXPROCESSES==8000
;assert MINDISTANCE==100
      org   imp

imp:  mov.i   imp,  imp+1
      end 
